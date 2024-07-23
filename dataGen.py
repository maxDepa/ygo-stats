import csv

from tournament import Parser as tournamentParser
from tournament import Tournament
from deck import Parser as deckParser
from deck import Deck

def genData(tournaments):
    #tournaments is the number of tournaments to use, sorted by date.(i.e sorted by recency)
    #max 50.
    tournamentArray = tournamentParser.getTournamentLinks()
    
    decks = []
    for x in range(0, tournaments):
        tLinks = tournamentArray[x]
        bArray = Tournament.getDecks(tLinks)
        decksArray = bArray[0]
        noDeckList = bArray[1]

        for deckLink in decksArray:
            info = Deck.getDeckInfo(deckLink)
            decks.append(info)
            
        for name in noDeckList:
            decks.append([name, 'unknown', 'unknown', 'unknown'])

    with open('decks.csv', 'w',encoding="utf-8") as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', lineterminator = '\n')
        #Creates header row
        filewriter.writerow(['name','main', 'extra', 'side'])

        for deck in decks:
            if deck[0] != [] and deck[1] != []:
                print(deck)
                filewriter.writerow([deck[0],deck[1], deck[2], deck[3]])

if __name__ == "__main__":
    genData(2)
