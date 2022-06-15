from selenium_template import SeleniumTemplate
from selenium.webdriver.common.by import By
import time
import re
import pandas as pd

# Change chromedriver with your path
driver_path = r'D:\chromedriver_win32\chromedriver.exe'

final_data = []

scrape_data = SeleniumTemplate(driver_path)

driver = scrape_data.get_chrome_driver()

# List of input from excel file
df = pd.read_excel('Search_Product_List.xls')

# Function that scrape data for Amazon


def amazon_scraper():
    amazon_input_list = df['Amazon_Product'].values.tolist()
    for product in amazon_input_list:
        print('--Scraping Amazon Data--')
        amazon_data = {}
        link = "https://www.amazon.in/s?k=" + product
        driver.delete_all_cookies()
        scrape_data.open_webpage(driver, link, 2)
        time.sleep(10)
        xpath1 = '//div[contains(@data-component-type, "s-search-result") and ' \
                 '(//span[contains(text(), ' + '"' + product + '"' + ' )])[2]]'
        item = scrape_data.wait_web_driver(driver, 20, xpath1)
        ratings, product_name_found = scrape_data.amazon_rating_finder(item, xpath1,
                                                                     './/div[@class="a-row a-size-small"]/span')

        product_name = product_name_found.text if product_name_found != '' else 'Not Found'
        amazon_data['product_name'] = product_name
        amazon_data['ratings'] = str(ratings).strip().replace(' out of ', '/').replace(' stars', '')
        amazon_data['Source'] = 'Amazon'
        final_data.append(amazon_data)


# Function to scrape Flipkart data
def flipkart_scrapper():
    flipkart_input_list = df['Flipkart_Product'].values.tolist()
    product_url_list = []

    for product in flipkart_input_list:
        print("--Scraping Flipkart Data---")
        link = "https://www.flipkart.com/search?q=" + product
        driver.delete_all_cookies()
        scrape_data.open_webpage(driver, link, 2)
        time.sleep(10)
        product_url_list.append(scrape_data.flipkart_url_finder(driver, '(//a[contains(@rel, '
                                                                        '"noopener noreferrer")])[1]'))
    for product_url in product_url_list:
        flipkart_data = {}
        visible_path = '//div[contains(@id, container)]'
        scrape_data.open_webpage(driver, product_url, 2)
        time.sleep(10)
        item_found = scrape_data.wait_web_driver(driver, 20, visible_path)
        rating_path_id = re.findall(r'productRating_.*\w', item_found.get_attribute('innerHTML'))
        span_id = rating_path_id[0].split('" class')[0]
        xpath2 = '//span[contains(@id, "'+ str(span_id) + '")]'
        flipkart_product_name, ratings = scrape_data.flipkart_product_rating(item_found, xpath2)
        flipkart_data['product_name'] = flipkart_product_name
        flipkart_data['ratings'] = str(ratings) + '/5'
        flipkart_data['Source'] = 'Flipkart'
        final_data.append(flipkart_data)


# Function that scrape data for Myntra
def myntra_scrapper():
    print("--Scraping Myntra Data---")
    myntra_input_list = df['Myntra_Product'].values.tolist()
    for product in myntra_input_list:
        myntra_data = {}
        link = "https://www.myntra.com/" + product
        driver.delete_all_cookies()
        scrape_data.open_webpage(driver, link, 2)
        time.sleep(10)
        xpath = '//body'
        rating_path = '//div[contains(@class, "product-ratingsContainer")]//span'
        item = scrape_data.wait_web_driver(driver, 20, xpath)
        ratings = scrape_data.myntra_scraper(item, rating_path)
        myntra_data['product_name'] = product
        myntra_data['ratings'] = ratings
        myntra_data['Source'] = 'Myntra'
        final_data.append(myntra_data)


# Initialized function to scrape data


amazon_scraper()
flipkart_scrapper()
myntra_scrapper()

cnames = ['product_name', 'ratings', 'Source']

final_df = pd.DataFrame(final_data)
final_df = final_df[cnames]
correct_name = []
final_df.to_csv('Rating_Comparison.csv', index=False)

driver.close()

# Code Format output according to requirement

df_change = pd.read_csv('Rating_Comparison.csv')

# Function changes the original output to required output


def foramting_file(df_change):
    correct_name = []
    for name in df_change['product_name'].values.tolist():

        if "Zeta" in name:
            c_name = "Puma Shoes"
            correct_name.append(c_name)
        if "NN3184SL01" in name:
            c_name = "Fastrack Watch"
            correct_name.append(c_name)
        if "HP Pavilion" in name:
            c_name = "Hp Laptops"
            correct_name.append(c_name)
        if "HD3151" in name:
            c_name = "Hair Dyer"
            correct_name.append(c_name)
        if "boAt" in name or "boat" in name:
            c_name = "Boat Headset"
            correct_name.append(c_name)

    df_change['Product Name'] = correct_name
    df_change = df_change.drop(['product_name'], axis=1)
    df_new = df_change.pivot(index=['Product Name'], columns=['Source'], values=['ratings'])
    df_new.columns = df_new.columns.droplevel(0)
    df_new = df_new.reset_index()
    df_new.to_csv('Rating_Comparison_Formated_Output.csv', index=False)


foramting_file(df_change)




