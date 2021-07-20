
from bs4 import BeautifulSoup
import requests


def send_request(url):
    try:
        return requests.get(url, timeout=30)
    except requests.ConnectionError:
        pass


if __name__ == '__main__':
    target_url = 'http://192.168.1.8/mutillidae/index.php?page=dns-lookup.php'
    response = send_request(target_url)
    if response is not None:
        soup = BeautifulSoup(response.text, 'html.parser')
        forms = soup.find_all('form')
        for form in forms:
            action = form.get('action')
            if action is not None:
                print('Action: ' + action)
            method = form.get('method')
            if method is not None:
                print('Method: ' + method)
            inputs = form.find_all('input')
            for input in inputs:
                print('Input: ' + str(input.get('name')) +
                      ' ' + str(input.get('value')))
