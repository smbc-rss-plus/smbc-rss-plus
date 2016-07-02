import os
import random

import boto3
import requests
from lxml import html
import lxml
import redis


def update_rss():
    request = requests.get('http://www.smbc-comics.com/rss.php', stream=True, timeout=20)
    root = lxml.etree.fromstring(request.content)
    cached_redis = redis.from_url(os.environ.get("REDIS_URL"))

    for title in root.findall('./channel/title'):
        title.text = "SMBC + Bonus Drawing"

    for link in root.findall('./channel/link'):
        link.text = 'http://smbc-rss-plus.mindflakes.com/'

    for atom_link in root.findall("./channel/{http://www.w3.org/2005/Atom}link"):
        atom_link.set('href', 'http://smbc-rss-plus.mindflakes.com/rss.xml')

    for description in root.findall('./channel/item/description'):
        description_root = html.fromstring(description.text)

        # Get Comic Link from description
        comic_url = description_root.xpath('/html/body/a/@href')[0]

        # Check if this item was already processed and restore the cached description
        new_description_str = cached_redis.get(str(comic_url))
        if new_description_str:
            description.text = new_description_str
            continue

        # Get comic's HTML
        comic_scrape_html = requests.get(comic_url, timeout=20)
        # Parse for Red Button Link in HTML
        comic_root = html.fromstring(comic_scrape_html.content)
        comic_img = comic_root.xpath("//*[@id=\"cc-comic\"]")[0]
        # Remove the id attribute since it's the right thing to do.
        comic_img.attrib.pop('id')
        red_button_comic_img = comic_root.xpath("//*[@id=\"aftercomic\"]/img")[0]
        # A break
        description_root.insert(0, lxml.html.Element("br"))
        # Stick the Red Button Image at the top
        description_root.insert(0, red_button_comic_img)
        # And a break
        description_root.insert(0, lxml.html.Element("br"))
        # Then at the top again, insert the comic image which had gone missing?
        description_root.insert(0, comic_img)

        # Add tagline so that users may find the RSS feed should it be desired
        tagline = r'<p>' \
                  r'<hr>' \
                  r'Red Button pushing provided by ' \
                  r'<a href="http://smbc-rss-plus.mindflakes.com">SMBC RSS Plus</a>' \
                  r'</p>' \
                  r'<br>'
        tagline_root = html.fromstring(tagline)

        description_root.append(tagline_root)

        description.text = lxml.etree.tostring(description_root)

        cached_redis.setex(comic_url, description.text, random.randint(3600, 36000))

    processed_feed = lxml.etree.tostring(root)

    upload_str(processed_feed)


def upload_str(feed: str):
    s3 = boto3.resource('s3')
    s3.Bucket('smbc-rss-plus.mindflakes.com').put_object(Key='rss.xml',
                                                         Body=feed,
                                                         ACL='public-read',
                                                         ContentType='application/xml')


if __name__ == "__main__":
    print("Updating RSS Feed.")
    update_rss()
    print("RSS Feed Updated.")
