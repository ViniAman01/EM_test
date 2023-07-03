from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import csv

class Driver:
    def __init__(self):
        self.driver = webdriver.Chrome()
    def start_driver(self):
        self.driver.implicitly_wait(0.5)
        self.driver.get("https://nces.ed.gov/globallocator/")

class State(Driver):
    def __init__(self,tag_name: str):
        self.tag_name = tag_name
    def return_select_options(self):
        select = Select(self.driver.find_element(By.TAG_NAME,self.tag_name))
        all_options = select.options
        for option in select.options:
            value_len = len(option.get_attribute('value'))
            if value_len != 2:
                all_options.remove(option)
        return all_options

class Window(Driver):
    def open_citys_window(self): #Window class
        browse_for_city = self.driver.find_element(By.PARTIAL_LINK_TEXT,'Browse')
        browse_for_city.click()

    def switch_window(self,num_window): #Window class
        windows =  self.driver.window_handles
        self.driver.switch_to.window(windows[num_window])

class City(Driver): 
    def __init__(self,city_name: str):
        self.city_name = city_name

    def get_citys_names(self): #City class
        lists_of_citys = self.driver.find_elements(By.TAG_NAME,'li')
        city_names = []
        for li in lists_of_citys:
            city_names.append(li.text)
        return city_names

    def set_city_name(self): #City class
        input_city = self.driver.find_element(By.ID,'city') 
        input_city.clear()
        input_city.send_keys(self.city_name)
        input_city.send_keys(Keys.ENTER)

class School(Driver):
    def __init__(self,type_school: str):
        self.type_school = type_school

    def set_type_of_school(self): #School class
        checkbox_public = self.driver.find_element(By.XPATH,'//*[@id="institutions"]/table/tbody/tr/td/table/tbody/tr[4]/td[3]/font/input')
        is_checked_public = checkbox_public.get_attribute('checked')
        checkbox_private = self.driver.find_element(By.XPATH,'//*[@id="institutions"]/table/tbody/tr/td/table/tbody/tr[5]/td[3]/font/input')
        is_checked_private = checkbox_private.get_attribute('checked')
        if 'public' in self.type_school.lower() and not 'private' in self.type_school.lower():
            if is_checked_private:
                checkbox_private.click()
            if not is_checked_public:
                checkbox_public.click()

        if 'private' in self.type_school.lower() and not 'public' in self.type_school.lower():
            if is_checked_public:
                checkbox_public.click()
            if not is_checked_private:
                checkbox_private.click()

        if 'public' in self.type_school.lower() and 'private' in self.type_school.lower():
            if not is_checked_public:
                checkbox_public.click()
            if not is_checked_private:
                checkbox_private.click()

    def adjust_description_line(self,description):
        description_line = description.text.splitlines()
        description_line[0] = description_line[0][2:]
        del description_line[3:]
        description_line[2] = description_line[2].replace(' ','')
        description_line[2] = description_line[2][:13]
        description_line.append(self.type_school)

        return description_line

    def set_school_description(self,csv_file, count): #School class
        public_schools_descriptions = self.driver.find_elements(By.ID,'hiddenitems_school')
        private_schools_descriptions = self.driver.find_elements(By.ID,'hiddenitems_privschool')
        spam_writer = csv.writer(csv_file, dialect='excel')
        for description in public_schools_descriptions:
            if description.get_attribute('align') != 'center':
                description_line = self.adjust_description_line(description,'Public')
                spam_writer.writerow(description_line)

        for description in private_schools_descriptions:
            if description.get_attribute('align') != 'center':
                description_line = self.adjust_description_line(description,'Private')
                spam_writer.writerow(description_line)
        return count

i = 0
distric = 0
options = return_select_options('select')
index = 0
csv_file = open('US_schools.csv', 'w', newline='')
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
    for city in citys:
        set_city_name(city)
        i = set_school_description(csv_file,i)
        print(f'Número de escolas: {i}')
    distric += 1
    options = return_select_options('select')
    index += 1
