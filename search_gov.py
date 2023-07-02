from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import csv

driver = webdriver.Chrome()
driver.implicitly_wait(0.5)
driver.get("https://nces.ed.gov/globallocator/")

def return_select_options(tag_name: str):
    select = Select(driver.find_element(By.TAG_NAME,tag_name))
    all_options = select.options
    for option in select.options:
        value_len = len(option.get_attribute('value'))
        if value_len != 2:
            all_options.remove(option)
    return all_options

def open_citys_window(): #Window class
    browse_for_city = driver.find_element(By.PARTIAL_LINK_TEXT,'Browse')
    browse_for_city.click()

def switch_window(num_window): #Window class
    windows =  driver.window_handles
    driver.switch_to.window(windows[num_window])

def get_citys_names(): #City class
    lists_of_citys = driver.find_elements(By.TAG_NAME,'li')
    city_names = []
    for li in lists_of_citys:
        city_names.append(li.text)
    return city_names

def set_city_name(city_name: str): #City class
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

def set_type_of_school(school_type: str): #School class
    checkbox_public = driver.find_element(By.XPATH,'//*[@id="institutions"]/table/tbody/tr/td/table/tbody/tr[4]/td[3]/font/input')
    is_checked_public = checkbox_public.get_attribute('checked')
    checkbox_private = driver.find_element(By.XPATH,'//*[@id="institutions"]/table/tbody/tr/td/table/tbody/tr[5]/td[3]/font/input')
    is_checked_private = checkbox_private.get_attribute('checked')
    if 'public' in school_type.lower() and not 'private' in school_type.lower():
        if is_checked_private:
            checkbox_private.click()
        if not is_checked_public:
            checkbox_public.click()

    if 'private' in school_type.lower() and not 'public' in school_type.lower():
        if is_checked_public:
            checkbox_public.click()
        if not is_checked_private:
            checkbox_private.click()

    if 'public' in school_type.lower() and 'private' in school_type.lower():
        if not is_checked_public:
            checkbox_public.click()
        if not is_checked_private:
            checkbox_private.click()

def set_school_description(csv_file, count): #School class
    schools_descriptions = driver.find_elements(By.CLASS_NAME,'InstDesc')
    spam_writer = csv.writer(csv_file, dialect='excel')
    for description in schools_descriptions:
        if description.get_attribute('align') != 'center':
            description_line = description.text.splitlines()
            count += len(description_line)/3
            del description_line[3:]
            description_line[2] = description_line[2].replace(' ','')
            description_line[2] = description_line[2][:13]
            spam_writer.writerow(description_line)
    return count

i = 0
distric = 0
options = return_select_options('select')
index = 0
with open('US_schools.csv', 'w', newline='') as csv_file:
    spam_writer = csv.writer(csv_file, dialect='excel')
    spam_writer.writerow(["Name","Adress","Phone","Type"])
    for index in range(len(options)):
        options[index].click()
        open_citys_window()
        switch_window(1)
        citys = get_citys_names()
        driver.close()
        switch_window(0)
        set_type_of_school('public and private')
        for city in citys[-1:]:
            set_city_name(city)
            i = set_school_description(csv_file,i)
            print(f'Número de escolas: {i}')
        distric += 1
        options = return_select_options('select')
        index += 1
