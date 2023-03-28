from time import sleep

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Edge("./msedgedriver.exe")
url = "https://scholar.google.com/citations?hl=en&user=p3vHDZYAAAAJ"
driver.get(url)
sleep(3)

while True:
    try:
        show_more = driver.find_element(By.CSS_SELECTOR, "#gsc_bpf_more")
        show_more.click()
        time.sleep(3)
    except Exception as e:
        break

sleep(3)

title_list = []
author_list = []
cite_list = []
year_list = []

papers_list = driver.find_elements(By.CSS_SELECTOR, '.gsc_a_tr')

for paper in papers_list:
    title = paper.find_element(By.CSS_SELECTOR, '.gsc_a_at')
    author = paper.find_element(By.CSS_SELECTOR, '.gs_gray')
    cite = paper.find_element(By.CSS_SELECTOR, '.gsc_a_ac.gs_ibl')
    year = paper.find_element(By.CSS_SELECTOR, '.gsc_a_h.gsc_a_hc.gs_ibl')

    title_list.append(title.text)
    author_list.append(author.text)
    cite_list.append(cite.text)
    year_list.append(year.text)

data = {'Title': title_list, 'Authors': author_list, 'Cited by': cite_list, 'Year': year_list}

pd.DataFrame(data).to_csv('./csv/paper.csv')

driver.close()
