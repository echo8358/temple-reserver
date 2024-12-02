from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import requests
import json

def getLoginCookies():
    driver = webdriver.Firefox()
    driver.get("https://temple-online-scheduling.churchofjesuschrist.org/?locale=en")
    time.sleep(5)
    #try:
    #        elem = WebDriverWait(driver, 30).until( EC.presence_of_element_located((By.ID, "input28")))
    #except:
    #    print("username element not found")
    elem = driver.find_element(By.ID, "input28")
    elem.send_keys("higgcody")
    elem.send_keys(Keys.RETURN)
    time.sleep(2)
    elem = driver.find_element(By.ID, "input53")
    elem.send_keys(open("passwd",'r').read())
    elem.send_keys(Keys.RETURN)

    time.sleep(5)
    
    ret_val = driver.get_cookies()

    return ret_val

def getReqCookies(cookies):
    requests_cookies = {}
    for c in cookies:
        requests_cookies[c['name']] = c['value']    

    return requests_cookies

class Sessions():
    parsedSessions = {}
    def __init__(self, jsonString):
        self.parsedSessions = json.loads(jsonString)

    def getSessionsWithSpots(self, numSpots: int):
        for session in self.parsedSessions['sessionList']:
            #print(session)
            if session['details']['seatsAvailable'] >= numSpots:
                print(session)






def main():
    req_cookies = getReqCookies(getLoginCookies())
    
    #print(req_cookies)
    #response = requests.get('https://temple-online-scheduling.churchofjesuschrist.org/api/userInfo', cookies=req_cookies)
    json = {"sessionYear":2024,"sessionMonth":8,"sessionDay":17,"appointmentType":"PROXY_BAPTISM","templeOrgId":4012416,"isGuestConfirmation":False}
    headers = {'Content-type': 'application/json', 'Accept': '*/*'}
    response = requests.post("https://temple-online-scheduling.churchofjesuschrist.org/api/templeSchedule/getSessionInfo", cookies=req_cookies, json=json, headers=headers)
    #response = requests.get('https://temple-online-scheduling.churchofjesuschrist.org/api/templeSchedule/getSessionInfo', cookies=req_cookies, data='{"sessionYear":2024,"sessionMonth":8,"sessionDay":17,"appointmentType":"PROXY_BAPTISM","templeOrgId":4012416,"isGuestConfirmation":false}')    
    #print(response)
    #print(response.text)

    sessions = Sessions(response.text)
    sessions.getSessionsWithSpots(1)

main()
