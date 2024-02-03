from enum import Enum

CARDS = ["bc10", "bc2", "bc4", "bc3", "bc9", "bca", "fc10", "fc2", "fc4", "fc3", "fc9", "fca", "gc10", "gc2", "gc4",
         "gc3", "gc9", "gca", "rc10", "rc2", "rc4", "rc3", "rc9", "rca"]
CARDSFULL = ["bc10", "bc4", "bc2", "bc3", "bc9", "bca", "fc10", "fc4", "fc2", "fc3", "fc9", "fca", "gc10", "gc4", "gc2",
         "gc3", "gc9", "gca", "rc10", "rc4", "rc2", "rc3", "rc9", "rca"]
IMAGES = ["10bata.png", "4bata.png", "2bata.png", "3bata.png", "9bata.png", "asbata.png", "10verde.png"
    , "4verde.png" , "2verde.png", "3verde.png", "9verde.png", "asverde.png"
    ,"10ghinda.png","4ghinda.png","2ghinda.png","3ghinda.png","9ghinda.png","asghinda.png"
    ,"10rosu.png","4rosu.png","2rosu.png","3rosu.png","9rosu.png","asrosu.png"]


class Suit(Enum):
    RED = 'r'
    GREEN = 'f'
    ACORN = 'g'
    VAN = 'b'


WINNING_CARD_INPUT_FILENAME = 'winning_card.in'
WINNING_CARD_OUTPUT_FILENAME = 'winning_card.out'

SCREEN_WIDTH = 1850
SCREEN_HEIGHT = 1000
