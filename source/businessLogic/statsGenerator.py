import numpy as np
import matplotlib.pyplot as plt
import csv
import os
from source.persistence.file import FileReader
import source.common.constant as constant

def generateArchetypeStats():
    print('Generating archetype files from tournament decks...')
    parsed = FileReader.readCsv(constant.decksFile)
    info = FileReader.getNameDict(constant.decksFile, parsed)
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
                    if cardID.isdigit() == False:
                        continue
                    card_int = int(cardID)
                    name = cardNames.get(card_int)
                    cards.append(name)
                    reverseCards.update({name:cardID})
            deckInformation = FileReader.occurances(cards)

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
                
        directory = os.path.dirname(pathFile)
        if not os.path.exists(directory):
            os.makedirs(directory) 

        with open(pathFile, 'w', encoding="utf-8") as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',', lineterminator = '\n')
            # Creates header row
            filewriter.writerow(['Card Name', 'count','Avg count in decks', 'In percentage of decks',
                                 key, 'deck count: ' + str(count)])
            filewriter.writerows(toWrite)
    print('... finished')


def bar(data):
    fig, ax = plt.subplots(figsize=(16, 9))

    # data in the form of csv name as a str
    parsed = FileReader.readCsv(data)
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

def uniqueDecks(arrayData):
    #assumes read Data from function
    names = []
    for lines in arrayData:
        names.append(lines[0])

    occ = FileReader.occurances(names)

    dtype = [('name', 'U40'), ('count', int)]
    s = np.array(occ, dtype=dtype)
    sorted = np.sort(s, order=['count', 'name'])

    names = []
    count = []

    for element in sorted:
        names.append(element[0])
        count.append(element[1])


    return [names,count]
       
def main():
    generateArchetypeStats()

if __name__ == "__main__":
    main()