from source.model.tournament import Scraper
from source.model.tournament import Tournament
from source.model.deck import Deck
import source.common.constant as constant
from source.persistence.file import FileWriter

def generateDecksData():
    decks = Scraper.getDecksFromLatestTournaments()
    FileWriter.WriteDecksCsv(decks)

if __name__ == "__main__":
    generateDecksData(2)
