import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels
import csv
import math
import requests
import json
import os

def bar(data):
    fig, ax = plt.subplots(figsize=(16, 9))

    # data in the form of csv name as a str
    parsed = readData(data)
    occ = uniqueDecks(parsed)
    unique = occ[0]
    count = occ[1]

    ax.set_title("Tear Format breakdown")
    ax.yaxis.set_tick_params(pad=10)
    ax.xaxis.set_tick_params(pad=5)
    for i in ax.patches:
        plt.text(i.get_width() + 0.2, i.get_y() + 0.5,
                 str(round((i.get_width()), 2)),
                 fontsize=10, fontweight='bold',
                 color='grey')
    ax.barh(unique,count)
    plt.show()


def readData(data):
    # data in the form of csv name as a str
    csvLines = []
    with open(data, mode='r',encoding="utf-8") as file:
        # reading the CSV file
        csvFile = csv.reader(file)
        # retreiving the contents of the CSV file

        for lines in csvFile:
            if lines != []:
                #turns back into list
                for index in [1,2,3]:
                    temp = lines[index]
                    temp = temp.replace('[', '')
                    temp = temp.replace(']','')
                    temp = temp.replace('\'','')
                    temp = temp.split(', ')
                    lines[index] = temp
                csvLines.append(lines)
    fixedLines = csvLines[1:]
    return fixedLines

def occurances(arrayData):
    #array of each element, unique entries
    unique = []
    count = []
    for element in arrayData:
        if element not in unique:
            unique.append(element)
            count.append(0)
        index = unique.index(element)
        count[index] += 1

    combined = []

    for uElement in unique:
        index = unique.index(uElement)
        cElement = count[index]
        combo = (uElement,cElement)
        combined.append(combo)
    return combined

def uniqueDecks(arrayData):
    #assumes read Data from function
    names = []
    for lines in arrayData:
        names.append(lines[0])

    occ = occurances(names)

    dtype = [('name', 'U40'), ('count', int)]
    s = np.array(occ, dtype=dtype)
    sorted = np.sort(s, order=['count', 'name'])

    names = []
    count = []

    for element in sorted:
        names.append(element[0])
        count.append(element[1])


    return [names,count]

def getNameDict(data):
    # data in the form of csv name as a str
    parsed = readData(data)
    main = {}
    extra = {}
    side = {}

    #unique copies of a card in a particular deck. For example, if one tear list runs 3 copies of '123' and another
    # runs only 1 in the extra deck, then uniqueExtra would have an array as follows: ['123', '123']
    uniqueMain = {}
    uniqueExtra = {}
    uniqueSide = {}
    
    for deck in parsed:
        # deck[1] is a array/list.
        key = deck[0]
        
        def getUnique(array):
            unique = []
            for id in array:
                if id not in unique:
                    unique.append(id)
            return unique

        if key not in main.keys() and deck[1] != ['unknown']:
            main.update({key:deck[1]})
            uniqueMain.update({key:getUnique(deck[1])})

            extra.update({key:deck[2]})
            uniqueExtra.update({key: getUnique(deck[2])})

            side.update({key:deck[3]})
            uniqueSide.update({key: getUnique(deck[3])})

        elif key in main.keys() and deck[1] != ['unknown']:
            tempArray = main.get(key) + deck[1]
            main.update({key:tempArray})
            uArray = uniqueMain.get(key) + getUnique(deck[1])
            uniqueMain.update({key:uArray})

            tempArray = extra.get(key) + deck[2]
            extra.update({key:tempArray})
            uArray = uniqueExtra.get(key) + getUnique(deck[2])
            uniqueExtra.update({key: uArray})

            tempArray = side.get(key) + deck[3]
            side.update({key:tempArray})
            uArray = uniqueSide.get(key) + getUnique(deck[3])
            uniqueSide.update({key: uArray})

    cardsID = []
    for deckDict in [main,extra,side]:
        for key in deckDict.keys():
            value = deckDict.get(key)
            cardsID = cardsID + value
    combined = occurances(cardsID)
    #array of unique card ID's
    unique = []
    for list in combined:
        unique.append(list[0])

    return [getCardsInfo(unique), main, extra, side, uniqueMain, uniqueExtra, uniqueSide]


def getCardsInfo(cardArray):
    #card array is an array, filled with unique card ID's.
    #api endpoint: https://db.ygoprodeck.com/api/v7/cardinfo.php
    ID = ''

    for cardID in cardArray:
        # '%2C' is a URL encoded comma. This is needed to do multiple ID's in one request.
        ID = ID + cardID + '%2C'

    data = requests.get("https://db.ygoprodeck.com/api/v7/cardinfo.php?id="+ ID)
    if (data.status_code != 200):
        print('ERROR: request status code not 200', data.status_code)

    info = data.json()['data']
    #creates a dictionary that takes an id for input and translates it into a name.
    cardNames = {}
    for card in info:
        #creates an array with all the cardID's for the specific card.
        cardIDs = []
        for image in card['card_images']:
            cardIDs.append(image['id'])
        for cardID in cardIDs:
            cardNames.update({cardID:card['name']})

    return cardNames
    # IMPORTANT: The api combines the return for the same card in the case of erratas. FOr example, the bagooska errata
    # is combined into one return, and seemingly the only way to get all the ID's is to look at the ID's for the image
    # return.

def genBuildStats():
    parsed = readData('decks.csv')
    info = getNameDict('decks.csv')
    uniqueMain = info[4]
    uniqueExtra = info[5]
    uniqueSide = info[6]

    #map with card names
    cardNames = info[0]
    #dictionary with all cards in specific decks
    stats = uniqueDecks(parsed)
    deckNames = stats[0]
    deckCount = stats[1]

    # creates a dictionary that uses deck names and input and returns all individual cards found in those decks.
    # this is not 'unique' cards.
    for key in info[1].keys():
        toWrite = []
        for part in [[info[1],'main'],[info[2],'extra'],[info[3],'side']]:
            #don't technically need some of these but it helps me to see it
            decks = part[0]
            #adds 'main' for example to know what part of the deck you are in
            toWrite.append([part[1],'','','','',''])

            cards = []
            reverseCards = {}
            #creates a path and file Name for each individual deck type. EX: spright.csv
            deckNameForFile = key

            #removes illegal characters from name. The only ones that might be used to be honest are @,/, and *
            iChar = '<>:"/\|?*@'
            for char in iChar:
                if char in deckNameForFile:
                    deckNameForFile = deckNameForFile.replace(char,'')

            fileName = deckNameForFile + '.csv'

            pathFile = "{}{}{}{}{}".format(os.getcwd(), os.sep, 'deckStats', os.sep, fileName)
            cardList = part[0][key]
            
            if decks[key] != ['']:
                for cardID in cardList:
                    card_int = int(cardID)
                    name = cardNames.get(card_int)
                    cards.append(name)
                    reverseCards.update({name:cardID})
            deckInformation = occurances(cards)

            ind = deckNames.index(key)
            count = deckCount[ind]
            #prepares info to write into csv file.
            for card in deckInformation:
                card_name = card[0]
                card_count = card[1]
                card_avg_count = (float(card[1]) / float(count))
                cID = reverseCards[card[0]]
                if part[1] == 'main':
                    deck_percentage = uniqueMain[key].count(cID) / float(count)
                elif part[1] == 'extra':
                    deck_percentage = uniqueExtra[key].count(cID) / float(count)
                elif part[1] == 'side':
                    deck_percentage = uniqueSide[key].count(cID) / float(count)

                card_avg_count = format(card_avg_count, '.3')
                deck_percentage = format(deck_percentage, '.3%')
                payload = (card_name, card_count, card_avg_count, deck_percentage,'','')
                toWrite.append(payload)
                
        with open(pathFile, 'w', encoding="utf-8") as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',', lineterminator = '\n')
            # Creates header row
            filewriter.writerow(['Card Name', 'count','Avg count in decks', 'In percentage of decks',
                                 key, 'deck count: ' + str(count)])
            filewriter.writerows(toWrite)

        
def main():
    genBuildStats()


if __name__ == "__main__":
    main()