import re
import requests
import xml.etree.ElementTree as ETree


def update_rss():
    request = requests.get('http://www.smbc-comics.com/rss.php', stream=True)
    tree = ETree.parse(request.raw)
    root = tree.getroot()

    for description in root.findall('./channel/item/description'):
        pattern = r'<img src="http://www\.smbc-comics\.com/comics/(\d+\-\d+)\.([pg][ni][gf])"/>(.*)'
        replace = r'<img src="http://www\.smbc-comics\.com/comics/\1\.\2"><br><br>' \
                  r'<img src="http://www\.smbc-comics\.com/comics/\1after\.png">\3'
        description.text = re.sub(pattern, replace, description.text)

    new_feed = ETree.tostring(root)

if __name__ == "__main__":
    update_rss()
