from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.options import Options
import requests
from bs4 import BeautifulSoup

def getTournamentLinks():
    
    firefoxOptions = Options()
    firefoxOptions.add_argument('--headless')
    driver = webdriver.Firefox(options=firefoxOptions)
    #using firefox because it is my favorite browser :)))
    url = 'https://ygoprodeck.com/category/tournaments/'
    
    driver.get(url)

    #waits for table to be finished
    element = WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.CLASS_NAME, "even"))
        )
    #table = driver.find_element(By.ID, "tournamentsTable")
    #print(table.text)

    hrefs = getTournaments(driver.page_source)

    driver.close()

    return hrefs

def getTournaments(source):
    soup = BeautifulSoup(source, 'html.parser')
    td = soup.findAll('a', {'target': "_blank"})
    hrefs = []
    for element in td:
        link = element['href']
        #makes sure it is a link from a tournament.
        if '/category/tournament/' in link:
            hrefs.append('https://ygoprodeck.com' + link)

    return hrefs