from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import selenium.common.exceptions as ex
import time

driver = webdriver.Chrome()
driver.implicitly_wait(0.5)
driver.get("https://nces.ed.gov/globallocator/")
# Seleciona cidades 
select = Select(driver.find_element(By.TAG_NAME, 'select'))
all_options = select.options
for option in all_options:
    value = option.get_attribute('value')
    if value and value != 'OTHER':
        print(f"Value: {value}")
        option.click()

browse_for_city = driver.find_element(By.PARTIAL_LINK_TEXT,'Browse')
time.sleep(0.5)
browse_for_city.click()
time.sleep(0.5)
windows =  driver.window_handles
driver.switch_to.window(windows[1])
time.sleep(0.5)
links = driver.find_elements(By.TAG_NAME,'a')
for a in links:
    try:
        value = a.get_attribute('value')
        print(f"Value: {value}")
        a.click()
        time.sleep(0.5)
    except ex.NoSuchWindowException:
        print("Selecionado!")
time.sleep(1000)
# table = driver.find_element(By.TAG_NAME,'ul')
# li = table.find_elements(By.TAG_NAME,'li')
# for item in li:
#     print(f"Value: {item.get_attribute('xpath')}")
# time.sleep(1000)
