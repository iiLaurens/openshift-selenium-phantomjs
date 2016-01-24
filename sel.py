import os
from selenium import webdriver

webdriver.PhantomJS(service_log_path=os.path.join(os.environ['OPENSHIFT_DATA_DIR'],'log.log'),port='127.8.80.1:17771')
#webdriver.PhantomJS(executable_path=os.path.join(os.environ['OPENSHIFT_DATA_DIR'],'phantomjs'),service_log_path=os.path.join(os.environ['OPENSHIFT_DATA_DIR'],'log.log'),port='127.8.80.1:8081')