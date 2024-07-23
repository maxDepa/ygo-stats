from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup

from www import WebDriver
from www import Page;

class Tournament:
    #def __init__(self, url):
    #    self.soup = Page.GetSoupFromUrl(url)
    
    def getDecks(tournament_url):
        links = []
        noDeckList = []

        soup = Page.GetSoupFromUrl(tournament_url)

        #data = soup.findAll('div', {'id': 'tournament_table'})
        decks = soup.findAll('a', {'role': 'row'})
        count = 0

        for element in decks:
            try:
                links.append('https://ygoprodeck.com' + element['href'])
                count += 1
            except:
                print('failed to find decklist (This is normal)')
                try:
                    #sp = BeautifulSoup(element, 'html.parser')
                    rows = element.findAll('span', {'class':'as-tablecell','role': 'gridcell'})
                    name = rows[2].text
                    #removes whitespace
                    transName = name.replace("\n", "")
                    if transName != '':
                        count += 1
                        noDeckList.append(transName)
                except:
                    print('something went wrong')
        print('deck count: ' + str(count))
        return [links, noDeckList]

class Parser:
    url = 'https://ygoprodeck.com/tournaments/'
    
    def getTournamentLinks():
        driver = WebDriver.Create()
        driver.get(Parser.url)

        #waits for table to be finished
        element = WebDriverWait(driver, 100).until(
                EC.presence_of_element_located((By.CLASS_NAME, "even"))
            )
        
        hrefs = Parser.getTournaments(driver.page_source)
        driver.close()
        return hrefs

    def getTournaments(source):
        soup = Page.GetSoupFromContent(source)
        td = soup.findAll('a', {'target': "_blank"})
        hrefs = []
        for element in td:
            link = element['href']
            #filter tournament links
            if '/tournament/' in link:
                hrefs.append('https://ygoprodeck.com' + link)
        return hrefs
