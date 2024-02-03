#!/usr/bin/env python3
import random
import button
import pygame

from constants import CARDS, SCREEN_WIDTH, SCREEN_HEIGHT, IMAGES, CARDSFULL, Suit
from cruce_file_operations import change_file, interpret_Output
from winning_card_file_operations import determine_which_card_wins


class UI:
    window = None
    cardNonebutton = None
    winning_player_text = None
    winning_player_text_rectangle = None
    font = None
    trump_to_img = {Suit.RED: "resources/trumpimages/red.png",
                    Suit.GREEN: "resources/trumpimages/green.png",
                    Suit.ACORN: "resources/trumpimages/acorn.png",
                    Suit.VAN: "resources/trumpimages/van.png",
                    }

    def __init__(self, width, height, title):
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self.initElements()

    def initElements(self):
        cardNone = pygame.image.load("resources/carticruce/none.png").convert_alpha()
        self.cardNonebutton = button.Button(10, 100, cardNone, 1)

        self.font = pygame.font.Font("resources/Seagram tfb.ttf", 50)
        self.winning_player_text = self.font.render("", True, (255, 255, 255))
        self.winning_player_text_rectangle = self.winning_player_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 200))

    def updateWinningPlayerText(self, msg):
        self.winning_player_text = self.font.render(msg, True, (255, 255, 255))
        self.winning_player_text_rectangle = self.winning_player_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 200))

    def getTrumpImage(self, trump):
        return pygame.transform.scale(pygame.image.load(self.trump_to_img[trump]), (80, 80))


class GameState:
    deck = None
    played_cards = None
    player = None
    trump = None
    first_card = None
    output_info = None
    winner = None

    def __init__(self, player):
        self.deck = Deck()
        self.player = player
        self.played_cards = []
        self.output_info = []

    def initGameState(self):
        self.winner = None
        self.deck = Deck()
        self.played_cards = []
        self.player.hand = []
        self.output_info = []
        self.deck.shuffle()
        self.trump = random.choice(list(Suit))
        print(self.trump)
        self.player.hand = self.deck.deal_cards(6)
        self.played_cards = self.deck.deal_cards(3)
        self.first_card = self.played_cards[0]

    def determineWhichCardsArePlaceable(self):
        change_file(self.player.hand, self.first_card, self.trump)
        allow = interpret_Output()

        img = []
        for i in self.player.hand:
            for j in CARDSFULL:
                if i == j:
                    img.append(IMAGES[CARDSFULL.index(j)])

        # allowed:
        allowed_cards = []
        for i in self.player.hand:
            for j in allow:
                if i == j[0]:
                    print(j[0])
                    if not j[1]:
                        allowed_cards.append("resources/carticruce/close.png")
                    else:
                        allowed_cards.append("resources/carticruce/check.png")

        in_hand_card_screen_pos = [(440, 760), (570, 760), (700, 760), (830, 760), (960, 760), (1090, 760)]

        for i in range(0, len(allowed_cards)):
            self.output_info.append((img[i], allowed_cards[i], in_hand_card_screen_pos[i]))


class Game:
    state = None
    gameUI = None

    def __init__(self):
        self.state = GameState(Player())
        self.gameUI = UI(SCREEN_WIDTH, SCREEN_HEIGHT, "CRUCE")
        self.state.initGameState()

    def updateWindow(self):
        self.gameUI.window.fill((52, 78, 91))

        # trump
        self.gameUI.window.blit(self.gameUI.getTrumpImage(self.state.trump), (430, 360))

        # left
        self.gameUI.cardNonebutton.draw(self.gameUI.window)
        self.gameUI.cardNonebutton.drawAt(self.gameUI.window, 10, 200)
        self.gameUI.cardNonebutton.drawAt(self.gameUI.window, 10, 300)
        self.gameUI.cardNonebutton.drawAt(self.gameUI.window, 10, 400)
        self.gameUI.cardNonebutton.drawAt(self.gameUI.window, 10, 500)

        # up
        self.gameUI.cardNonebutton.drawAt(self.gameUI.window, 590, 10)
        self.gameUI.cardNonebutton.drawAt(self.gameUI.window, 700, 10)
        self.gameUI.cardNonebutton.drawAt(self.gameUI.window, 810, 10)
        self.gameUI.cardNonebutton.drawAt(self.gameUI.window, 920, 10)
        self.gameUI.cardNonebutton.drawAt(self.gameUI.window, 1030, 10)

        # right
        self.gameUI.cardNonebutton.drawAt(self.gameUI.window, 1710, 100)
        self.gameUI.cardNonebutton.drawAt(self.gameUI.window, 1710, 200)
        self.gameUI.cardNonebutton.drawAt(self.gameUI.window, 1710, 300)
        self.gameUI.cardNonebutton.drawAt(self.gameUI.window, 1710, 400)
        self.gameUI.cardNonebutton.drawAt(self.gameUI.window, 1710, 500)

        # CARDS_IN_HAND
        for i in range(0, len(self.state.output_info)):
            image = pygame.image.load("resources/carticruce/" + self.state.output_info[i][0]).convert_alpha()
            imgButton = button.Button(self.state.output_info[i][2][0], self.state.output_info[i][2][1], image, 1)

            # allowed or not
            imgAllowed = pygame.image.load(self.state.output_info[i][1]).convert_alpha()
            imgAllowed1Button = button.Button(self.state.output_info[i][2][0] + 40,
                                              self.state.output_info[i][2][1] - 60, imgAllowed, 1)
            imgAllowed1Button.draw(self.gameUI.window)

            if imgButton.draw(self.gameUI.window) and self.state.output_info[i][
                1] == "resources/carticruce/check.png" and len(
                    self.state.played_cards) != 4:
                self.placeDownCard(i)

                self.determineRoundWinner()
                break

        # cards_down
        img_cards_down = []
        for i in self.state.played_cards:
            for j in CARDSFULL:
                if i == j:
                    img_cards_down.append(IMAGES[CARDSFULL.index(j)])

        imgDown1 = pygame.image.load("resources/carticruce/" + img_cards_down[0]).convert_alpha()
        imgDownButton = button.Button(580, 360, imgDown1, 1)
        imgDownButton.draw(self.gameUI.window)

        imgDown2 = pygame.image.load("resources/carticruce/" + img_cards_down[1]).convert_alpha()
        imgDown2Button = button.Button(730, 360, imgDown2, 1)
        imgDown2Button.draw(self.gameUI.window)

        imgDown3 = pygame.image.load("resources/carticruce/" + img_cards_down[2]).convert_alpha()
        imgDown3Button = button.Button(880, 360, imgDown3, 1)
        imgDown3Button.draw(self.gameUI.window)

        if len(img_cards_down) == 4:
            imgDown4 = pygame.image.load("resources/carticruce/" + img_cards_down[3]).convert_alpha()
            imgDown4Button = button.Button(1030, 360, imgDown4, 1)
            imgDown4Button.draw(self.gameUI.window)

        if self.state.winner is not None:
            winning_player_index = self.state.played_cards.index(self.state.winner)
            if winning_player_index == 3:
                msg = "You won! Congrats!"
            else:
                msg = "Player " + str(winning_player_index + 1) + " won!"
            self.gameUI.updateWinningPlayerText(msg)
            self.gameUI.window.blit(self.gameUI.winning_player_text, self.gameUI.winning_player_text_rectangle)
            #restart button
            imgRestart = pygame.image.load("resources/buttonimages/restart.png").convert_alpha()
            imgRestartButton = button.Button(1230, 360, imgRestart, 1)
            if imgRestartButton.draw(self.gameUI.window):
                GameState.initGameState(self.state)
                self.state.determineWhichCardsArePlaceable()

    def run(self):

        self.state.determineWhichCardsArePlaceable()

        running = True
        while running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            print("cartile jucatorului")
            print(self.state.player.hand)

            self.updateWindow()
            pygame.display.flip()

    def placeDownCard(self, i):
        self.state.played_cards.append(self.state.player.hand[i])
        self.state.player.hand.remove(self.state.player.hand[i])
        self.state.output_info.pop(i)

    def determineRoundWinner(self):
        self.state.winner = determine_which_card_wins(self.state.trump, *self.state.played_cards)


class Deck:
    cards = None

    def __init__(self):
        self.cards = CARDS.copy()

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_cards(self, number_of_cards):
        cards = []
        for _ in range(0, number_of_cards):
            cards.append(self.cards.pop())
        return cards


class Player:
    hand = None

    def __init__(self):
        self.hand = []


if __name__ == "__main__":
    pygame.init()

    gameInstance = Game()
    gameInstance.run()

    pygame.quit()