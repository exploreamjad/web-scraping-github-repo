import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

web = "https://debank.com/token/ftm/ftm/overview"

path = '/home/neo/tests/venv/bin/chromedriver/chromedriver'
service = Service(executable_path=path)  # selenium 4
driver = webdriver.Chrome(service=service)  # define 'driver' variable
# open Google Chrome with chromedriver
driver.get(web)
driver.maximize_window()
time.sleep(5)

# Pagination
page = True
pagination = driver.find_element(By.XPATH,'//ul[contains(@class,"db-talbe-pagination mini")]')
pages = pagination.find_elements(By.XPATH, 'li')
last_page = int(pages[-3].text)
print(last_page)


# last_page = int(pages[-3].text)
# print(last_page)
# next_ = pagination.find_element(By.XPATH, './/li[@ title="Next Page"]')
# status = next_.get_attribute('aria-disabled')

user = []
token_balance = []
net_worth = []
tvf_followers = []
current_page = 1
while current_page <= last_page:
    time.sleep(5)
    container = driver.find_element(By.CLASS_NAME, 'db-table-body')
    products = container.find_elements(By.XPATH, './/div[contains(@class, "db-table-wrappedRow")]')

    for product in products:
        user.append(product.find_element(By.XPATH, './/div[@class="db-user-name is-web3"]').text)
        token_balance.append(product.find_element(By.XPATH, './/div[@class="db-table-cell"][2]').text.replace('\n', '/'))
        net_worth.append(product.find_element(By.XPATH, './/div[@class="db-table-cell"][3]').text.replace('\n', '/'))
        tvf_followers.append(product.find_element(By.XPATH, './/div[@class="db-table-cell"][4]').text.replace('\n', '/'))
    current_page = current_page + 1
    next_page = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, './/li[@ title="Next Page"]'))
    )
    next_page.click()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//ul[contains(@class,"db-talbe-pagination mini")]'))
      )


    # next_button = pagination.find_element(By.XPATH, './/li[@ title="Next Page"]')
    #
    # if next_button.is_enabled():
    #     next_button.click()
    #     # Wait for the next page to load
    #     #WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//title")))
    # else:
    #     page = False

    # next_ = pagination.find_element(By.XPATH, './/li[@ title="Next Page"]')
    # status = next_.get_attribute('aria-disabled')
    # print(status)
    # if status == 'true':
    #     page = False


driver.quit()
#Storing the data into a DataFrame and exporting to a csv file
df_books = pd.DataFrame({'user': user, 'token balance': token_balance, 'net worth': net_worth, 'tvf / followers': tvf_followers})
df_books.to_csv('dbank.csv', index=False)
