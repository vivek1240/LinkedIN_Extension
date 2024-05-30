# import requests
# import re

# class LinkedIn:

#     def __init__(self):
#         self.s = requests.Session()
#         self.headers = {
#             "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
#             "Accept-Language": "en-US,en;q=0.9",
#             "Referer": "https://www.linkedin.com/",
#             "Connection": "keep-alive"
#         }


#     def login(self, email, password):
#         try:
#             sc = self.s.get("https://www.linkedin.com/login", headers=self.headers).text
#         except Exception as e:
#             print(f"Error during GET request: {e}")
#             return False

#         try:
#             csrfToken = sc.split('csrfToken" value="')[1].split('"')[0]
#             sid = sc.split('sIdString" value="')[1].split('"')[0]
#             pins = sc.split('pageInstance" value="')[1].split('"')[0]
#             lcsrf = sc.split('loginCsrfParam" value="')[1].split('"')[0]
#         except Exception as e:
#             print(f"Error parsing the login page: {e}")
#             return False

#         data = {
#             'csrfToken': csrfToken,
#             'session_key': email,
#             'ac': '2',
#             'sIdString': sid,
#             'parentPageKey': 'd_checkpoint_lg_consumerLogin',
#             'pageInstance': pins,
#             'trk': 'public_profile_nav-header-signin',
#             'authUUID': '',
#             'session_redirect': 'https://www.linkedin.com/feed/',
#             'loginCsrfParam': lcsrf,
#             'fp_data': 'default',
#             '_d': 'd',
#             'showGoogleOneTapLogin': 'true',
#             'controlId': 'd_checkpoint_lg_consumerLogin-login_submit_button',
#             'session_password': password,
#             'loginFlow': 'REMEMBER_ME_OPTIN'
#         }

#         try:
#             after_login = self.s.post("https://www.linkedin.com/checkpoint/lg/login-submit", headers=self.headers, data=data).text
#         except Exception as e:
#             print(f"Error during POST request: {e}")
#             return False

#         is_logged_in = after_login.split('<title>')[1].split('</title>')[0].strip()
#         if is_logged_in == "LinkedIn":
#             return True
#         else:
#             print("Login failed, possibly due to incorrect credentials or changes in LinkedIn's login mechanism.")
#             return False

#     def bulkScan(self, profiles):
#         all_emails = []
#         for profile in profiles:
#             profile = profile + "/detail/contact-info/"
#             sc = self.s.get(profile, headers=self.headers, allow_redirects=True).text
#             emails_found = re.findall(r'[a-zA-Z0-9\.\-\_i]+@[\w.]+', sc)
#             all_emails.extend(emails_found)
#         return all_emails

#     def singleScan(self, profile):
#         profile = profile + "/detail/contact-info/"
#         sc = self.s.get(profile, headers=self.headers, allow_redirects=True).text
#         emails_found = re.findall(r'[a-zA-Z0-9\.\-\_i]+@[\w.]+', sc)
#         return emails_found

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import re

class LinkedIn:
    def __init__(self):
        self.driver = webdriver.Chrome()  # Ensure you have ChromeDriver installed and added to PATH
        self.driver.implicitly_wait(10)

    def login(self, email, password):
        self.driver.get("https://www.linkedin.com/login")
        time.sleep(2)  # Wait for the page to load
        print(f"email:"{email "password":{password}})
        email_field = self.driver.find_element_by_id("username")
        password_field = self.driver.find_element_by_id("password")
        print(f"email_field:"{email_field "password_field":{password_field}})
        email_field.send_keys(email)
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)
        time.sleep(5)  # Wait for the login process
        if "feed" in self.driver.current_url:
            print("inside feed")
            return True
        else:
            print("outside feed")
            return False

    def bulkScan(self, profiles):
        all_emails = []
        for profile in profiles:
            profile_url = profile + "/detail/contact-info/"
            self.driver.get(profile_url)
            time.sleep(2)  # Wait for the page to load
            sc = self.driver.page_source
            emails_found = re.findall(r'[a-zA-Z0-9\.\-\_i]+@[\w.]+', sc)
            all_emails.extend(emails_found)
        return all_emails

    def singleScan(self, profile):
        profile_url = profile + "/detail/contact-info/"
        self.driver.get(profile_url)
        time.sleep(2)  # Wait for the page to load
        sc = self.driver.page_source
        emails_found = re.findall(r'[a-zA-Z0-9\.\-\_i]+@[\w.]+', sc)
        return emails_found


    def close(self):
        self.driver.quit()