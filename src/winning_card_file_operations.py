import os
import re
import json
import subprocess

from constants import CARDS, WINNING_CARD_INPUT_FILENAME, WINNING_CARD_OUTPUT_FILENAME,Suit


def setup_winning_card_input_file(tromf, first_card, second_card, third_card, fourth_card):

    filename = WINNING_CARD_INPUT_FILENAME
    with open(filename, 'r') as file:
        lines = file.readlines()

    cards = CARDS.copy()
    trumps = trump_to_trump_cards(tromf, cards)
    not_trumps = [card for card in cards if card not in trumps]
    played_cards = [second_card, third_card, fourth_card]

    trump_pattern = re.compile(r"^.*tromf\([^)]*\)\..*$")
    first_card_pattern = re.compile("^.*played_first\([^)]*\)\..*$")
    played_card_pattern = re.compile("^played\([^)]*\)\..*$")

    modified_lines = []

    index_trumps = 0
    index_not_trumps = 0
    index_played_cards = 0

    for l in lines:
        if trump_pattern.match(l):
            if l[0] == '-':
                l = "-tromf(" + not_trumps[index_not_trumps] + ").\n"
                index_not_trumps += 1
            else:
                l = "tromf(" + trumps[index_trumps] + ").\n"
                index_trumps += 1
        elif first_card_pattern.match(l):
            l = "played_first(" + first_card + ").\n"
        elif played_card_pattern.match(l):
            l = "played(" + played_cards[index_played_cards] + ").\n"
            index_played_cards += 1
        modified_lines.append(l)

    with open(filename, 'w') as file:
        file.writelines(modified_lines)


def trump_to_trump_cards(trump, cards):
    return [card for card in cards if card[0] == trump.value]


def return_winning_card_from_winning_card_output_file():

    filename = WINNING_CARD_OUTPUT_FILENAME

    with open(filename, 'r') as file:
        output = json.load(file)

    domain_index_of_cards = {}
    duce_list = []
    played_list = []

    for elem in output[0][2]:
        if elem[0] == 'function':
            domain_index_of_cards[elem[1]] = elem[3]
        if elem[0] == 'relation':
            if elem[1] == 'nu_duce':
                duce_list = elem[3]
            elif elem[1] == 'played':
                played_list = elem[3]

    winning_card = None
    played_cards = [card for card in CARDS if played_list[domain_index_of_cards[card]] == 1]

    for card in played_cards:
        if duce_list[domain_index_of_cards[card]] == 0:
            winning_card = card

    return winning_card

def run_mace4():
    commands = [
        "./Prover9Mace4/bin/mace4 -c -f " + WINNING_CARD_INPUT_FILENAME + " | ./Prover9Mace4/bin/interpformat portable > " + WINNING_CARD_OUTPUT_FILENAME]

    # Execute the command silently
    for arg in commands:
        result = subprocess.run(arg, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if result.returncode != 0:
            print("Failed to execute command " + arg)
            exit(-1)

def determine_which_card_wins(tromf, first_card, second_card, third_card, fourth_card):
    setup_winning_card_input_file(tromf, first_card, second_card, third_card, fourth_card)
    run_mace4()
    return return_winning_card_from_winning_card_output_file()

