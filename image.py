import os
import time

import bs4
import requests
from selenium import webdriver

folder_name = 'images'
if not os.path.isdir(folder_name):
    os.makedirs(folder_name)


def download_image(url, folder_name, num):
    reponse = requests.get(url)
    if reponse.status_code == 200:
        with open(os.path.join(folder_name, str(num) + ".jpg"), 'wb') as file:
            file.write(reponse.content)


search_query = str(input("Please provide the keyword..."))

driver = webdriver.Edge("./msedgedriver.exe")
url = f"https://www.google.com/search?q={search_query}&source=lnms&tbm=isch"
driver.get(url)

driver.execute_script("window.scrollTo(0, 0);")

page_html = driver.page_source
pageSoup = bs4.BeautifulSoup(page_html, 'html.parser')
containers = pageSoup.findAll('div', {'class': "isv-r PNCib MSM1fd BUooTd"})

len_containers = len(containers)

for i in range(1, len_containers + 1):
    if i % 25 == 0:
        continue

    xPath = f"""//*[@id="islrg"]/div[1]/div[{i}]"""

    previewImageXPath = f"""//*[@id="islrg"]/div[1]/div[{i}]/a[1]/div[1]/img"""
    previewImageElement = driver.find_element_by_xpath(previewImageXPath)
    previewImageURL = previewImageElement.get_attribute("src")

    driver.find_element_by_xpath(xPath).click()

    timeStarted = time.time()
    while True:
        imgXpath = """//*[@id="Sva75c"]/div[2]/div/div[2]/div[2]/div[2]/c-wiz/div/div[2]/div[1]/a/img[1]"""
        imageElement = driver.find_element_by_xpath(imgXpath)
        imageURL = imageElement.get_attribute('src')

        if imageURL != previewImageURL:
            break

        else:
            currentTime = time.time()

            if currentTime - timeStarted > 10:
                print("Timeout! Will download a lower resolution image and move onto the next one")
                break

    try:
        download_image(imageURL, folder_name, i)
        print("Downloaded element %s out of %s total. URL: %s" % (i, len_containers + 1, imageURL))
    except:
        print("Couldn't download an image %s, continuing downloading the next one" % (i))
