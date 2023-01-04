import requests
from bs4 import BeautifulSoup
import logging
from selenium import webdriver

#"static" scrape, unlike dynamic.py

def getDeckInfo(url):
    r = requests.get(url)
    # Parsing the HTML
    soup = BeautifulSoup(r.content, 'html.parser')

    name = soup.find('h1', {'class': 'mt-5'})
    name = name.get_text()

    #finding Deck info
    #cards = soup.findAll('a', {'class': 'ygodeckcard'})
    main = soup.find('div', {'class': 'deck-output', 'id' : 'main_deck'}).find_all('a', {'class': 'ygodeckcard'})
    extra = soup.find('div', {'class': 'deck-output', 'id' : 'extra_deck'}).find_all('a', {'class': 'ygodeckcard'})
    side = soup.find('div', {'class': 'deck-output', 'id' : 'side_deck'}).find_all('a', {'class': 'ygodeckcard'})

    mainDeck = removeLinks(main)
    extraDeck = removeLinks(extra)
    side = removeLinks(side)

    #discription, that you see on the page normally
    #fullDesc = soup.findAll('div', {'class': 'inner-deck-text'})

    #return [name, fullDesc, deck]
    return [name, mainDeck, extraDeck, side]

def removeLinks(cards):
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


def getDecksFromT(tournament_url):
    #gets decks from a tournament URL. returns
    # ex: deckFinder = 'https://ygoprodeck.com/category/tournament/ycs-minneapolis-34'
    links = []
    noDeckList = []
    r = requests.get(tournament_url)
    soup = BeautifulSoup(r.content, 'html.parser')

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

