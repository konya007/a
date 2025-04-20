import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver

KEYWORD="django"

service = Service(".venv/chromedriver.exe")
driver = WebDriver(service=service)
sub_driver = WebDriver(service=service)

driver.get("https://thuvien.ou.edu.vn/")
driver.maximize_window()

search_box = driver.find_element(By.CSS_SELECTOR, "#search-global-form input")
search_btn = driver.find_element(By.CSS_SELECTOR, "#search-global-form a")
search_box.send_keys(KEYWORD)
search_btn.click()
article_books = []

def get_ISBN(driver, item):
    item.click()
    iframe = driver.find_element(By.CSS_SELECTOR, "#bookDetailModal div.modal-body > iframe")
    close_btn = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "#bookDetailModal .modal-header i"))
    )
    # close_btn = driver.find_element(By.CSS_SELECTOR, "#bookDetailModal .modal-header i")
    time.sleep(5)
    close_btn.click()
    sub_driver.get(iframe.get_attribute("src"))
    ISBN = WebDriverWait(sub_driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#tblRecordDetails > tbody > tr:nth-child(2)"))
    )
    try:
        t1 = ISBN.find_element(By.CSS_SELECTOR, "td:nth-child(1)").text
        t2 = ISBN.find_element(By.CSS_SELECTOR, "td:nth-child(2)").text
        if t1.find("ISBN") >= 0 and t2.find(":")>=0:
            return t2.split(":")[0]
    except:
        print("ERR")
    return "Không có"



while True:
    items = WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#tab1 ul li a.name-book"))
    )
    for i in items:
        obj = {
            "name": i.text,
            "ISBN":get_ISBN(driver, i)
        }
        print(f"Tên sách: {obj.get("name")}")
        print(f"ISBN: {obj.get("ISBN")}")
        article_books.append(obj)

    next_btn = driver.find_element(By.CSS_SELECTOR, ".opac_next a:last-child")
    if not next_btn.get_attribute("onclick"):
        break
    else:
        next_btn.click()
# for i, e in enumerate(article_books):
#     print(e.get("name"))
#     print(e.get("ISBN"))
print(len(article_books))
sub_driver.close()
driver.close()
input()


