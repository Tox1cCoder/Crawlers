import argparse
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

import csv

parser = argparse.ArgumentParser()
parser.add_argument('--num_article', type=int, help='number article to get crawling', default=2)
parser.add_argument('--num_commnet', type=int, help='number comment per post', default=2)
parser.add_argument('--save_file', type=str, default='csv/comment.csv')
args = vars(parser.parse_args())

driver = webdriver.Edge("./msedgedriver.exe")
url = 'https://vnexpress.net/'
driver.get(url)

page_source = BeautifulSoup(driver.page_source, features="html.parser")
element_title_articles = page_source.find_all('h3', class_="title-news")

all_title_link = []
all_title_name = []
all_comments = []

for element in element_title_articles:
    all_title_name.append(element.find('a').get('title'))
    all_title_link.append(element.find('a').get('href'))

for link in all_title_link[:min(len(all_title_link), args['num_article'])]:
    driver.get(link)
    page_source = BeautifulSoup(driver.page_source)
    time.sleep(2)

    element_comments = set()
    num_of_comment = len(element_comments)

    while num_of_comment < args['num_commnet']:
        try:
            comments = page_source.find_all('div', class_='content-comment')
            element_comments.update(comments)
        except:
            break

        try:
            btn = driver.find_element(By.ID, 'show_more_coment')
        except:
            break
        browser.execute_script("arguments[0].click();", btn)

    for cmt in list(element_comments):
        try:
            cmt_text = cmt.find('p', 'full_content')
            all_comments.append([cmt_text.text])
        except:
            cmt_text = cmt.find('p', 'content_more')
            all_comments.append([cmt_text.text])

driver.close()

header = ['Comment']
with open(args['save_file'], 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(all_comments)
