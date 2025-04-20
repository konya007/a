from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver

service = Service(".venv/chromedriver.exe")
driver = WebDriver(service=service)

driver.get("https://www.google.com/")