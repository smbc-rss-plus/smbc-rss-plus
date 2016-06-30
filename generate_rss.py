import boto3
import re
import requests
import xml.etree.ElementTree as ETree
import redis

def update_rss():
    request = requests.get('http://www.smbc-comics.com/rss.php', stream=True)
    tree = ETree.parse(request.raw)
    root = tree.getroot()

    for title in root.findall('./channel/title'):
        title.text = "SMBC + Bonus Drawing"

    for link in root.findall('./channel/link'):
        link.text = 'http://smbc-rss-plus.mindflakes.com/'

    for atom_link in root.findall("./channel/{http://www.w3.org/2005/Atom}link"):
        atom_link.set('href', 'http://smbc-rss-plus.mindflakes.com/rss.xml')

    for description in root.findall('./channel/item/description'):
        # Should I be doing this with Regexps? Probably not. Do I care? No.
        # Tony the Pony, I welcome you!
        pattern = r'<img src="http://www\.smbc-comics\.com/comics/\.\./comics/(\d+\-\d+)\.([pg][ni][gf])"/>(.*)'
        replace = r'<img src="http://www.smbc-comics.com/comics/../comics/\1.\2"><br><br>' \
                  r'<img src="http://www.smbc-comics.com/comics/../comics/\1after.png"><br>' \
                  r'\3  '

        tagline = r'<p>' \
                  r'<hr>' \
                  r'Red Button pushing provided by ' \
                  r'<a href="http://smbc-rss-plus.mindflakes.com">SMBC RSS Plus</a>' \
                  r'</p>' \
                  r'<br>'

        description.text = re.sub(pattern, replace, description.text) + tagline

    processed_feed = ETree.tostring(root)

    print(processed_feed)
    

def upload_str(feed: str):
    s3 = boto3.resource('s3')
    s3.Bucket('smbc-rss-plus.mindflakes.com').put_object(Key='rss.xml',
                                                         Body=feed,
                                                         ACL='public-read',
                                                         ContentType='application/xml')

def process_description(description):
    pass

if __name__ == "__main__":
    print("Updating RSS Feed.")
    update_rss()
    print("RSS Feed Updated.")
