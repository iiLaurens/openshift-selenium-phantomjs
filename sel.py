import os
from selenium import webdriver

driver = webdriver.PhantomJS(service_log_path=os.path.join(os.environ['OPENSHIFT_DATA_DIR'],'log.log'),port='127.8.80.1:17771')

driver.get("https://duckduckgo.com/")
driver.find_element_by_id('search_form_input_homepage').send_keys("realpython")
driver.find_element_by_id("search_button_homepage").click()
print driver.current_url
driver.quit()