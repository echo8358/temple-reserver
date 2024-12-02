from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import requests
import json
import random

from model import *

class WebInterface():
    cookies: str = ""
    username: str = "higgcody"
    password: str = open("passwd",'r').read()

    def __init__(self) -> None:
        #self.username: str = username
        #self.password: str = password
        self.cookies = self.getCookies()

    def getCookies(self):
        try:
            cookies = json.loads(open('cookies','r').read())
            headers = {'Content-type': 'application/json', 'Accept': '*/*'}
            jsonBody = {"sessionYear":2024,"sessionMonth":8,"sessionDay":17,"appointmentType":"PROXY_BAPTISM","templeOrgId":4012416,"isGuestConfirmation":False}
            #response = requests.get('https://temple-online-scheduling.churchofjesuschrist.org/api/userInfo', cookies=cookies, headers=headers)
            response = requests.post("https://temple-online-scheduling.churchofjesuschrist.org/api/templeSchedule/getSessionInfo", cookies=cookies, json=jsonBody, headers=headers)
            print(response.status_code)
            print(response.history)
            time.sleep(5)
            response.raise_for_status()
            if response.history:
                raise Exception("redirected, invalid cookie")
            print(cookies)
        
        except Exception as e:
            print(repr(e))
            cookies = self.convertLoginToRequestCookies(self.getLoginCookies(self.username, self.password))
        return cookies

    def getLoginCookies(self, username, password) -> str:
        driver = webdriver.Firefox()
        driver.get("https://temple-online-scheduling.churchofjesuschrist.org/?locale=en")
        time.sleep(5)
        #try:
        #        elem = WebDriverWait(driver, 30).until( EC.presence_of_element_located((By.ID, "input28")))
        #except:
        #    print("username element not found")
        elem = driver.find_element(By.ID, "input28")
        elem.send_keys(username)
        elem.send_keys(Keys.RETURN)
        time.sleep(2+random.uniform(0, 2))
        elem = driver.find_element(By.ID, "input53")
        elem.send_keys(password)
        elem.send_keys(Keys.RETURN)

        time.sleep(5+random.uniform(0,2))
        
        ret_val = driver.get_cookies()
        driver.close()

        return ret_val

    def convertLoginToRequestCookies(self, request_cookies: str) -> dict:
        requests_cookies = {}
        for c in request_cookies:
            requests_cookies[c['name']] = c['value']    

        f = open('cookies', 'w')
        f.write(json.dumps(requests_cookies))
        f.close()

        return requests_cookies

    def getSessionInfo(self, sessionRequest: SessionRequest.SessionRequest):
        #json = {"sessionYear":2024,"sessionMonth":8,"sessionDay":17,"appointmentType":"PROXY_BAPTISM","templeOrgId":4012416,"isGuestConfirmation":False}
        headers = {'Content-type': 'application/json', 'Accept': '*/*'}
        response = requests.post("https://temple-online-scheduling.churchofjesuschrist.org/api/templeSchedule/getSessionInfo", cookies=self.cookies, json=sessionRequest.__dict__, headers=headers)
        if response.status_code >= 400:
            self.cookies = self.getCookies()
            response = requests.post("https://temple-online-scheduling.churchofjesuschrist.org/api/templeSchedule/getSessionInfo", cookies=self.cookies, json=sessionRequest.__dict__, headers=headers)

        sessionResponse = SessionResponse.SessionResponse(response.json())
        return sessionResponse


