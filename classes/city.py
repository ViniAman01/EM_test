from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

class CityOperations: 
    def __init__(self,driver):
        self.driver = driver

    def get_citys_names(self): #City class
        lists_of_citys = self.driver.find_elements(By.TAG_NAME,'li')
        city_names = []
        for li in lists_of_citys:
            city_names.append(li.text)
        return city_names


    def put_city_in_input_box(self,city_name: str): #City class
        input_city = self.driver.find_element(By.ID,'city') 
        input_city.clear()
        input_city.send_keys(city_name)
        input_city.send_keys(Keys.ENTER)
