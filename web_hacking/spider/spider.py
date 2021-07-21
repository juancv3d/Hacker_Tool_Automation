
import requests
import re
from urllib.parse import urljoin


target_url = 'https://3dimpressio.co'
target_links = []


def extract_links_from(url):
    """
    extract all the links from the given url.

    """
    response = requests.get(url)
    return re.findall('(?:href=")(.*?)"', str(response.content))


def crawler(url):
    """
    This function is the main crawler function. and it will be called recursively to search for all the links in the given url.

    Args:
        url (string): The url to be crawled.
    """
    href_links = extract_links_from(target_url)
    for link in href_links:
        link = urljoin(url, link)

        if '#' in link:
            link = link.split('#')[0]

        if url in link and link not in target_links:
            target_links.append(link)
            print(link)
            crawler(link)


if __name__ == '__main__':
    crawler(target_url)
