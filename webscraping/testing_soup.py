'''
#using beautifullsoup
#pip install BeautifulSoup4
from bs4 import BeautifulSoup
import urllib.request
import re
import requests
#pip install lxml
#pip install html5lib

url = "https://www.lazada.sg/#"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
#url = "https://en.wikipedia.org/wiki/List_of_national_capitals"

try:
    #page = urllib.request.urlopen(url)
    r = requests.get(url, headers=headers)
    print("the url has no error")
except:
    print("the url has an error ")

try: 
    #soup = BeautifulSoup(page, 'html.parser')
    soup = BeautifulSoup(r, "html.parser")
    print("no error on the request form")
    print(soup)
except:
    print("your request was denied sir")
    
''' 
'''
#using selenium
#pip install selenium

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

driver = webdriver.Chrome(executable_path='chromedriver')
driver.get('https://www.linkedin.com/in/lo%C3%AFc-e-90ba8111b/')

#https://www.linkedin.com/in/loïc-e-90ba8111b/

"""
timeout = 30
try:
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.ID, "Level_1_Categry_No1")))
except TimeoutException:
    driver.quit()
"""
category_element = driver.find_element(By.XPATH,'//*[@id="ember51"]/div[2]/div[2]/div[1]/ul[1]/li[1]').text

'''
#pip install sleep
#crée un robot qui va se connecter
#importer les librairies necessaires
from selenium import  webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
import parameters
from parsel import Selector

# function to ensure all key data fields have a value
def validate_field(field):# if field is present pass if field:pass
# if field is not present print text else:
       field = 'No results'
       return field

#utiliser le river correspondant à son navigateur
driver = webdriver.Chrome('C:/Users/moi/Desktop/projet finder/chromedriver')

driver.get('https://www.linkedin.com')


username= driver.find_element_by_name('session_key')
username.send_keys(parameters.linkedin_username)
sleep(2)


password = driver.find_element_by_name('session_password')
password.send_keys(parameters.linkedin_password)
sleep(4)


log_in_button=driver.find_element_by_class_name('sign-in-form__submit-btn')
log_in_button.click()

#aller sur google pour faire sa recherche
driver.get('https://www.google.com')
search_query= driver.find_element_by_name('q')
search_query.send_keys(parameters.search_query)
sleep(3)
search_query.send_keys(Keys.RETURN)

linkedin_urls= driver.find_elements_by_class_name('iUh30')
len(linkedin_urls)

linkedin_urls = [url.text for url in linkedin_urls]

for i in range(len(linkedin_urls)-1):
    if linkedin_urls[i]=="89":
        del linkedin_urls[i]

driver.quit()

##faire des commentaires
#faire une base de  donnée pour 
# url = url + nom de la personne