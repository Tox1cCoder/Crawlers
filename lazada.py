import random
from time import sleep

import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

browser = webbrowser.Edge("./msedgedriver.exe")

driver.get("https://www.lazada.vn/dien-thoai-di-dong/?page=1&spm=a2o4n.home.cate_1.1.19053bdcDsT4Jk")
sleep(random.randint(5, 10))

elems = driver.find_elements(By.CSS_SELECTOR, ".RfADt [href]")
title = [elem.text for elem in elems]
links = [elem.get_attribute("href") for elem in elems]

elems_price = driver.find_elements(By.CSS_SELECTOR, ".aBrP0")
price = [elem.text for elem in elems_price]

df1 = pd.DataFrame(list(zip(title, price, links)), columns=['tile', 'price', 'link_item'])
df1['index_'] = np.arange(1, len(df1) + 1)

elems_discountPercent = driver.find_elements(By.CSS_SELECTOR, ".WNoq3 .IcOsH")
discountPercent = [elem.text for elem in elems_discountPercent]

discount_idx, discount_percent_list = [], []
for i in range(1, len(title) + 1):
    try:
        discount_percent = driver.find_element("xpath",
                                               "/html/body/div[3]/div/div[3]/div[1]/div/div[1]/div[2]/div[{}]/div/div/div[2]/div[4]/span".format(
                                                   i))
        discount_percent_list.append(discount_percent.text)
        discount_idx.append(int(i))
        print(i)
    except NoSuchElementException:
        print("No such element exception " + str(i))

df2 = pd.DataFrame(list(zip(discount_idx, discount_percent_list)), columns=['discount_idx', 'discount_percent'])
df3 = df1.merge(df2, how='left', left_on='index_', right_on='discount_idx')

elems_countReviews = driver.find_elements(By.CSS_SELECTOR, "._6uN7R")
countReviews = [elem.text for elem in elems_countReviews]

df3['countReviews'] = countReviews
df3 = df3.drop(['index_', 'discount_idx'], axis=1)

df3.to_csv("./csv/lazada.csv", index=False)

driver.close()
