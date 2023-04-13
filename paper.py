import os
from time import sleep

import pandas as pd
from selenium import webdriver

driver = webdriver.Edge("./msedgedriver.exe")
author_name = str(input("Please provide the author's name: "))
url = f"https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q={author_name}&btnG="
driver.get(url)
sleep(2)

_ = input("Please input after captcha... ")

profile_xpath = """//*[@id="gs_res_ccl_mid"]/div[1]/table/tbody/tr/td[2]/h4/a"""
profile = driver.find_element_by_xpath(profile_xpath)
profile.click()
sleep(2)


def showMore():
    while True:
        try:
            show_more = driver.find_element_by_css_selector("#gsc_bpf_more")
            show_more.click()
            time.sleep(2)
        except Exception as e:
            break


titles = []
articles = []
authors = []
cited_by = []
years = []

showMore()
sleep(3)
papers = driver.find_elements_by_css_selector('.gsc_a_tr')

print(f"There are {len(papers)} papers.")

for id, paper in enumerate(papers, start=1):
    print(f"Crawling paper {id}...")
    title = driver.find_element_by_xpath(f'''//*[@id="gsc_a_b"]/tr[{id}]/td[1]/a''')
    cite = driver.find_element_by_css_selector('.gsc_a_ac.gs_ibl')
    cited_by.append(cite.text)
    title.click()
    sleep(2)

    title = driver.find_element_by_xpath('//*[@id="gsc_oci_title"]')
    elements = driver.find_elements_by_class_name('gs_scl')
    try:
        article = elements[len(elements) - 1].find_element_by_css_selector(
            'div.gsc_oci_value > div > div:nth-child(1) > a')
        articles.append(article.get_attribute('href'))
    except Exception as e:
        articles.append("")
    author = driver.find_element_by_xpath('//*[@id="gsc_oci_table"]/div[1]/div[2]')
    year = driver.find_element_by_xpath('//*[@id="gsc_oci_table"]/div[2]/div[2]')

    titles.append(title.text)

    authors.append(author.text)
    years.append(year.text)

    driver.execute_script("window.history.go(-1)")
    showMore()
    sleep(1)

data = {'Title': titles, 'Article Link': articles, 'Authors': authors, 'Cited by': cited_by, 'Year': years}

path = "csv"
exist = os.path.exists(path)
if not exist:
    os.makedirs(path)

pd.DataFrame(data).to_csv('./csv/paper.csv')

driver.close()
