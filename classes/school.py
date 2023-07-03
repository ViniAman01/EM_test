from selenium.webdriver.common.by import By
from classes.window import WindowOperations
from classes.city import CityOperations
from classes.state import StateOperations
import csv

class SchoolOperations:
    def __init__(self,driver):
        self.driver = driver

    def set_type_of_school(self,type_school): #School class
        checkbox_public = self.driver.find_element(By.XPATH,'//*[@id="institutions"]/table/tbody/tr/td/table/tbody/tr[4]/td[3]/font/input')
        is_checked_public = checkbox_public.get_attribute('checked')

        checkbox_private = self.driver.find_element(By.XPATH,'//*[@id="institutions"]/table/tbody/tr/td/table/tbody/tr[5]/td[3]/font/input')
        is_checked_private = checkbox_private.get_attribute('checked')

        if 'public' in type_school.lower() and not 'private' in type_school.lower():
            if is_checked_private:
                checkbox_private.click()
            if not is_checked_public:
                checkbox_public.click()

        if 'private' in type_school.lower() and not 'public' in type_school.lower():
            if is_checked_public:
                checkbox_public.click()
            if not is_checked_private:
                checkbox_private.click()

        if 'public' in type_school.lower() and 'private' in type_school.lower():
            if not is_checked_public:
                checkbox_public.click()
            if not is_checked_private:
                checkbox_private.click()

    def adjust_description_line(self,description,type_school):
        description_line = description.text.splitlines()
        description_line[0] = description_line[0][2:]
        del description_line[3:]
        description_line[2] = description_line[2].replace(' ','')
        description_line[2] = description_line[2][:13]
        description_line.append(type_school)

        return description_line

    def set_school_description(self,csv_file): #School class
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

    def search_school(self,number_school,type_school):
        window = WindowOperations(self.driver)
        city = CityOperations(self.driver)
        state = StateOperations('select',self.driver)

        self.set_type_of_school(type_school)
        options = state.return_select_options()

        csv_file = open('US_schools.csv', 'w', newline='')
        spam_writer = csv.writer(csv_file, dialect='excel')
        spam_writer.writerow(["Name","Adress","Phone","Type"])

        index = 0

        for index in range(len(options)):
            options[index].click()
            window.open_citys_window()
            window.switch_window(1)
            citys_names = city.get_citys_names()
            window.switch_window(0)

            for city_name in citys_names:
                city.point_cursor_in_input_box(city_name)
                self.set_school_description(csv_file)

            options = state.return_select_options()
            index += 1
        
        csv_file.close()
