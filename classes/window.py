from selenium.webdriver.common.by import By

class WindowOperations:
    def __init__(self,driver):
        self.driver = driver
    def open_citys_window(self): #Window class
        browse_for_city = self.driver.find_element(By.PARTIAL_LINK_TEXT,'Browse')
        browse_for_city.click()

    def switch_window(self,num_window): #Window class
        windows =  self.driver.window_handles
        self.driver.switch_to.window(windows[num_window])
