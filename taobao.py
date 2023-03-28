import random
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Edge('msedgedriver.exe')
driver.maximize_window()

driver.get("https://www.1688.com/")
sleep(random.randint(5, 10))

pre_height = driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
count = 1
while True:
    print('-----scroll: {} times-----'.format(count))

    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    sleep(3)
    new_height = driver.execute_script('return document.body.scrollHeight')

    print('new_height: {}\npre_height: {}'.format(new_height, pre_height))

    if new_height == pre_height:
        print("While loop Done!!!")
        break

    count += 1
    pre_height = new_height

# elem_body = driver.find_element(By.TAG_NAME ,"body")
# count = 1
# while True:
#     print(count)
#     elem_body.send_keys(Keys.PAGE_DOWN)
#     sleep(3)
#     count+=1

elems_offers = driver.find_elements(By.CLASS_NAME, "grid.rec-offer")
len(elems_offers)

elems_img = driver.find_elements(By.CLASS_NAME, "grid.rec-offer .custom.offer-image")
elems_link = driver.find_elements(By.CLASS_NAME, "grid.rec-offer .link")
elems_title = driver.find_elements(By.CLASS_NAME, "grid.rec-offer .offer-info .inline-block.offer_titles")
elems_benefit = driver.find_elements(By.CLASS_NAME, "grid.rec-offer .offer-info .clear.benefit-tags")

titles = [i.text for i in elems_title]
benefits = [i.text for i in elems_benefit]
imgs = [elem.get_attribute('src') for elem in elems_img]
links = [elem.get_attribute('href') for elem in elems_link]

list_titles = []
for offer in elems_offers[:5]:
    print(offer)
    driver.switch_to.window(driver.window_handles[0])
    offer.click()
    sleep(6)
    driver.switch_to.window(driver.window_handles[1])
    elems_titletext = driver.find_element(By.CLASS_NAME, "title-text")
    list_titles.append(elems_titletext.text)
    driver.close()

driver.switch_to.window(driver.window_handles[0])
driver.close()
