from selenium import webdriver

class DriverOperations:
    def __init__(self):
        self.driver = webdriver.Chrome()
    def start_driver(self):
        self.driver.implicitly_wait(0.5)
        self.driver.get("https://nces.ed.gov/globallocator/")
