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
    checkbox_public = driver.find_element(By.XPATH,'//*[@id="institutions"]/table/tbody/tr/td/table/tbody/tr[4]/td[3]/font/input')
    is_checked_public = checkbox_public.get_attribute('checked')
    print(f"public: {is_checked_public}")
    checkbox_private = driver.find_element(By.XPATH,'//*[@id="institutions"]/table/tbody/tr/td/table/tbody/tr[5]/td[3]/font/input')
    is_checked_private = checkbox_private.get_attribute('checked')
    print(f"private: {is_checked_private}")
    if 'public' in type.lower() and not 'private' in type.lower():
        if is_checked_private:
            checkbox_private.click()
        if not is_checked_public:
            checkbox_public.click()

    if 'private' in type.lower() and not 'public' in type.lower():
        if is_checked_public:
            checkbox_public.click()
        if not is_checked_private:
            checkbox_private.click()

    if 'public' in type.lower() and 'private' in type.lower():
        if not is_checked_public:
            checkbox_public.click()
        if not is_checked_private:
            checkbox_private.click()

def get_description(csv_file, i):
    descs = driver.find_elements(By.CLASS_NAME,'InstDesc')
    spam_writer = csv.writer(csv_file, dialect='excel')
    for desc in descs:
        if desc.get_attribute('align') != 'center':
            desc_line = desc.text.splitlines()
            i += len(desc_line)/3
            del desc_line[2:]
            print(desc_line)
            spam_writer.writerow(desc_line)
    return i


i = 0
distric = 0
options = return_options('select')
index = 0
with open('US_schools.csv', 'w', newline='') as csv_file:
    for index in range(len(options)):
        options[index].click()
        open_window_city()
        switch_window(1)
        citys = get_city_names()
        driver.close()
        switch_window(0)
        set_type_of_school('public and private')
        for city in citys:
            set_city_name(city)
            i = get_description(csv_file,i)
            print(f'Número de escolas: {i}')
        distric += 1
        options = return_options('select')
        index += 1

