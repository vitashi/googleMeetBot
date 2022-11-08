import uuid
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class DriverSession():
    def __init__(self, meetingURL: str, attendanceName: str, chatMessage: str):
        self.meetingURL = meetingURL
        self.attendanceName = attendanceName
        self.chatMessage = chatMessage
        self.id = str(uuid.uuid4())
        self.driver = None
        self.update = None

    def start(self):
        opt = webdriver.ChromeOptions()
        opt.add_argument("--disable-dev-shm-usage")
        opt.add_argument('--profile-directory=Default')
        opt.add_argument('--user-data-dir=/home/seluser/.config/google-chrome')
        opt.add_argument("--disable-blink-features")
        opt.add_argument('--disable-blink-features=AutomationControlled')
        opt.add_argument('--start-maximized')
        opt.add_argument("--verbose")
        opt.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.5304.87 Safari/537.36")
        opt.add_experimental_option("excludeSwitches", ["enable-automation"])
        opt.add_experimental_option('useAutomationExtension', False)
        opt.add_experimental_option("prefs", {
            "profile.default_content_setting_values.media_stream_mic": 1,
            "profile.default_content_setting_values.media_stream_camera": 1,
            "profile.default_content_setting_values.geolocation": 0,
            "profile.default_content_setting_values.notifications": 1
        })

        self.driver = webdriver.Remote(
			command_executor='http://chrome:4444/wd/hub',
			options=opt)

        self.update = "Bot initiated"

    def mimicHumanTyping(self, inputBox, input:str, enter:bool=True):
        time.sleep(1)
        for char in input:
            time.sleep(0.1)
            inputBox.send_keys(char)
        time.sleep(5)
        if enter: inputBox.send_keys(Keys.ENTER)
        self.driver.implicitly_wait(100)

    def accessMeeting(self, meetingURL:str):
        self.driver.get('https://google.com')
        time.sleep(5)
        self.driver.get(meetingURL)
        self.driver.implicitly_wait(100)
        self.update = "Meeting url accessed"

    def inPutAttendanceName(self, name:str):
        time.sleep(20)
        inputBox = self.driver.find_element(By.ID, "c7")
        inputBox.click()
        self.mimicHumanTyping(inputBox, name)
        self.update = "Attendance name entered"

    def addChatMessage(self, message: str):
        time.sleep(5)
        self.driver.find_element(By.XPATH, "/html/body[@class='EIlDfe J0p3ve']/div[@id='yDmH0d']/c-wiz[@id='ow3']/div[@class='T4LgNb']/div[@class='kFwPee']/div[12]/div[@class='crqnQb']/div[@class='UnvNgf Sdwpn  P9KVBf IYIJAc BIBiNe']/div[@class='jsNRx']/div[@class='fXLZ2']/div[@class='PL2QSb LgPKBb']/div[@class='SGP0hd kunNie']/div[@class='r6xAKc'][3]/span/button[@class='VfPpkd-Bz112c-LgbsSe yHy1rc eT1oJ JsuyRc boDUxc']").click()
        time.sleep(5)
        chatbox = self.driver.find_element(By.XPATH, "/html/body[@class='EIlDfe J0p3ve']/div[@id='yDmH0d']/c-wiz[@id='ow3']/div[@class='T4LgNb']/div[@class='kFwPee']/div[12]/div[@class='crqnQb']/div[@class='R3Gmyc qwU8Me']/div[@class='WUFI9b']/div[@class='hWX4r']/div[@class='vvTMTb']/div[@class='NiQxf XpnDCe']/div[@class='bXH0G']/div[@class='Ufn6O XnKlKd']/label[@class='VfPpkd-fmcmS-yrriRe VfPpkd-fmcmS-yrriRe-OWXEXe-mWPk3d VfPpkd-ksKsZd-mWPk3d VfPpkd-fmcmS-yrriRe-OWXEXe-B7I4Od VfPpkd-fmcmS-yrriRe-OWXEXe-di8rgd-V67aGc VfPpkd-fmcmS-yrriRe-OWXEXe-INsAgc cfWmIb orScbe kxz0kd edOlkc iL4fNe VfPpkd-fmcmS-yrriRe-OWXEXe-XpnDCe']/textarea[@id='bfTqV']")
        self.mimicHumanTyping(chatbox, message)
        self.update = "Chat message entered"

    def run(self):
        print("Test started")
        self.accessMeeting(self.meetingURL)
        self.inPutAttendanceName(self.attendanceName)
        self.addChatMessage(self.chatMessage)


class DriverSessions():
    def __init__(self):
        self.store = {}

    def addSession(self, meetingURL: str, attendanceName: str, chatMessage: str):
        session = DriverSession(meetingURL, attendanceName, chatMessage)
        self.store[session.id] = session
        return session.id

    def getSession(self, sessionId):
        return self.store[sessionId]
