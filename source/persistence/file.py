import csv

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