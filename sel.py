import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.PhantomJS(service_log_path=os.path.join(os.environ['OPENSHIFT_DATA_DIR'],'log.log'),port='127.8.80.1:17771')

driver.get("http://www.python.org")
assert "Python" in driver.title
elem = driver.find_element_by_name("q")
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)
assert "No results found." not in driver.page_source
driver.close()