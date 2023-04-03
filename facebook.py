import os
import pickle
from time import sleep

import pandas as pd
from selenium import webdriver


def initDriver():
    driver = webdriver.Edge(executable_path="./msedgedriver.exe")
    return driver


def loginFacebook(driver, username, password):
    driver.get("https://facebook.com/")

    # textUserName = driver.find_element(By.ID, "email")
    # textUserName.send_keys(username)
    #
    # textPassword = driver.find_element(By.ID, "pass")
    # textPassword.send_keys(password)
    #
    # loginButton = driver.find_element(By.NAME, "login")
    # loginButton.click()
    #
    # sleep(10)
    #
    # pickle.dump(driver.get_cookies(), open("my_cookie.pkl", "wb"))

    cookies = pickle.load(open("my_cookie.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)

    driver.get("https://facebook.com/")


def readData(fileName):
    f = open(fileName, 'r', encoding='utf-8')
    data = []
    for i, line in enumerate(f):
        line = repr(line)
        line = line[1:len(line) - 3]
        data.append(line)
    return data


def writeFile(fileName, content):
    with open(fileName, 'a', encoding='utf-8') as f:
        f.write(content + os.linesep)


def getContentComment(driver):
    list_comments_of_a_post = []
    links = driver.find_elements_by_xpath('//a[contains(@href, "comment/replies")]')
    ids = []
    if (len(links)):
        for link in links:
            takeLink = link.get_attribute('href').split('ctoken=')[1].split('&')[0]
            textCommentElement = driver.find_element_by_xpath(
                ('//*[@id="' + takeLink.split('_')[1] + '"]/div/div[1]'))
            if (takeLink not in ids):
                list_comments_of_a_post.append(textCommentElement.text)
                ids.append(takeLink)
    return ids, list_comments_of_a_post


def getAmountOfComments(driver, postId, numberCommentTake, list_comments):
    driver.get("https://mbasic.facebook.com/" + str(postId))
    sumLinks, list_comments_of_a_post = getContentComment(driver)
    list_comments.append(list_comments_of_a_post)
    while (len(sumLinks) < numberCommentTake):
        nextBtn = driver.find_elements_by_xpath('//*[contains(@id,"see_next")]/a')
        if (len(nextBtn)):
            nextBtn[0].click()
            sumLinks_more, list_comments_of_a_post_more = getContentComment(driver)
            list_comments.append(list_comments_of_a_post_more)
            sumLinks.extend(sumLinks_more)
        else:
            break

    return list_comments


def getPostIds(driver, filePath='posts.csv'):
    allPosts = readData(filePath)
    sleep(2)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    shareBtn = driver.find_elements_by_xpath('//a[contains(@href, "/sharer.php")]')
    if (len(shareBtn)):
        for link in shareBtn:
            postId = link.get_attribute('href').split('sid=')[1].split('&')[0]
            if postId not in allPosts:
                writeFile(filePath, postId)


def getnumOfPostFanpage(driver, pageId, amount, filePath='posts.csv'):
    driver.get("https://touch.facebook.com/" + pageId)
    while len(readData(filePath)) < amount * 2:
        getPostIds(driver, filePath)


list_comments = []
driver = initDriver()

loginFacebook(driver, "cs232khcl@gmail.com", "definitelynotapassword")
getnumOfPostFanpage(driver, "/UIT.Fanpage", 10, './csv/posts.csv')

for postId in readData('./csv/posts.csv'):
    list_comments.append(getAmountOfComments(driver, postId, 10, list_comments))

data = {'List Comments': list_comments}
pd.DataFrame(data).to_csv('./csv/comments.csv')
