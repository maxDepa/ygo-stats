from source.integration.ygo import TournamentsPage
from source.integration.ygo import TournamentPage
from source.integration.ygo import DeckPage
from source.persistence.file import FileWriter
import source.common.constant as constant

def generateDecksData():
    tournamentLinks = TournamentsPage.getTournamentLinks()
    decks = generateDecksFromTournaments(tournamentLinks)
    FileWriter.WriteDecksCsv(decks)
    
def generateDecksFromTournaments(tournamentLinks):
    decks = []
    for x in range(0, constant.numberOfTournamentsToScrape):
        tournamentLink = tournamentLinks[x]
        
        if(TournamentPage.IsTCG(tournamentLink) == False):
            continue

        deckLinks = TournamentPage.getDecks(tournamentLink)
        
        validDecks = deckLinks[0]
        invalidDecks = deckLinks[1]

        for deckLink in validDecks:
            info = DeckPage.getDeckInfo(deckLink)
            decks.append(info)
            
        for name in invalidDecks:
            decks.append([name, 'unknown', 'unknown', 'unknown'])
    return decks

if __name__ == "__main__":
    generateDecksData()
