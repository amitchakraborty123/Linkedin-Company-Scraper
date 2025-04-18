'''
Author: Amit Chakraborty
Project: Linkedin Website Company Data Scraper
Profile URL: https://github.com/amitchakraborty123
E-mail: mr.amitc55@gmail.com
'''

import datetime
import time
import pandas as pd
from bs4 import BeautifulSoup
import warnings
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
import os

warnings.filterwarnings("ignore")
x = datetime.datetime.now()
n = x.strftime("__%b_%d_%Y")


def driver_conn():
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--headless")      # Make the browser Headless. if you don't want to see the display on chrome just uncomment this
    chrome_options.add_argument("--log-level=3")    # Removes error/warning/info messages displayed on the console
    chrome_options.add_argument("--disable-infobars")  # Disable infobars ""Chrome is being controlled by automated test software"  Although is isn't supported by Chrome anymore
    chrome_options.add_argument("start-maximized")     # Make chrome window full screen
    chrome_options.add_argument('--disable-gpu')       # Disable gmaximizepu (not load pictures fully)
    # chrome_options.add_argument("--incognito")       # If you want to run browser as incognito mode then uncomment it
    chrome_options.add_argument("--disable-notifications")  # Disable notifications
    chrome_options.add_argument("--disable-extensions")     # Will disable developer mode extensions

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)  # you don't have to download chromedriver it will be downloaded by itself and will be saved in cache
    return driver


all_link = []
driver = driver_conn()
driver.get('https://www.linkedin.com')
input('Login and Press Enter Here: ')


# ================================================================================
#                         Getting Company Links From Name Search
# ================================================================================
def get_link():
    url = 'https://www.linkedin.com/search/results/companies/?origin=SWITCH_SEARCH_VERTICAL&sid=hsa'
    driver.get(url)
    time.sleep(3)
    df = pd.read_csv("company_name.csv")
    names = df['Name'].values
    print('Total link: ' + str(len(names)))
    d = 0
    for name in names:
        d += 1
        print('Getting company names: ' + str(d) + ' out of ' + str(len(names)))
        page = 0
        while True:
            page += 1
            if page > 5:
                break
            print(f'>>>>>>>>>>> Page number: {page}')
            driver.get(f'https://www.linkedin.com/search/results/companies/?keywords={name}&origin=GLOBAL_SEARCH_HEADER&page={page}')
            time.sleep(3)
            soup = BeautifulSoup(driver.page_source, 'lxml')
            try:
                divs = soup.find('div', {'class': 'search-results-container'}).find_all('li')
            except:
                divs = []
            print(f'Listing here: {len(divs)}')
            for div in divs:
                try:
                    link = div.find('a')['href']
                    urls = {
                        'links': link,
                    }
                    if urls not in all_link:
                        all_link.append(urls)
                        df = pd.DataFrame(all_link)
                        df = df.rename_axis("Index")
                        df.to_csv('links.csv', encoding='utf-8-sig')
                except:
                    pass
        df = pd.DataFrame(all_link)
        df = df.rename_axis("Index")
        df.to_csv('links.csv', encoding='utf-8-sig')


def get_data():
    df = pd.read_csv('links.csv')
    links = df['links'].values
    print('================ Getting Data ================')
    l = 0
    for link in links:
        l += 1
        print('Link ' + str(l) + ' Out of ' + str(len(links)))
        driver.get(link + 'about/')
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, 'lxml')

        company_name = ''
        tagline = ''
        service_summery = ''
        followers = ''
        employee = ''
        website = ''
        location = ''
        overview = ''
        industry = ''
        company_size = ''
        founded = ''
        headquarter = ''
        try:
            company_name = soup.find('div', {'class': 'org-top-card__primary-content'}).find('h1').text.replace('\n', '')
        except:
            pass
        try:
            tagline = soup.find('div', {'class': 'org-top-card__primary-content'}).find('p', {'class': 'org-top-card-summary__tagline'}).text.replace('\n', '').strip()
        except:
            pass
        try:
            service_summery = soup.find('div', {'class': 'org-top-card-summary-info-list'}).find('div', {'class': 'org-top-card-summary-info-list__info-item'}).text.replace('\n', '').strip()
        except:
            pass
        try:
            temp = soup.find('div', {'class': 'org-top-card-summary-info-list'}).find_all('div', {'class': 'org-top-card-summary-info-list__info-item'})
            for dess in temp:
                if 'followers' in dess.text:
                    followers = dess.text.replace('\n', '').strip().replace('followers', '')
        except:
            pass
        try:
            temp = soup.find('section', {'class': 'org-top-card artdeco-card'}).find_all('a')
            for dess in temp:
                if 'employees' in dess.text:
                    employee = dess.text.replace('\n', '').strip().replace('See all ', '')
        except:
            pass
        try:
            dess = soup.find('div', {'class': 'org-transition-scroll'}).find_all('dt')
            for des in dess:
                if 'Website' in des.text:
                    print('got')
                    website = des.find_next_sibling('dd').text.strip()
                if 'Industry' in des.text:
                    industry = des.find_next_sibling('dd').text.strip()
                if 'Company size' in des.text:
                    company_size = des.find_next_sibling('dd').text.strip()
                if 'Headquarters' in des.text:
                    headquarter = des.find_next_sibling('dd').text.strip()
                if 'Founded' in des.text:
                    founded = des.find_next_sibling('dd').text.strip()
        except:
            pass
        try:
            overview = soup.find('section', {'class': 'org-page-details-module__card-spacing'}).find('p').text.replace('\n', '').strip()
        except:
            pass
        try:
            location = soup.find('div', {'class': 'org-location-card'}).text.replace('      ', '').strip()
        except:
            pass

        if company_name != '':
            data = {
                'Company url': link,
                'Company Name': company_name,
                'Tagline': tagline,
                'Service Summery': service_summery,
                'Followers': followers,
                'Employee': employee,
                'Website': website,
                'Location': location,
                'Overview': overview,
                'Industry': industry,
                'Company Size': company_size,
                'Founded': founded,
                'Headquarter': headquarter,
            }
            df = pd.DataFrame([data])
            df.to_csv('Company_data' + n + '.csv', mode='a', header=not os.path.exists('Company_data' + n + '.csv'), encoding='utf-8-sig', index=False)
    print('================ Final Data Saved ================')
    driver.close()
    driver.quit()


if __name__ == '__main__':
    get_link()
    get_data()
