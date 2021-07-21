
from bs4 import BeautifulSoup
import requests
import urllib.parse


def send_request(url):
    try:
        return requests.get(url, timeout=30)
    except requests.ConnectionError:
        pass


if __name__ == '__main__':
    """
    This script extracts the forms from the target website. 
    """
    target_url = 'http://192.168.1.8/mutillidae/index.php?page=dns-lookup.php'
    response = send_request(target_url)
    post_data = {}
    if response is not None:
        soup = BeautifulSoup(response.text, 'html.parser')
        forms = soup.find_all('form')
        for form in forms:
            action = form.get('action')
            if action is not None:
                action = urllib.parse.urljoin(target_url, action)
                method = form.get('method')
                print('[*] Method: %s | Action: %s' % (method, action))
            inputs = form.find_all('input')
            for input in inputs:
                name = input.get('name')
                if name is not None:
                    input_name = input.get('name')
                    input_type = input.get('type')
                    input_value = input.get('value')
                    print('[+] Input: %s | Name: %s | Type: %s | Value: %s' %
                          (input_type, input_name, input_type, input_value))
                    if input_type == 'text':
                        input_value = 'test'
                    post_data[input_name] = input_value
            result = requests.post(target_url, data=post_data)
            print(result.text)
