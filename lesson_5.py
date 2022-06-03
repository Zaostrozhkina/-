from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from pymongo import MongoClient
from pprint import pprint


s = Service('./chromedriver4')
options = Options()
options.add_argument('start-maximized')

driver = webdriver.Chrome(service=s)
driver.implicitly_wait(10)
driver.get('https://www.mvideo.ru')

trends = []

while True:
    try:
        button = driver.find_element(By.XPATH, "//span[contains(text(),'В тренде')]")
        button.click()
        break
    except:
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)

### Собираем ссылки

links = []

total_link = driver.find_element(By.CLASS_NAME, 'count').text
total_link = int(total_link)

for i in driver.find_elements(By.XPATH, "//div[contains(@class, 'product-mini-card__name')]//a"):
    link = i.get_attribute('href')
    links.append(link)

total_link = total_link - 1
links = links[:total_link]

### Собираем информацию о товаре из ссылок

for link in links:
    info = {}
    driver.get(link)

    name = driver.find_element(By.XPATH, "//h1[contains(@class, 'title')]").text
    price = driver.find_element(By.XPATH, "//mvid-price//span[contains(@class, 'price__main-value')]").text
    description = driver.find_element(By.XPATH, "//mvid-about-product[contains(@class, 'general__about-product')]//div[contains(@class, 'description')]").text

    info['name'] = name
    info['price'] = price
    info['description'] = description

    trends.append(info)

### Загружаем данные в БД

client = MongoClient('127.0.0.1', 27017)
db = client['all_trends']
all_trends = db.all_trends
all_trends.insert_many(trends)



