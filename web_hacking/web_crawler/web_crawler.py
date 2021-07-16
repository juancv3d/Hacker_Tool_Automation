
import requests
import multiprocessing
import concurrent.futures

target_url = 'google.com'
common_subdomains = 'short-wordlist.txt'
common_directories = 'dir-wordlist.txt'


def send_request(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print('[+] Discovered URL --> ' + url)
    except requests.ConnectionError:
        pass
    except requests.exceptions.Timeout:
        pass


def search_subdomains(common_subdomains):
    try:
        with open(common_subdomains, 'r') as f:
            for line in f:
                subdomain = line.strip()
                test_url = f'https://{subdomain}.{target_url}'
                send_request(test_url)
    except FileNotFoundError:
        print('[-] Can\'t open the file: ' + common_subdomains)
        exit()


def search_directories(common_directories):
    try:
        with open(common_directories, 'r') as f:
            for line in f:
                directory = line.strip()
                test_url = f'https://{target_url}/{directory}'
                send_request(test_url)
    except FileNotFoundError:
        print('[-] Can\'t open the file: ' + common_directories)
        exit()


if __name__ == '__main__':
    search_subdomains(common_directories)
    search_directories(common_directories)
