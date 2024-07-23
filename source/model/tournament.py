from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import source.common.constant as constant
from source.integration.www import WebDriver
from source.integration.www import Page;

class Tournament:
    def getDecks(url):
        links = []
        noDeckList = []

        soup = Page.GetSoupFromUrl(url)

        #data = soup.findAll('div', {'id': 'tournament_table'})
        decks = soup.findAll('a', {'role': 'row'})
        count = 0

        for element in decks:
            try:
                links.append(constant.baseUrl + element['href'])
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

class Scraper:
    def getTournamentLinks():
        driver = WebDriver.Create()
        driver.get(constant.tournamentsUrl)

        #waits for table to be finished
        element = WebDriverWait(driver, 100).until(
                EC.presence_of_element_located((By.CLASS_NAME, "even"))
            )
        
        hrefs = Scraper.filterTournamentsLinks(driver.page_source)
        driver.close()
        return hrefs

    def filterTournamentsLinks(source):
        soup = Page.GetSoupFromContent(source)
        td = soup.findAll('a', {'target': "_blank"})
        hrefs = []
        for element in td:
            link = element['href']
            if constant.tournamentsSubUrl in link:
                hrefs.append(constant.baseUrl + link)
        return hrefs
