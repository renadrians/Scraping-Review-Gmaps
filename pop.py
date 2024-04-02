from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import pandas as pd

driver = webdriver.Chrome()
url = 'https://www.google.com/maps/place/Pantai+Pandawa/@-8.8447868,115.1762472,15z/data=!4m16!1m9!3m8!1s0x2dd25b7cd8ba1f31:0x41b8785dd055b2a4!2sPantai+Pandawa!8m2!3d-8.8452802!4d115.1870679!9m1!1b1!16s%2Fg%2F1ygbcghrt!3m5!1s0x2dd25b7cd8ba1f31:0x41b8785dd055b2a4!8m2!3d-8.8452802!4d115.1870679!16s%2Fg%2F1ygbcghrt?entry=ttu'
driver.get(url)

# Wait for the element to be clickable
wait = WebDriverWait(driver, 10)
wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]/div/div/button[2]'))).click()

time.sleep(3)

# Handling popup if present
try:
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "widget-pane-link"))).click()
except:
    pass

# Find the total number of reviews
total_number_of_reviews = driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[2]/div/div[2]/div[3]').text
total_number_of_reviews = int(total_number_of_reviews.split(' ')[0].replace('.', ''))
print(total_number_of_reviews)

# Find scroll layout
scrollable_div = driver.find_element(By.CSS_SELECTOR, '#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div.m6QErb.DxyBCb.kA9KIf.dS8AEf')
review_summary = []

# Scroll as many times as necessary to load all reviews
j = 1
while len(review_summary) < 500:
    driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div)
    time.sleep(5)

    for _ in range(10):
        review_text = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[9]/div[' + str(j) + ']/div/div/div[4]/div[2]/div/span').text
        review_rate = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[9]/div[' + str(j) + ']/div/div/div[4]/div[1]/span[1]').get_attribute("aria-label")
        review_time = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[9]/div[' + str(j) + ']/div/div/div[4]/div[1]/span[2]').text

        print(review_text)
        print(review_rate)
        print(review_time)
        print('\n')

        review_summary.append([review_text, review_rate, review_time])
        j += 3

        if len(review_summary) >= 500:
            break

data_review = pd.DataFrame(review_summary, columns=['review_text', 'review_rate', 'review_time'])

# Save data to CSV
data_review.to_csv('google_maps_reviews.csv', index=False)
