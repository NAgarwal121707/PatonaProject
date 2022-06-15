# -*- coding: utf-8 -*-
# Importing Libraries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time


# Created a class as SeleniumTemplate
class SeleniumTemplate:
    # use init method to use driver path once as common
    # Args : driver_path(path of web driver of your choice)
    def __init__(self, driver_path):
        self.driver_path = driver_path

    # if want to use chrome as browser use this
    # Args : None
    # return : chrome driver object
    def get_chrome_driver(self):
        driver = webdriver.Chrome(self.driver_path)
        return driver

    # if want to use firefox as browser use this
    # Args : None
    # return : firefox driver object
    def get_firefox_driver(self):
        driver = webdriver.Firefox(self.driver_path)
        return driver

    # Open web page in selenium driver
    # Args : driver object, website link, required time
    # return : page source of website
    def open_webpage(self, driver, web_url, sleep_time):
        driver.get(web_url)
        time.sleep(sleep_time)
        return driver.page_source

    # Close web page in selenium driver
    # Args : driver object
    # return : close open website
    def close_webpage(self, driver):
        driver.close()

    # Open web page in selenium driver and scroll to e
    # Args : driver object, website link, required time
    # return : page source of website
    def scroll_to_end(self, driver, sleep_time):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(sleep_time)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        return driver.page_source

    # Args : driver object, number of scrolls, time for wait
    # return : page source of website
    def scroll_many_till_end(self, driver, number_of_scrolls, sleep_time):
        scrolls = number_of_scrolls
        while True:
            scrolls -= 1
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(sleep_time)
            if scrolls < 0:
                break
        return driver.page_source

    # Args : driver object, time to wait, xpath to locate element
    # return : driver url after clicking
    def click_button(self, xpath, sleep_time, driver):
        try:
            button = driver.find_element_by_xpath(xpath)
            time.sleep(sleep_time)
            button.click()
            print('Clicked Button')
            # time.sleep(sleep_time)
        except:
            print('Given Xpath not found in page source')
        return driver.current_url

    # Args : driver object, put value in input part, time for wait,change input if required
    # return : return current website url
    def write_in_input_box(self, driver, xpath, sleep_time, input_value):
        try:
            variable = driver.find_element_by_xpath(xpath)
            time.sleep(sleep_time)
            variable.send_keys(input_value)
        except:
            print('Xpath not found in page source')
        return driver.current_url

    # Args : driver object, put value in input part asmuch as required, time for wait,change input if required
    # return : return current website url
    def login_website(self, driver, sleep_time, input_value1, input_value2, submit_button_xpath, xpath1,
                      xpath2):
        try:
            val1 = driver.find_element_by_xpath(xpath1)
            val1.send_keys(input_value1)
            time.sleep(1)
            val2 = driver.find_element_by_xpath(xpath2)
            val2.send_keys(input_value2)
            time.sleep(1)
            submit_button = driver.find_element_by_xpath(submit_button_xpath)
            time.sleep(3)
            submit_button.click()
            time.sleep(sleep_time)
        except:
            print('Problem in finding either xpath or input value given not correct please check')
            return driver.current_url

    def switch_to_iframe(self, driver, link, sleep_time):
        driver.get(link)
        time.sleep(10)
        iframe = driver.find_element_by_xpath('(//iframe)[1]')
        driver.switch_to.frame(iframe)
        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(sleep_time)
        return driver.page_source

    def add_option_to_chrome(self, user_option):
        options = Options()
        for u in user_option:
            options.add_argument(str(u))
        driver = webdriver.Chrome(options=options)
        return driver

    def wait_web_driver(self, driver, wait_time, xpath):
        try:
            items = WebDriverWait(driver, wait_time).until(
                EC.presence_of_element_located((By.XPATH, xpath)))
        except Exception as e:
            print('Opps!!!! error', e)
            items = e
        return items

    def find_element(self, element, xpath):
        try:
            data_found = element.find_element(By.XPATH, xpath)
        except Exception as e:
            data_found = e
            print('Opps!! Data you looking for not found. see the error', e)
        return data_found

    def amazon_rating_finder(self, item, xpath1, xpath2):

        # find product name
        path = str(xpath1) + '//h2//a'

        product_name = item.find_element(By.XPATH, path)

        # find ratings box
        ratings_box = item.find_elements(By.XPATH, xpath2)

        # find ratings and ratings_num
        if ratings_box != []:
            ratings = ratings_box[0].get_attribute('aria-label')
        else:
            ratings = 0

        return ratings, product_name

    def flipkart_url_finder(self, driver, xpath):
        url = ''
        # find product detail path
        url_path = driver.find_element(By.XPATH, xpath)
        if url_path != '':
            url = url_path.get_attribute('href')
        else:
            print('Opps!! Data you looking for not found. see the error')

        return url

    def flipkart_product_rating(self, product_page, xpath2):
        # find product name
        xpath1 = '//h1'
        product_name = product_page.find_element(By.XPATH, xpath1)
        if product_name != '':
            product_name = product_name.text
            try:
                product_name = product_name.strip().replace('\n', '')
            except:
                product_name = product_name.strip()
        else:
            product_name = 'Not Found'

        # find ratings box

        ratings_box = product_page.find_element(By.XPATH, xpath2)

        # find ratings and ratings_num
        if ratings_box != []:
            ratings = ratings_box.text.strip()
        else:
            ratings = 0

        return product_name, ratings

    def myntra_scraper(self, product_page, xpath1):

        # find ratings box
        try:
            ratings_box = product_page.find_element(By.XPATH, xpath1)

            # find ratings and ratings_num
            if ratings_box != []:
                ratings = ratings_box.text.strip()
                ratings = str(ratings) + '/5'
            else:
                ratings = 0
        except:
            ratings = 'Not Found'
        return ratings