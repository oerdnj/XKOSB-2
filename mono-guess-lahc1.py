#!/usr/bin/env python3

# Jakobsen, T. (1995). A FAST METHOD FOR CRYPTANALYSIS OF SUBSTITUTION CIPHERS. Cryptologia, 19(3), 265–274. doi:10.1080/0161-119591883944

import sys
import numpy as np
import random
from lahc import LateAcceptanceHillClimber
from utils import mono_decrypt, read_text, toidx, fitness, letters_by_frequency

# Import our constants
from consts import (
    CZECH_ALPHABET_SIZE,
    CZECH_LETTER_FREQUENCIES,
    CZECH_LETTERS_BY_FREQUENCY,
    CZECH_DIGRAM_MATRIX,
)

CZECH_AVERAGE_FITNESS = -4.359122494441955
CZECH_TETRAGRAM_MATRIX = np.load("tetragrams.pickle", allow_pickle=True)

class Decipher(LateAcceptanceHillClimber):

    def __init__(self, initial_state, cipher_text, matrix):
        self.cipher_text = cipher_text
        self.matrix = matrix

        super(Decipher, self).__init__(initial_state=initial_state)

    def move(self):
        """Swaps the characters in the key"""

        initial_energy = self.energy()

        a = random.randint(0, len(self.state) - 1)
        b = random.randint(0, len(self.state) - 1)

        # swap the letters in the key
        self.state[a], self.state[b] = self.state[b], self.state[a]

        new_energy = self.energy()

        return new_energy - initial_energy

    def energy(self):
        text = mono_decrypt(self.cipher_text, self.state)

        return -fitness(text, self.matrix) * 100

def main(filename):
    cipher_text = read_text(filename)

    print(cipher_text)

    # generate the initial key by frequency
    init_state = letters_by_frequency(cipher_text)

    LateAcceptanceHillClimber.history_length = 5000
    LateAcceptanceHillClimber.updates_every = 1000

    cypher = Decipher(init_state, cipher_text, CZECH_TETRAGRAM_MATRIX)

    cypher.run()

    print()
    print(f'key: {"".join(cypher.state)}')
    print(mono_decrypt(cipher_text, cypher.state))

if __name__ == '__main__':
    main(sys.argv[1])
