from pprint import pprint
import requests
import os

from pokemontcgsdk import Card
from pokemontcgsdk import Set
from pokemontcgsdk import Type
from pokemontcgsdk import Supertype
from pokemontcgsdk import Subtype
from pokemontcgsdk import Rarity

from pokemontcgsdk import RestClient
from secret import api_key

RestClient.configure(api_key)

def get_splits(path_name):
    head, tail = os.path.split(path_name)
    pth = tail[:-4]
    pth = pth.split('_')
    return pth

def get_card(path_name):
    head, tail = os.path.split(path_name)
    pth = tail[:-4]
    pth = pth.split('_')
    card = Card.find(pth[-1])
    return card

def get_price(path_name):
    head, tail = os.path.split(path_name)
    pth = tail[:-4]
    pth = pth.split('_')
    card = Card.find(pth[-1])
    return card.cardmarket.prices.averageSellPrice

def get_image(path_name):
    head, tail = os.path.split(path_name)
    pth = tail[:-4]
    pth = pth.split('_')
    card = Card.find(pth[-1])
    return card.images.large

def get_price_c(c):
    return c.cardmarket.prices.averageSellPrice
    
# run this to download every pic lol
if __name__ == '__main__':

    # p = get_card('/home/jestone/tcgdetector/card_imgs_desc/Absol G_1_Rare Holo_pl3-1.jpg')
    # print(p.images.large)
    # exit(0)

    # grab all Card objects (count 18,685)
    cards = Card.all()

    # write image links to CSV from array cards of Card objects

    '''
    with open('card_links.csv', 'w') as handler:
        for i, card in enumerate(cards):
            handler.write(f'{card.images.large},{card.images.small},\n')
    ''' 

    # download images from array cards of Card objects

    for i, card in enumerate(cards):
        img_data = requests.get(card.images.large).content
        with open(f'./card_imgs_desc/{card.name}_{card.number}_{card.rarity}_{card.id}.jpg','wb') as handler:
            handler.write(img_data)
