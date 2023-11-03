#!/usr/bin/env python3

# Jakobsen, T. (1995). A FAST METHOD FOR CRYPTANALYSIS OF SUBSTITUTION CIPHERS. Cryptologia, 19(3), CZECH_ALPHABET_SIZE5–274. doi:10.1080/0161-119591883944

import sys
from string import ascii_lowercase
import numpy as np
from collections import Counter
from simanneal import Annealer
from utils import mono_decrypt, read_text, toidx, fitness, letters_by_frequency
import random

# Import our constants
from consts import (
    CZECH_ALPHABET_SIZE,
    CZECH_LETTER_FREQUENCIES,
    CZECH_LETTERS_BY_FREQUENCY,
    CZECH_DIGRAM_MATRIX,
)

CZECH_AVERAGE_FITNESS = -4.359122494441955
CZECH_TETRAGRAM_MATRIX = np.load("tetragrams.pickle", allow_pickle=True)

def get_digraph_matrix(text):
    arr = np.zeros((CZECH_ALPHABET_SIZE, CZECH_ALPHABET_SIZE), dtype=float)

    N = 0
    for i in range(len(text) - 1):
        key = text[i:i+2]

        row, col = CZECH_LETTERS_BY_FREQUENCY.index(key[0]), CZECH_LETTERS_BY_FREQUENCY.index(key[1])

        arr[row][col] += 1
        N += 1

    sum = 0.0
    for row in range(CZECH_ALPHABET_SIZE):
        for col in range(CZECH_ALPHABET_SIZE):
            arr[row][col] = round(arr[row][col] * 100 / N, 3)
            sum += arr[row][col]

    return arr

class Decipher(Annealer):

    def __init__(self, initial_state, cipher_text, matrix):
        self.cipher_text = cipher_text
        self.matrix = matrix

        super(Decipher, self).__init__(initial_state=initial_state)

    def move(self):
        initial_energy = self.energy()

        a = random.randint(0, len(self.state) - 1)
        b = random.randint(0, len(self.state) - 1)

        # swap the letters in the key
        self.state[a], self.state[b] = self.state[b], self.state[a]

        return self.energy() - initial_energy

    def energy(self):
        text = mono_decrypt(self.cipher_text, self.state)

        return -fitness(text, self.matrix) * 100

def main(filename):
    cipher_text = read_text(filename)

    print(cipher_text)

    # generate the initial key by frequency
    init_state = letters_by_frequency(cipher_text)

    cypher = Decipher(init_state, cipher_text, CZECH_TETRAGRAM_MATRIX)
    cypher.set_schedule(cypher.auto(minutes=1))
    cypher.copy_strategy = "slice"

    state, e = cypher.anneal()

    print()
    print(f'key: {"".join(state)}')
    print(mono_decrypt(cipher_text, state))

if __name__ == '__main__':
    main(sys.argv[1])
