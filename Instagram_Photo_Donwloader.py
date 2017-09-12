# -*- coding: utf-8 -*-

from selenium       import webdriver
from getpass        import getpass
from urllib.request import urlretrieve
from time           import sleep
from colorama       import init, deinit, Fore
from termcolor      import colored, cprint

import os
import json

print_red       = lambda x, y="\n" : cprint(x, "red", end=y)
print_green     = lambda x, y="\n" : cprint(x, "green", end=y)
print_magenta   = lambda x, y="\n" : cprint(x, "magenta", end=y)
print_yellow    = lambda x, y="\n" : cprint(x, "yellow", end=y)
print_cyan      = lambda x, y="\n" : cprint(x, "cyan", end=y)


def create_config_if_not_exist():
    if not os.path.isfile("config.json"):
        try:
            data = {"username" : "", "password" : "", "path" : "pictures"}
            text = json.dumps(data)
            with open("config.json", "w") as file:
                file.write(text)
        except:
            print_red("Config file could not be created!")
            print_yellow("Try run this script as root.")
            return

def header():
    print()
    print_magenta("----------------------------------", "\n\n")
    print_magenta("### Instagram Photo Downloader ###", "\n\n")
    print_magenta("----------------------------------")
    print()

def read_json():
    if not os.path.isfile("config.json"):
        return False, null
    else:
        try:
            with open("config.json") as data_file:
                data = json.load(data_file)
            return True, data
        except:
            return False, null

def get_username():
    config = read_json()
    if os.path.isfile("config.json") and config[0]:
        if config[1]["username"] != "":
            return config[1]["username"]
        else:
            return input("Username : ")
    else:
        return input("Username : ")

def get_password():
    config = read_json()
    if os.path.isfile("config.json") and config[0]:
        if config[1]["password"] != "":
            return config[1]["password"]
        else:
            return getpass("Password : ")
    else:
        return getpass("Password : ")

def get_path():
    config = read_json()
    if os.path.isfile("config.json") and config[0]:
        if config[1]["path"] != "":
            return config[1]["path"]
        else:
            return "pictures"
    else:
        return "pictures"

def choose_driver():
    while True:
        print_cyan("CHOOSE DRIVER : [1]PhantomJS [2]Chrome")
        d_choice = input("Driver : ")

        if d_choice == "1":
            driver = webdriver.PhantomJS()
            break
        elif d_choice == "2":
            driver = webdriver.Chrome()
            break 
    return driver
    
def line():
    print_magenta("-----------------")
    
def signing_in(driver):
    while True:
        username = get_username()
        password = get_password()
        
        driver.get("https://www.instagram.com/")
        try:
            driver.find_element_by_class_name("_b93kq").click()
        except:
            pass
        
        driver.find_element_by_name("username").send_keys(username)
        driver.find_element_by_name("password").send_keys(password)
        driver.find_element_by_tag_name("button").click()
        
        sleep(4)
        try:
            driver.find_element_by_name("verificationCode")
            print_green("Username and password are correct!")
            line()
            verification = True
            break
        except:
            pass
        
        try:
            driver.find_element_by_class_name("coreSpriteSearchIcon")
            print_green("Username and password are correct!")
            line()
            verification = False
            break
        except:
            pass
    
        print_red("Your username or password is wrong. Try again!")
        line()
    
    while verification:
        try :
            code = input("The code, sent to your phone by Instagram : ")
            driver.find_element_by_name("verificationCode").clear()
            driver.find_element_by_name("verificationCode").send_keys(code)
            driver.find_element_by_tag_name("button").click()
            
            sleep(5)
            driver.find_element_by_class_name("coreSpriteSearchIcon")
            print_green("Login is successful.")
            break
        except :
            print_red("Your code is wrong. Try again!")
            line()
  
def find_photos(driver):
    username = input("Username for Photos : ")
    driver.get("https://www.instagram.com/" + username)
    
    print_green("Getting user...")
    print_green("Listing photos...")
    page = round(int(driver.find_element_by_class_name("_fd86t").text) / 10) + 5
    try:
        driver.find_element_by_class_name("_1cr2e").click()
    except:
        pass
    sleep(1)
    for k in range(1, page):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(0.5)
        
    print_green("Collection photos...")
    imgList = driver.find_elements_by_css_selector("._f2mse a")
    imgLinks = []
    for img in imgList:
        imgLinks.append(img.get_property("href"))
    
    print_cyan("# " + str(len(imgList)) + " #", "")
    print_green(" photos found.")
    return imgLinks, username

def create_folder(folderName):
    if not os.path.exists(folderName):
        os.makedirs(folderName)
        print_green("User folder created!")
    else:
        print_yellow("User folder already exists!")
    
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
                print_red("Input cannot be negative!")
        except:
            print_red("Please give number!")
        line()
    
    print_green("Download process started!")
    
    for idx, link in enumerate(imgLinks):
        # Get Picture URL
        driver.get(link)
        tag = driver.find_element_by_css_selector('meta[property="og:image"]')
        img_link = tag.get_property("content")
        
        # Create Name
        s = img_link.split("/")
        name = s[-1]
        
        # Download photos
        if not os.path.isfile(folderName + "/" + name):
            urlretrieve(img_link, folderName + "/" + name)
        
        # Info
        if idx % 5 == 0:
            print_green(str(idx) + " / " + str(last) + " photos downloaded...")
            
        # Max photo check
        if idx == last - 1:
            break
            
    print_green("Photos ( " + str(last) + " ) downloaded!")

def core():
    create_config_if_not_exist()
    init()
    
    header()
    
    driver = choose_driver()
    line()
    
    signing_in(driver)
    
    while True :
        imgLinks, username = find_photos(driver)
        line()
        
        path = get_path() + "/" + username
        create_folder(path)
        line()
        
        download_photos(driver, imgLinks, path)
        line()
        
        ans = input("Use again(y/N)? : ")
        line()
        if not ans == "y":
            break
    
    input("Press any key to exit")
    driver.close()
    deinit()
    print("Closed.")
    
if __name__ == "__main__":
    core()