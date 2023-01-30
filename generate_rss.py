from datetime import timedelta
import requests_cache
from lxml import html
import lxml
from tenacity import retry, stop_after_attempt


@retry(stop=stop_after_attempt(3))
def update_rss():
    session = requests_cache.CachedSession('cache/cache.sqlite')

    request = session.get('http://www.smbc-comics.com/rss.php', stream=True, timeout=20)
    root = lxml.etree.fromstring(request.content)

    for title in root.findall('./channel/title'):
        title.text = "SMBC + Bonus Drawing"

    for link in root.findall('./channel/link'):
        link.text = 'http://smbc-rss-plus.mindflakes.com/'

    for atom_link in root.findall("./channel/{http://www.w3.org/2005/Atom}link"):
        atom_link.set('href', 'http://smbc-rss-plus.mindflakes.com/rss.xml')

    for item in root.findall('./channel/item'):
        description_root = html.fromstring(item.findall("description")[0].text)

        # Get Comic Link from Item Link
        comic_url = item.findall("link")[0].text

        # Get comic's HTML
        comic_scrape_html = session.get(comic_url, timeout=20, expire_after=timedelta(days=1))
        comic_root = html.fromstring(comic_scrape_html.content)
        # Parse for Comic Img
        comic_img = comic_root.xpath("//*[@id=\"cc-comic\"]")[0]
        # Remove the id attribute since it's the right thing to do.
        comic_img.attrib.pop('id')
        # Parse for Red Button Link
        red_button_comic_img = comic_root.xpath("//*[@id=\"aftercomic\"]/img")[0]
        # A break
        description_root.append(lxml.html.Element("hr"))
        # Stick the Red Button Image at the bottom
        description_root.append(lxml.html.Element("br"))
        description_root.append(red_button_comic_img)

        # Add tagline so that users may find the RSS feed should it be desired
        tagline = '<p>' \
                  '<hr>' \
                  'Red Button mashing provided by ' \
                  '<a href="http://smbc-rss-plus.mindflakes.com">SMBC RSS Plus</a>. ' \
                  'If you consume this comic through RSS, you may want to support ' \
                  '<a href="https://www.patreon.com/ZachWeinersmith">Zach\'s Patreon</a> ' \
                  'for like a $1 or something at least especially' \
                  ' since this is scraping the site deeper than provided.' \
                  '</p>' \
                  '<br>'
        tagline_root = html.fromstring(tagline)

        description_root.append(tagline_root)

        item.findall("description")[0].text = lxml.etree.tostring(description_root)

    processed_feed = lxml.etree.tostring(root)

    with open("output/rss.xml", "wb") as f:
        print("Writing Feed Locally")
        f.write(processed_feed)

if __name__ == "__main__":
    print("Updating RSS Feed.")
    update_rss()
    print("RSS Feed Updated.")
