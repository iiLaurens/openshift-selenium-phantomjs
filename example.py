import os
from PhantomJSpatched.webdriver import WebDriver as PhantomJS
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def PhantomJS_example():
    # First of all, it is recommended to explicitly state the executable_path, as not to depend on Openshift's PATH.
    #
    # Please keep the log somewhere in the Openshift data directory, or else be prepared to get a permissions error.
    #
    # Include in the port argument the IP assigned to the Python cartridge in combination with an port in the upper
    # range (> 15000) to be safe.
    #
    # Finally, you might want to ignore SSL errors or change the SSL protocol to prevent errors when visiting HTTPS pages.
    driver = PhantomJS(ip=os.environ['OPENSHIFT_PYTHON_IP'],service_args=['--ignore-ssl-errors=true'])

    driver.get("https://duckduckgo.com/")
    driver.find_element_by_id('search_form_input_homepage').send_keys("realpython")
    driver.find_element_by_id("search_button_homepage").click()
    url = driver.current_url
    driver.quit()
    return url