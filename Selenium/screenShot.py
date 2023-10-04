from selenium import webdriver

import chromedriver_autoinstaller
chromedriver_autoinstaller.install()
driver = webdriver.Chrome()

driver.get("https://www.delftstack.com/")
driver.save_screenshot("filename.png")