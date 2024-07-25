import requests

class Card:
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