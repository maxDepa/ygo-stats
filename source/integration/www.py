from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import requests

class WebDriver:
    def Create():
            firefoxOptions = Options()
            firefoxOptions.add_argument('--headless')
            return webdriver.Firefox(options=firefoxOptions)
        
class Page:
    def Get(url):
        return requests.get(url)
    
    def GetText(url):
        return Page.Get(url).text
    
    def GetContent(url):
        return Page.Get(url).content
    
    def GetSoupFromUrl(url):
        return BeautifulSoup(Page.GetContent(url), 'html.parser')
    
    def GetSoupFromContent(content):
        return BeautifulSoup(content, 'html.parser')