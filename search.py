from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import selenium.common.exceptions as ex
import time

driver = webdriver.Chrome()
driver.implicitly_wait(0.5)
driver.get("https://www.google.com/")
m = driver.find_element(By.NAME,"q")
m.send_keys("USA schools")
time.sleep(0.2)
m.send_keys(Keys.ENTER)
time.sleep(0.5)
# driver.find_element(By.XPATH,f'//*[@id="rso"]/div[{i}]/div/div/div[1]/div/a/h3').click()
elements = driver.find_elements(By.PARTIAL_LINK_TEXT,'school')
time.sleep(0.5)
for element in elements:
    try:
        print(element)
        element.click()
        time.sleep(1)
        if element:
            driver.back()
        time.sleep(1)
    except ex.ElementNotInteractableException:
        print("Elemento não interagivel!")
    except ex.StaleElementReferenceException:
        print("Elemento Obsoleto!")
    except ex.ElementClickInterceptedException:
        print("Click interceptado!")
