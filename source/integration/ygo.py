#selenium
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
#source
from source.integration.www import WebDriver
import source.common.constant as constant
from source.integration.www import Page;

class TournamentsPage:
    def getTournamentLinks():
        print('Trying to get ' + str(constant.numberOfTournamentsToScrape) + ' tournaments link...')
        driver = WebDriver.Create()
        driver.get(constant.tournamentsUrl)

        #waits for table to be finished
        element = WebDriverWait(driver, 100).until(
                EC.presence_of_element_located((By.CLASS_NAME, "even"))
            )
        
        links = TournamentsPage.scrapeLinksFromSource(driver.page_source)
        driver.close()
        print("... finished! \nNumber of tournaments: " + str(len(links)) + '/' + str(constant.numberOfTournamentsToScrape))
        return links

    def scrapeLinksFromSource(source):
        links = TournamentsPage.findElementsWithBlankTarget(source)
        return TournamentsPage.filterTournamentsInElements(links)

    def findElementsWithBlankTarget(source):
        soup = Page.GetSoupFromContent(source)
        return soup.findAll('a', {'target': "_blank"})
        
    def filterTournamentsInElements(elements):
        links = []
        for element in elements:
            link = element['href']
            if constant.tournamentsSubUrl in link:
                links.append(constant.baseUrl + link)
        return links

class TournamentPage:
    def getDecks(url):
        print('Getting decks from tournament: ' + url)
        decksWithLink = []
        decksWithNoLink = []

        soup = Page.GetSoupFromUrl(url)

        #data = soup.findAll('div', {'id': 'tournament_table'})
        decks = soup.findAll('a', {'role': 'row'})
        count = 0

        for element in decks:
            try:
                decksWithLink.append(constant.baseUrl + element['href'])
                count += 1
            except:
                #print('failed to find decklist (This is normal)')
                try:
                    #sp = BeautifulSoup(element, 'html.parser')
                    rows = element.findAll('span', {'class':'as-tablecell','role': 'gridcell'})
                    name = rows[2].text
                    #removes whitespace
                    transName = name.replace("\n", "")
                    if transName != '':
                        count += 1
                        decksWithNoLink.append(transName)
                except:
                    print('something went wrong')
        #print(url + ' deck count: ' + str(count))
        return [decksWithLink, decksWithNoLink]

class DeckPage:
    def getDeckInfo(url):
        print('Getting deck info from ' + url)
        soup = Page.GetSoupFromUrl(url)
        
        name = DeckPage.getName(soup)
        mainDeck = DeckPage.getMainDeckCards(soup)
        extraDeck = DeckPage.getExtraDeckCards(soup)
        side = DeckPage.getSideDeckCards(soup)

        return [name, mainDeck, extraDeck, side]
    
    #Info
    def getName(soup):
        name = soup.find('h1', {'class': 'mt-5'})
        return name.get_text()
    
    def getDescription(soup):
        return soup.findAll('div', {'class': 'inner-deck-text'})
    
    #Card Ids
    def getAllCards(soup):
        return DeckPage.getCardIdsFromLinks(DeckPage.getAllCardsLinks(soup))

    def getMainDeckCards(soup):
        return DeckPage.getCardIdsFromLinks(DeckPage.getMainDeckCardLinks(soup))

    def getExtraDeckCards(soup):
        return DeckPage.getCardIdsFromLinks(DeckPage.getExtraDeckCardLinks(soup))

    def getSideDeckCards(soup):
        return DeckPage.getCardIdsFromLinks(DeckPage.getSideDeckCardLinks(soup))
    
    def getCardIdsFromLinks(cards):
        deck = []
        for card in cards:
            # removes the hyperlink part to get card ID
            # for example, /card/?search=48130397 -> 48130397
            parsed = ''
            read = False
            for character in card['href']:
                if read:
                    parsed = parsed + character
                if character == '=':
                    read = True
            deck.append(parsed)
        return deck
    
    #Card Links
    def getAllCardsLinks(soup):
        return soup.findAll('a', {'class': 'ygodeckcard'})

    def getMainDeckCardLinks(soup):
        return DeckPage.getDeckSection(soup, 'main_deck').find_all('a', {'class': 'ygodeckcard'})

    def getExtraDeckCardLinks(soup):
        return DeckPage.getDeckSection(soup, 'extra_deck').find_all('a', {'class': 'ygodeckcard'})

    def getSideDeckCardLinks(soup):
        sideDeck = DeckPage.getDeckSection(soup, 'side_deck')
        if sideDeck == None:
            return []
        return sideDeck.find_all('a', {'class': 'ygodeckcard'})
    
    def getDeckSection(soup, section) :
        return soup.find('div', {'class': 'deck-output', 'id' : section})