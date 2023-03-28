from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def initDriver():
    options = Options()

    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    browser = webdriver.Chrome(executable_path="./chromedriver.exe", chrome_options=options)
    return browser


driver = initDriver()
url = "https://images.google.com/"
driver.get()

# Find search input
search_input = driver.find_element(by=By.XPATH, value='//*[@id="sbtc"]/div/div[2]/input')

# Type information which we want to search
info = 'cat'
search_input.send_keys(info)

search_input.send_keys(Keys.ENTER)

src_images = []
path = 'D:\\Hoc_ky_6\\Tinh_Toan_Da_Phuong_Tien\\image\\'

for i in range(1, 10):
    try:
        img = browser.find_element(by=By.XPATH, value='//*[@id="islrg"]/div[1]/div[' + str(i) + ']/a[1]/div[1]/img')
        src_images.append(img.get_attribute("src"))
        sleep(0.5)
    except:
        continue

sleep(120)

browser.close()
