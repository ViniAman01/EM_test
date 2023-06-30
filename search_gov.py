from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import selenium.common.exceptions as ex
import time

driver = webdriver.Chrome()
driver.implicitly_wait(0.5)
driver.get("https://nces.ed.gov/globallocator/")
#if option.get_attribute('value') != None and != 'OTHER'
def return_options(tag_name: str):
    select = Select(driver.find_element(By.TAG_NAME,tag_name))
    all_options = select.options
    for option in all_options:
        if option and option.get_attribute('value') != 'OTHER':
            all_options.remove(option)
    return all_options

def open_window_city():
    browse_for_city = driver.find_element(By.PARTIAL_LINK_TEXT,'Browse')
    time.sleep(0.5)
    browse_for_city.click()

def switch_window(num_window):
    windows =  driver.window_handles
    driver.switch_to.window(windows[num_window])

def get_city_names():
    lists = driver.find_elements(By.TAG_NAME,'li')
    city_names = []
    for li in lists:
        print(li.text)
        city_names.append(li.text)
    return city_names

def set_city_name(city_name: str):
    input_city = driver.find_element(By.ID,'city') 
    input_city.clear()
    input_city.send_keys(city_name)

i = 0
options = return_options('select')
for option in options:
    option.click()
    open_window_city()
    switch_window(1)
    citys = get_city_names()
    driver.close()
    switch_window(0)
    for city in citys:
        i += 1
        set_city_name(city)
print(i)
# table = driver.find_element(By.TAG_NAME,'ul')
# li = table.find_elements(By.TAG_NAME,'li')
# for item in li:
#     print(f"Value: {item.get_attribute('xpath')}")
# time.sleep(1000)
