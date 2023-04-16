
    
        
    
    


from configparser import ConfigParser
import datetime
from time import sleep
configfile = ConfigParser()
from selenium import webdriver
from selenium.webdriver.remote.remote_connection import LOGGER, logging
LOGGER.setLevel(logging.CRITICAL)
import time
import random
import traceback
import sys

# class By:
#     """Set of supported locator strategies."""

#     ID = "id"
#     XPATH = "xpath"
#     LINK_TEXT = "link text"
#     PARTIAL_LINK_TEXT = "partial link text"
#     NAME = "name"
#     TAG_NAME = "tag name"
#     CLASS_NAME = "class name"
#     CSS_SELECTOR = "css selector"
global CONFIG_DICT
URL_LOGIN = "https://app.propertime.co.il/Default.aspx"
def set_up_driver():
    driver = webdriver.Edge()
    return driver


def sign_in(driver : webdriver.Edge, username : str, password : str):
    driver.get(URL_LOGIN)
    sleep(1)
    username_value = "ctl00$Content2$txtUsername"
    password_value = "ctl00$Content2$txtPassword"
    driver.find_element("name", username_value).send_keys(username) #(username_value).send_keys(username)
    driver.find_element("name", password_value).send_keys(password)
    driver.find_element('id', "ctl00_Content2_btnEntry").click()


def punch_in(driver : webdriver.Edge):
    driver.get(URL_LOGIN)
    sleep(1)
    driver.find_element("id", "punchInNow").click()

def punch_out(driver : webdriver.Edge):
    # driver.get(URL_LOGIN)
    sleep(1)
    driver.find_element("id", "punchOutNow").click()

def add_raw(driver : webdriver.Edge):
    print("add raw")
    driver.get(URL_LOGIN)
    add_row = None
    save_changes = None
    try:
        # retriev buttons add row and save
        for item in driver.find_elements("tag name", "input"):
            if item.accessible_name == "Add row":
                sleep(1)
                add_row = item
            if item.accessible_name == "Save":
                sleep(1)
                save_changes = item

        # click add row
        add_row.click()
    except Exception as e:
        print("error in add raw click")
        print(e)
        print(traceback.format_exc())
        return
        


    # click on drop down menu
    try:
        sleep(0.5)
        driver.find_elements("class name", "chosen-single")[1].click()
    except Exception as e:
        print("error in click on drop down menu")
        print(e)
        print(traceback.format_exc())
        return
   

    # select project 79275
    try:
        sleep(0.5)
        for item in driver.find_elements("xpath", "//li"):
            if item.text == "79275":
                sleep(0.5)
                item.click()
                break
    except Exception as e:
        print("error in select project 79275")
        print(e)
        print(traceback.format_exc())
        return
   

    try:
        sleep(0.5)
        t = driver.find_elements("class name", "clockImage")
        t[1].click()
        sleep(0.5)
        save_changes.click()
    except Exception as e:
        print("error in click on clock")
        print(e)
        print(traceback.format_exc())
        return
    print("raw added")

def sign_out(driver : webdriver.Edge):
    driver.get(URL_LOGIN)
    sleep(0.5)
    print("sign out")
    driver.find_element("id", "ctl00_Content1_mnuLogout").click()


def punch_all_in():
    # configfile.read("./config.ini")
    driver = None
    for section in CONFIG_DICT.values():
        try:
            # username = str(dict(configfile.items(section))["username"])
            # password = str(dict(configfile.items(section))["password"])
            # print(f"Punching in {section.title()} : {username}")
            username = str(section["username"])
            password = str(section["password"])
            title = str(section["name"])
            skip_days_list = section["skip_days_list"]
            print(f"Punching in {title} : {username}")
            date_today_in_month = time.localtime().tm_mday
            if date_today_in_month in skip_days_list:
                print(f"Skipping {title}")
                continue
            if driver == None:
                driver = set_up_driver()
            sign_in(driver, username, password)
            punch_in(driver)
            sign_out(driver)
            sleep_time = random.randrange(60, 300)
            print(f"Finihsed punching in {title} : {username}")
            print(f"sleeping for {sleep_time} seconds")
            sleep(sleep_time) # sleep between 1 and 5 minutes
        except Exception as e:
            print(f"Error while punching in {title} : {username}")
            print(e)
    if driver != None:
        driver.close()

def punch_all_out():

    # configfile.read("./config.ini")
    driver = None
    for section in CONFIG_DICT.values():
        try:
            username = str(section["username"])
            password = str(section["password"])
            title = str(section["name"])
            skip_days_list = section["skip_days_list"]
            print(f"Punching out {title} : {username}")
            date_today_in_month = time.localtime().tm_mday
            if date_today_in_month in skip_days_list:
                print(f"Skipping {title}")
                continue


            
            if driver == None:
                driver = set_up_driver()
            sign_in(driver, username, password)
            add_raw(driver)
            punch_out(driver)
            sign_out(driver)
            sleep_time = random.randrange(60, 300)
            print(f"Finihsed punching out {title} : {username}")
            print(f"sleeping for {sleep_time} seconds")
            sleep(sleep_time) # sleep between 1 and 5 minutes
        except Exception as e:
            print(f"Error while punching out {title} : {username}")
            print(traceback.format_exc())
            print(e)
    if driver != None:
        driver.close()

def delete_last_line():
    "Use this function to delete the last line in the STDOUT"

    #cursor up one line
    sys.stdout.write('\x1b[1A')

    #delete last line
    sys.stdout.write('\x1b[2K')

def sleep_until_morning(start_sleep, stop_time):

    current_time = time.localtime()
    # 8 >= start_sleep or 8 < stop_time
    while current_time.tm_hour >= start_sleep or current_time.tm_hour < stop_time:
        time_str ="Time: " + time.strftime('%a, %d-%m-%y %H:%M:%S',time.localtime())
        print(time_str, end="", flush=True)
        sleep(1)
        for _ in range(len(time_str)):
            print('\b', end = '')
        current_time = time.localtime()


def sleep_from_start_to_end(start_sleep, stop_time):

    current_time = time.localtime()
    # 18 >= start_sleep and 18 < stop_time
    while current_time >= start_sleep and current_time <= stop_time:
        time_str ="Time: " + time.strftime('%a, %d-%m-%y %H:%M:%S',time.localtime())
        print(time_str, end="", flush=True)
        sleep(1)
        for _ in range(len(time_str)):
            print('\b', end = '')
        current_time = time.localtime()
    
    



def punch_all_day():
    print("Starting to punch all day")
    global CONFIG_DICT
    
    
    need_punch_in = True
    need_punch_out = False
    while True:
        try:

            
            now_is = time.localtime()
            # if its fryday or saturday sleep until sunday monday its 0
            if now_is.tm_wday == 4 or now_is.tm_wday == 5:
                print("Its weekend, sleep until sunday")
                while now_is.tm_wday != 6 or now_is.tm_hour < 8: # sunday is 6
                    sleep(600)
                    now_is = time.localtime()
                sleep(300)
                print("Its sunday, continue")

            
            if need_punch_in and now_is.tm_hour >= 8 and now_is.tm_hour <= 10:
                CONFIG_DICT = read_config_json() # update the punch list
                print("*"*50)
                print("Starting to punch all IN")
                punch_all_in()
                need_punch_in = False
                need_punch_out = True
                checkout_not_early_than = time.localtime(32400 + int(datetime.datetime.now().timestamp()))
                print(f"Finnish to punch all IN. next punching time is {time.strftime('%a, %d-%m-%y %H:%M:%S', checkout_not_early_than)}")
                print("*"*50)
                sleep_from_start_to_end(now_is, checkout_not_early_than)
            if need_punch_out and now_is >= checkout_not_early_than and now_is.tm_hour <= 19:
                print("*"*50)
                print("Starting to punch all OUT")
                punch_all_out()
                need_punch_out = False
                need_punch_in = True
                print(f"Finnish to punch all OUT. See you tomorrow at 8:00 AM")
                print("*"*50)
                # tommorow_at_8 = time.localtime(32400 + int(datetime.datetime.now().timestamp()) + 86400)
                sleep_until_morning(now_is.tm_hour, 8)

            
                # exit()
            if need_punch_out:
                print("Sleep until checkout time")
                sleep_from_start_to_end(now_is, checkout_not_early_than)

            if need_punch_in:
                print("Sleep until 8:00 AM")
                sleep_until_morning(now_is.tm_hour, 8)
                time.sleep(random.randrange(300, 1800))
                
            
            # print(f"Idle... {time.strftime('%a, %d-%m-%y %H:%M:%S',time.localtime())}")
            
            # time.sleep(random.randrange(300, 1200)) 
            
        except Exception as ex:
            print(traceback.format_exc())
            print(ex)

def shuffle_dict(dic):
    from random import shuffle
    values = list(dic.items())
    shuffle(values)

    new_dic = {}
    for items in values:
        new_dic[items[0]] = items[1]
    
    return new_dic

def read_config_json():
    import json
    with open("config.json") as json_file:
        config = json.load(json_file)

    dic = {}
    for item in config:
        dic[item["username"]] = item

    return shuffle_dict(dic)


if __name__ == "__main__":
    CONFIG_DICT = read_config_json()
    # time.strftime("%a, %d-%m-%y %H:%M:%S", time_now)
    
    
    
    # punch_all_out()
    
    
    punch_all_day()
    
            
    
        
    
    
    