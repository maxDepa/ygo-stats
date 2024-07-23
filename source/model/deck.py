from source.integration.www import Page

class Deck:
    def getDeckInfo(url):
        soup = Page.GetSoupFromUrl(url)
        
        name = Parser.getName(soup)
        mainDeck = Parser.getMainDeckCards(soup)
        extraDeck = Parser.getExtraDeckCards(soup)
        side = Parser.getSideDeckCards(soup)

        return [name, mainDeck, extraDeck, side]

class Parser:
    #Info
    def getName(soup):
        name = soup.find('h1', {'class': 'mt-5'})
        return name.get_text()
    
    def getDescription(soup):
        return soup.findAll('div', {'class': 'inner-deck-text'})
    
    #Card Ids
    def getAllCards(soup):
        return Parser.getCardIdsFromLinks(Parser.getAllCardsLinks(soup));

    def getMainDeckCards(soup):
        return Parser.getCardIdsFromLinks(Parser.getMainDeckCardLinks(soup));

    def getExtraDeckCards(soup):
        return Parser.getCardIdsFromLinks(Parser.getExtraDeckCardLinks(soup));

    def getSideDeckCards(soup):
        return Parser.getCardIdsFromLinks(Parser.getSideDeckCardLinks(soup));
    
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
        return soup.find('div', {'class': 'deck-output', 'id' : 'main_deck'}).find_all('a', {'class': 'ygodeckcard'})

    def getExtraDeckCardLinks(soup):
        return soup.find('div', {'class': 'deck-output', 'id' : 'extra_deck'}).find_all('a', {'class': 'ygodeckcard'})

    def getSideDeckCardLinks(soup):
        return soup.find('div', {'class': 'deck-output', 'id' : 'side_deck'}).find_all('a', {'class': 'ygodeckcard'})