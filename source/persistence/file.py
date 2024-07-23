import csv
from source.model.card import Card

class FileWriter:        
    def WriteDecksCsv(decks):
        with open('decks.csv', 'w',encoding="utf-8") as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',', lineterminator = '\n')
            #Creates header row
            filewriter.writerow(['name','main', 'extra', 'side'])
            for deck in decks:
                if deck[0] != [] and deck[1] != []:
                    #print(deck)
                    filewriter.writerow([deck[0],deck[1], deck[2], deck[3]])
                    
class FileReader:
    def readCsv(data):
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

    def getNameDict(data, parsed):
        # data in the form of csv name as a str
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
        combined = FileReader.occurances(cardsID)
        #array of unique card ID's
        unique = []
        for list in combined:
            unique.append(list[0])

        return [Card.getCardsInfo(unique), main, extra, side, uniqueMain, uniqueExtra, uniqueSide]
    
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
    

