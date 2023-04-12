import os
from time import sleep

import pandas as pd
from selenium import webdriver

driver = webdriver.Edge("./msedgedriver.exe")
author_name = str(input("Please provide the author's name: "))
url = f"https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q={author_name}&btnG="
driver.get(url)
sleep(3)

profile_xpath = """//*[@id="gs_res_ccl_mid"]/div[1]/table/tbody/tr/td[2]/h4/a"""
profile = driver.find_element_by_xpath(profile_xpath)
profile.click()

while True:
    try:
        show_more = driver.find_element_by_css_selector("#gsc_bpf_more")
        show_more.click()
        time.sleep(3)
    except Exception as e:
        break

sleep(3)

title_list = []
author_list = []
cite_list = []
year_list = []

papers_list = driver.find_elements_by_css_selector('.gsc_a_tr')

for paper in papers_list:
    title = paper.find_element_by_css_selector('.gsc_a_at')
    author = paper.find_element_by_css_selector('.gs_gray')
    cite = paper.find_element_by_css_selector('.gsc_a_ac.gs_ibl')
    year = paper.find_element_by_css_selector('.gsc_a_h.gsc_a_hc.gs_ibl')

    title_list.append(title.text)
    author_list.append(author.text)
    cite_list.append(cite.text)
    year_list.append(year.text)

data = {'Title': title_list, 'Authors': author_list, 'Cited by': cite_list, 'Year': year_list}

path = "csv"
exist = os.path.exists(path)
if not exist:
    os.makedirs(path)

pd.DataFrame(data).to_csv('./csv/paper.csv')

driver.close()
