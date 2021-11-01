from selenium import webdriver
from selenium.webdriver.common import keys
from selenium.webdriver.common.keys import Keys
import urllib.parse
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import csv
import time
import os
import subprocess, os, platform
from dotenv import load_dotenv
load_dotenv()

companies = os.getenv('COMPANIES').split(",")
formats = os.getenv('FORMATS').split(",")
username = os.getenv('LINKEDIN_USERNAME')
password = os.getenv('LINKEDIN_PASSWORD')
filename = "contacts.csv"

driver = webdriver.Chrome()
        
# Log into LinkedIn
def log_into_linked_in():
    driver.get("https://www.linkedin.com/login")
    email_field = driver.find_element(By.XPATH, '//*[@id="username"]')
    email_field.send_keys(username)
    password_field = driver.find_element(By.XPATH, '//*[@id="password"]')
    password_field.send_keys(password)
    driver.find_element(
        By.XPATH, '//*[@id="organic-div"]/form/div[3]/button').click()
    try:
        driver.find_element(By.XPATH, '//*[@id="ember455"]/button').click()
    except:
        return

# Append string to url
def append_to_url(str):
    url = driver.current_url
    newurl = url+str
    driver.get(newurl)

# TODO
# Read email format to get email of person
def get_email_of(person, company):
    company_idx = companies.index(company)
    unformatted_email = formats[company_idx]
    email = format_email(unformatted_email, person)
    return email

def format_email(format, person):
    name = get_name_of(person).lower()
    names = name.split(" ")
    first_name = names[0]
    last_name = names[len(names)-1]

    if "first" in format:
        format = format.replace("first",first_name)
    else:
        first_initial = first_name[0]
        format = format.replace("f", first_initial)
    
    if "last" in format:
        format = format.replace("last",last_name)
    else:
        last_initial = last_name[0]
        format = format.replace("l",last_initial)

    return format

# Get LinkedIn link of person
def get_link_of(person):
    link = person.find_elements(By.XPATH, './/a')
    if len(link) > 0:
        return link[0].get_attribute("href")
    return None

# Get role of person
def get_role_of(person):
    role = person.find_elements(
        By.XPATH, './section/div/div/div[2]/div[3]/div/div')
    if len(role) > 0:
        return role[0].text
    return None

# Get name of person
def get_name_of(person):
    name = person.find_elements(
        By.XPATH, './section/div/div/div[2]/div[1]/a/div')
    if len(name) > 0:
        return name[0].text
    return None


accepted_roles = ['analyst', 'associate', 'investment manager', 'portfolio manager']
excluded_roles = ['director', 'officer', 'chief', 'incoming', 'partner', 'intern', 'quantitative']

# boolean : if current role is in accepted roles and exclude excluded roles
def filter_by_role(person):
    role = get_role_of(person)
    return role != None and any(x in role.lower() for x in accepted_roles) and not any(x in role.lower() for x in excluded_roles)

# Scrolls all the way down LinkedIn 
def get_all_people():
    previous_people = driver.find_elements(
        By.XPATH, '//*[@id="main"]/div[2]/div/div[2]/div/div[1]/ul/li')
    people = []
    while(len(people) != len(previous_people)):
        previous_people = people
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        people = driver.find_elements(
            By.XPATH, '//*[@id="main"]/div[2]/div/div[2]/div/div[1]/ul/li')
        relevant_people = list(filter(filter_by_role,people))
        if(len(relevant_people) > 0):
            return list(filter(filter_by_role,people))
    return None

# Records Organization, Name, Role, LinkedIn Link, and EMail to CSV
def write_all_people_to_csv(people):
    # field names
    fields = ['Organization', 'Contact',
              'Position/Title', 'LinkedIn', 'E-Mail']


    # writing to csv file
    with open(filename, 'w', newline='') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)

        # writing the fields
        csvwriter.writerow(fields)

        # writing the data rows
        csvwriter.writerows(people)

# Gives a list of all of a person's attributes
def map_person_to_row(person, company):
    name = get_name_of(person)
    role = get_role_of(person)
    link = get_link_of(person)
    email = get_email_of(person, company)
    return [company, name, role, link, email]

# Searches LinkedIn for a given company and goes to the "People" tab
def search(company):
    driver.get("https://www.linkedin.com/search/results/companies/?keywords=" +
               urllib.parse.quote(company))
    try:
        first_result = driver.find_element(
            By.XPATH, '//*[@id="main"]/div/div/div[2]/ul/li/div/div/div[2]/div[1]/div[1]/div/span/span/a')
        if first_result.text == company:
            first_result.click()
            time.sleep(3)
            append_to_url("people/")
            time.sleep(3)
            people = get_all_people()
            if len(people) > 0:
                return map_person_to_row(people[0], company)
    except:
        pass
    print("===============Company '" + company +    
            "' was not found=======================")
    return None

def open_csv():
    if platform.system() == 'Darwin':       # macOS
        subprocess.call(('open', filename))
    elif platform.system() == 'Windows':    # Windows
        os.startfile(filename)
    else:                                   # linux variants
        subprocess.call(('xdg-open', filename))

log_into_linked_in()
people_of_interest = list(
    filter((lambda x: x != None), list(
        map((lambda x: search(x)), companies))))
write_all_people_to_csv(people_of_interest)
driver.close()
driver.quit()
open_csv()