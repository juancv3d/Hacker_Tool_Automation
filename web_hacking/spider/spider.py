
import requests
import re
# import urlparse


target_url = 'https://www.google.com/search?q=test'


def extract_links_from(url):
    response = requests.get(url)
    return re.findall(b'(?:href=")(.*?)"', response.content)


href_links = extract_links_from(target_url)

for link in href_links:
    # link = urlparse.urljoin(target_url, link)
    print(link)
