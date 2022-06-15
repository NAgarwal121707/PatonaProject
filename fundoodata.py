from request_template import RequestTemplate
from selenium_template import SeleniumTemplate
import time
import re
import pandas as pd

driver_path = r'C:\Users\arpita\AppData\Local\Programs\Python\Python37-32\Lib\site-packages\selenium' \
                     r'\chromedriver.exe'
url = 'https://www.fundoodata.com/advance_search.php'
final_data = []
columns_name = ['Company Name', 'Industry Sector', 'Company Type', 'Website', 'Full_Address']
fund_data = SeleniumTemplate(driver_path)
fund_requests = RequestTemplate()
driver = fund_data.get_chrome_driver()
driver.delete_all_cookies()
driver.get(url)
fund_data.click_button("//a[@id='all-ckCompanyType']", 2, driver)
fund_data.click_button("//a[@id='all-ckCompanyEntity']", 2, driver)
fund_data.click_button("//input[@value='Search Query']", 2, driver)
soup = fund_requests.get_soup(driver.page_source)
div_box = soup.find_all('div', attrs={'class': 'normal-detail'})
all_links = [links.find('a')['href'] for links in div_box]
for link in all_links:
    inner_res = fund_requests.make_get_requests(link)
    inner_soup = fund_requests.get_soup(inner_res)
    company_name = inner_soup.find('div', attrs={'class': 'search-page-heading-red'})
    industry_sector = inner_soup.find('div', attrs={'class': 'detail-line'}).find_next('div')\
        .find_all('div', attrs={'class': 'overview-box2'})[2].find('br').next_sibling.strip()
    company_type = inner_soup.find('div', attrs={'class': 'detail-line'}).find_next('div')\
        .find_all('div', attrs={'class':'overview-box2'})[1].find('br').next_sibling.strip()
    website = inner_soup.find('a',attrs={'class': 'pglink'})['href']
    Address = str(inner_soup.find('font').next_sibling).replace('-','') + ' ' +\
              str(inner_soup.find('font').find_next('br').next_sibling).strip()
    Full_Address = " ".join(Address.split())
    a = [company_name.text.strip(), industry_sector, company_type, website, Full_Address]
    final_data.append(a)
fund_requests.create_file(final_data, 'Fundoodata', columns_name, '.csv')
driver.close()