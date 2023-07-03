from classes.school import SchoolOperations
from classes.driver import DriverOperations

driver_chrome = DriverOperations()
driver_chrome.start_driver()
school = SchoolOperations(driver_chrome.driver)
school.search_school(1000,'Public')
