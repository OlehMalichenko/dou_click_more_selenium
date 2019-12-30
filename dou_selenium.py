from selenium import webdriver
from pprint import pprint
from time import sleep
from bs4 import BeautifulSoup
import csv

def main():
    driver = start_driver()
    if driver is None:
        return

    driver.implicitly_wait(2)

    find_more_btn(driver)

    company_dict = find_company_list(driver)

    driver.close()

    write_to_csv(company_dict)



def parse_company_list(company_list: list):
    pass


def start_driver():
    driver = webdriver.Firefox()
    url = 'https://jobs.dou.ua/companies/'

    try:
        driver.get(url)
    except:
        print('not start driver')
        return None
    else:
        return driver


def find_more_btn(driver):
    displayed = True
    while displayed is True:
        try:
            more_btn = driver.find_element_by_xpath('//div[@id="companiesListId"]/div[@class="more-btn"]/a[@href]')
            print('Is displayed: ' + str(more_btn.is_displayed()))
            print('Is enabled: ' + str(more_btn.is_enabled()))
        except:
            displayed = False
            print('more_btn is not found')
        else:
            if more_btn.is_displayed() is True:
                more_btn.click()
            else:
                displayed = False


def find_company_list(driver):
    path_to_href = '//div[@id="companiesListId"]' \
                   '//div[@class="company"]' \
                   '/div[@class="ovh"]' \
                   '/div[@class="h2"]' \
                   '/a[@class="cn-a"]'
    try:
        tags = driver.find_elements_by_xpath(path_to_href)
    except:
        print('no find company list')
        return None
    else:
        company_dict = dict()
        for company in tags:
            href = company.get_attribute('href')
            name = company.get_attribute('text')
            company_dict[name] = href

        return company_dict


def write_to_csv(company_dict: dict):
    print('\n\n\n ====================================CSV=====================================')
    with open('csv_dou.csv', 'w', newline='\n') as csv_file:
        writer = csv.writer(csv_file)

        title_data = ['NAME', 'HREF']
        writer.writerow(title_data)

        for name, href in company_dict.items():
            line_list = [ name, href ]
            try:
                writer.writerow(line_list)
            except:
                continue


if __name__=='__main__':
    main()