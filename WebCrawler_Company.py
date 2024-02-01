# -*- coding: utf-8 -*-
"""
problem 1: do we consider info from pitchbook?
"""
# from linkedin_scraper import Person, actions, Company
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
import csv
import re
from writeXML import writeFile
from tqdm import tqdm
from companies_basic import guess_industry, guess_URL

def login(email, password):
    email = email
    password = password

    driver.maximize_window()

    driver.get('https://www.linkedin.com/login')
    time.sleep(10)
    driver.find_element_by_id('username').send_keys(email)
    driver.find_element_by_id('password').send_keys(password)
    driver.find_element_by_id('password').send_keys(Keys.RETURN)
    time.sleep(10)
    if len(driver.find_elements_by_name("pin")) != 0:
        code = fetch_ver_code(email, password)
        driver.find_element_by_name("pin").send_keys(code)
        driver.find_element_by_name("pin").send_keys(Keys.RETURN)
        time.sleep(10)

def fetch_ver_code(email, password):
    browser = webdriver.Chrome("C:\Ipser\web-crawler\chromedriver-win32\chromedriver-win32\chromedriver.exe")
    browser.get('https://mail.google.com/')
    # login gmail
    browser.find_element_by_id('identifierId').send_keys(email + Keys.ENTER)
    time.sleep(5)
    browser.find_element_by_name('Passwd').send_keys(password + Keys.ENTER)
    time.sleep(10)
    # fetch code
    browser.find_element_by_css_selector('table.F.cf.zt tbody tr').click()
    time.sleep(5)
    email_body = browser.find_elements_by_css_selector('div.ii.gt')[0].text
    verification_code = re.search(r'(\d{6})', email_body).group(1)
    browser.quit()
    return verification_code


# import requests
def fetch_companies():
    browser = webdriver.Chrome("C:\Ipser\web-crawler\chromedriver-win32\chromedriver-win32\chromedriver.exe")
    browser.get("https://itc.ucdavis.edu/startups/startup-companies/")
    time.sleep(7)
    elements = browser.find_elements_by_class_name("avia_textblock")
    companies = {}
    for element in tqdm(elements):
        try:
            startup_name = element.find_element_by_class_name("startup-title").text
            startup_description = element.find_element_by_class_name("startup-content").text
            startup_industry = guess_industry(startup_description)
            startup_link = guess_URL(startup_name)
            companies[startup_name] = {"sdescription": startup_description, "sindustry": startup_industry,
                                       "slink": startup_link, "sname": startup_name}
            fetch_company_employee(startup_name)
            writeFile("startup.xml", companies, "startup")
        except Exception as e:
            if str(e).split("\n")[
                0] != 'Message: no such element: Unable to locate element: {"method":"css selector","selector":".startup-title"}':
                print(startup_name)
                print(e)
            continue

    writeFile("startup.xml", companies, "startup")





def scroll(in_scroll, fin_scroll, scrollTime):
    start = time.time()

    # will be used in the while loop
    initialScroll = in_scroll
    finalScroll = fin_scroll
    while True:
        driver.execute_script(f"window.scrollTo({initialScroll},{finalScroll})")
        # this command scrolls the window starting from
        # the pixel value stored in the initialScroll 
        # variable to the pixel value stored at the
        # finalScroll variable
        initialScroll = finalScroll
        finalScroll += 200

        # we will stop the script for 3 seconds so that 
        # the data can load
        time.sleep(2)
        # You can change it as per your needs and internet speed

        end = time.time()

        # We will scroll for 10 seconds.
        # You can change it as per your needs and internet speed
        if round(end - start) > scrollTime:
            break

driver = webdriver.Chrome("C:\Ipser\web-crawler\chromedriver-win32\chromedriver-win32\chromedriver.exe")
email = "hongyew56@gmail.com"
password = "20000517"
login(email, password)

def fetch_company_employee(company_name:str):
    driver.get("https://www.linkedin.com/company/{0}".format(company_name.replace(" ", "-")))
    time.sleep(2)
    people_tab_1 = driver.find_element_by_xpath('//a[contains(@href,"/company/{0}/people")]'.format(company_name.lower().replace(" ", "-")))
    people_tab_1.click()
    employee = fetch_profiles(10)
    print(employee)
    return employee

def fetch_profiles(number:int):
    all_data = []
    driver.execute_script("document.body.style.zoom='70%'")
    # Scroll to load required number of profiles
    scroll(0, 200, number * 1.5)
    time.sleep(1)

    # Fetch and store all profile links on the page
    links = [x.get_attribute('href') for x in
             driver.find_elements_by_css_selector("div.scaffold-finite-scroll__content a")]

    for i, element in zip(range(0, number * 2, 2), links[::2]):
        # get current profile
        driver.get(links[i])

        # Wait for page load
        time.sleep(0.75)

        # Fetch page source code
        emp_src = driver.page_source

        # parse through Beautiful soup
        emp_soup = bs(emp_src, 'lxml')

        # Find header
        header = emp_soup.find('div', {'class': 'mt2 relative'})

        # Extract first name, last name, headline and location from header
        fname, lname = header.find('h1').get_text().split(" ")[0], ' '.join(header.find('h1').get_text().split(" ")[1:])
        headline = header.find('div', {'class': 'text-body-medium break-words'}).get_text().strip()
        location = header.find('span',
                               {'class': 'text-body-small inline t-black--light break-words'}).get_text().strip()

        # Append this information to list of list
        all_data.append([fname, lname, headline, location])

        # Locate image wrapper, download and save to disk. If Image is not present, proceed without doing anything
        img_wrapper = emp_soup.find('div', {'class': 'pv-top-card__non-self-photo-wrapper ml0'})
        pic = img_wrapper.find('img')
        # try:
        #     # r = requests.get(pic['src']).content
        #     pic['alt'] = pic['alt'].replace('/', ' ')
        #     with open("images/"+pic['alt']+".jpg","wb+") as f:
        #           f.write(r)
        #     f.close()
        # except:
        #     pass
    return all_data
    # headers = ['First_Name', 'Last_Name', 'Headline', 'Location']
    # write_to_csv(headers, all_data)


def write_to_csv(headers, data):
    with open('employees.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        # write the header
        writer.writerow(headers)
        # write all data
        writer.writerows(data)


if __name__ == "__main__":
    driver_path = "C:\Ipser\web-crawler\chromedriver-win32\chromedriver-win32\chromedriver.exe"
    email = "hongyew56@gmail.com"
    password = "20000517"

    fetch_companies()

    driver.quit()

    #
    # driver.get("https://www.linkedin.com/company/hubspot/")
    #
    # time.sleep(2)
    #
    # people_tab = driver.find_element_by_xpath('//a[contains(@href,"/company/hubspot/people")]')
    #
    # people_tab.click()

    # fetch_profiles(number)
