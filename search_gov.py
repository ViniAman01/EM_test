from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import selenium.common.exceptions as ex
import time,csv

driver = webdriver.Chrome()
driver.implicitly_wait(0.5)
driver.get("https://nces.ed.gov/globallocator/")
#if option.get_attribute('value') != None and != 'OTHER'
def return_options(tag_name: str):
    select = Select(driver.find_element(By.TAG_NAME,tag_name))
    all_options = select.options
    for option in select.options:
        value_len = len(option.get_attribute('value'))
        if value_len != 2:
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
        city_names.append(li.text)
    return city_names

def set_city_name(city_name: str):
    input_city = driver.find_element(By.ID,'city') 
    input_city.clear()
    input_city.send_keys(city_name)
    input_city.send_keys(Keys.ENTER)

def click_search():
    buttons = driver.find_elements(By.TAG_NAME,'input')
    for button in buttons:
        value = button.get_attribute('type')
        if 'submit' in value:
            button.click()
            break

def set_type_of_school(type: str):
    if(type.lower() == 'public'):
        checkbox = driver.find_element(By.XPATH,'//*[@id="institutions"]/table/tbody/tr/td/table/tbody/tr[4]/td[3]/font/input')
        checkbox.click()
    if(type.lower() == 'private'):
        checkbox = driver.find_element(By.XPATH,'//*[@id="institutions"]/table/tbody/tr/td/table/tbody/tr[5]/td[3]/font/input')
        checkbox.click()

def get_description():
    descs = driver.find_elements(By.CLASS_NAME,'InstDesc')
    for desc in descs:
        if desc.get_attribute('align') != 'center':
            desc_line = desc.text.splitlines()
            del desc_line[2:]
            print(desc_line)
            with open('US_schools.csv', 'w', newline='') as csv_file:
                spam_writer = csv.writer(csv_file, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                spam_writer.writerow(desc_line)


i = 0
options = return_options('select')
for option in options:
    option.click()
    open_window_city()
    switch_window(1)
    citys = get_city_names()
    driver.close()
    switch_window(0)
    i += len(citys)
    print(f'Num of citys: {i}')
    set_type_of_school('public')
    for city in citys:
        set_city_name(city)
        get_description()
