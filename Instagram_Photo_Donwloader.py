# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from getpass import getpass
from urllib.request import urlretrieve
from time import sleep
import os
    
def choose_driver():
    while True:
        print("GET DRIVER : [1]PhantomJS [2]Chrome")
        d_choice = input("Driver : ")

        if d_choice == "1":
            driver = webdriver.PhantomJS()
            break
        elif d_choice == "2":
            driver = webdriver.Chrome()
            break 
    return driver
    
def line():
    print("-----------------")
    
def signing_in(driver):
    while True:
        username = input("Username : ")
        password = getpass("Password : ")
        
        driver.get("https://www.instagram.com/")
        driver.find_element_by_class_name("_b93kq").click()
        
        driver.find_element_by_name("username").send_keys(username)
        driver.find_element_by_name("password").send_keys(password)
        driver.find_element_by_tag_name("button").click()
        
        sleep(4)
        try:
            driver.find_element_by_name("verificationCode")
            print("Username and password are correct!")
            line()
            verification = True
            break
        except:
            pass
        
        try:
            driver.find_element_by_class_name("coreSpriteSearchIcon")
            print("Username and password are correct!")
            line()
            verification = False
            break
        except:
            pass
    
        print("Your username or password is wrong. Try again!")
        line()
    
    while verification:
        try :
            code = input("The code, sent to your phone by Instagram : ")
            driver.find_element_by_name("verificationCode").clear()
            driver.find_element_by_name("verificationCode").send_keys(code)
            driver.find_element_by_tag_name("button").click()
            
            sleep(5)
            driver.find_element_by_class_name("coreSpriteSearchIcon")
            print("Login is successful.")
            break
        except :
            print("Your code is wrong. Try again!")
            line()
  
def find_photos(driver):
    username = input("Username for Photos : ")
    driver.get("https://www.instagram.com/" + username)
    
    print("Listing photos...")
    page = round(int(driver.find_element_by_class_name("_fd86t").text) / 10) + 5
    try:
        driver.find_element_by_class_name("_1cr2e").click()
    except:
        print("This user has less then 12 photos!")
    sleep(1)
    for k in range(1, page):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(0.5)
        
    print("Collection photos...")
    imgList = driver.find_elements_by_css_selector("._f2mse a")
    imgLinks = []
    for img in imgList:
        imgLinks.append(img.get_property("href"))
    
    print("#", str(len(imgList)),"#", "photos found.")
    return imgLinks, username

def create_folder(folderName):
    if not os.path.exists("pictures"):
        os.makedirs("pictures")
    
    if not os.path.exists("pictures/" + folderName):
        os.makedirs("pictures/" + folderName)
        print("User folder created!")
    else:
        print("User folder already exists!")
    
def download_photos(driver, imgLinks, folderName):
    total = len(imgLinks)
    
    while True:
        print("How many photos do you want to download?")
        lastStr = input("(For all photos, give 0) : ")
        try:
            last = int(lastStr)
            if last > 0:
                break
            elif last == 0:
                last = total
                break
            else:
                print("Input cannot be negative!")
        except:
            print("Please give number!")
        line()
    
    print("Download process started!")
    
    for idx, link in enumerate(imgLinks):
        # Get Picture URL
        driver.get(link)
        tag = driver.find_element_by_css_selector('meta[property="og:image"]')
        img_link = tag.get_property("content")
        
        # Create Name
        s = img_link.split("/")
        name = s[-1]
        
        # Download photos
        if not os.path.isfile("pictures/" + folderName + "/" + name):
            urlretrieve(img_link, "pictures/" + folderName + "/" + name)
        
        # Info
        if idx % 5 == 0:
            print(str(idx),"/", str(last), "photos downloaded...")
            
        # Max photo check
        if idx == last - 1:
            break
            
    print("Photos (", str(last), ") downloaded!")

def core():
    print("Instagram Photo Downloader")
    print("--------------------------")
    
    driver = choose_driver() 
    line()
    
    signing_in(driver)
    line()
    
    while True :
        imgLinks, username = find_photos(driver)
        line()
        
        create_folder(username)
        line()
        
        download_photos(driver, imgLinks, username)
        line()
        
        ans = input("Use again(y/N)? : ")
        line()
        if not ans == "y":
            break
    
    input("Press any key to exit")
    driver.close()
    print("Closed.")
    
if __name__ == "__main__":
    core()
    
    
    
    