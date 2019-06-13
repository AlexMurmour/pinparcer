import requests
from selenium import webdriver
from time import sleep
import parcerpinS
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException


driver = webdriver.Firefox()


def login():
    driver.get('https://www.pinterest.ru/')
    sleep(1)
    username = driver.find_element_by_id('email')
    username.send_keys(parcerpinS.username)
    password = driver.find_element_by_id('password')
    password.send_keys(parcerpinS.password)
    password.send_keys(Keys.RETURN)
    sleep(3)


def create_pic_list():
    global urls
    driver.get('https://www.pinterest.ru/pin/232709505727139314/')
    sleep(2)
    pic_hrefs = []
    for i in range(1, 20):
        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(1)
            hrefs_in_view= driver.find_elements_by_tag_name('a')
            # finding relevant hrefs
            hrefs_in_view = [unit.get_attribute('href') for unit in hrefs_in_view
                             if '/pin/' in unit.get_attribute('href')]
            [pic_hrefs.append(href) for href in hrefs_in_view if href not in pic_hrefs]
            # print("Check: pic href length " + str(len(pic_hrefs)))
        except Exception:
            continue
    urls = pic_hrefs[1:]
    return urls



def get_name(pic_href):
    name = pic_href.split('/')[-1]
    return name



def find_load():
    x = driver.find_elements_by_class_name("_u3._45._y6._4h")
    pic = []
    global picture
    for i in x:
        k = i.get_attribute('src')
        pic.append(k)
    picture = pic[1]
    sleep(0.5)

def load():
    q = requests.get(picture, stream=True)
    with open("C:\\Users\\Alexandra\\PycharmProjects\\instagramlike\\picture\\photo\\" + get_name(picture), 'wb') as f:
        sleep(1)
        for chunk in q.iter_content(chunk_size=10000):
            sleep(0.5)
            f.write(chunk)
    return picture

def de():
    login()
    sleep(1)
    create_pic_list()
    for url in urls:
        try:
            driver.get(url)
            sleep(2)
        except Exception:
            sleep(10)
        try:
            find_load()
            sleep(1)
            load()
        except StaleElementReferenceException:
            pass



if __name__ == '__main__':
    de()

