__author__ = 'nelson'

import requests
import xml.etree.ElementTree as etree

request = requests.get('http://www.smbc-comics.com/rss.php', stream=True)

tree = etree.parse(request.raw)

root = tree.getroot()

root