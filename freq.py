#!/usr/bin/env python3

import sys
from pprint import pprint
import numpy as np
from utils import read_text, index_of_coincidence

CZECH_LETTER_FREQUENCIES = {}

def letter_freq(text):
    from collections import Counter
    from string import ascii_lowercase

    freqs = Counter(text)

    N = len(text)

    if N == 0:
        return 0.0

    for c in freqs:
        freqs[c] = freqs[c] * 100 / N

    return freqs

def count_freq(text):

    arr = np.zeros((26, 26), dtype=float)

    N = 0
    for i in range(len(text) - 1):
        key = text[i:i+2]
        row, col = ord(key[0]) - ord('a'), ord(key[1]) - ord('a')

        arr[row][col] += 1
        N += 1

    for row in range(26):
        for col in range(26):
            arr[row][col] = arr[row][col] * 100 / N

    return arr

if __name__ == '__main__':
    from string import ascii_lowercase

    text = read_text(sys.argv[1])

    letterFreq = letter_freq(text)
    indexOfCoincidence = index_of_coincidence(text)

    print("""
# This file is autogenerated using freq.py <file.txt>

import numpy as np

# We are using English alphabet for Czech language
# This could support the full Czech alphabet, but it would need to adjusted
CZECH_ALPHABET_SIZE = 26

# Gymnázium Josefa Božka has gratiously provided quite nice collection
# of Czech books at https://www.gmct.cz/media/files/library/PDF/
#
# The frequencies were generated using 119 Czech books (old and new
# alike) containing roughly 7301763 words
        """)

    print()
    print("CZECH_INDEX_OF_COINCIDENCE = {0:0.5f}".format(indexOfCoincidence))

    print()
    print("CZECH_LETTER_FREQUENCIES = {")
    for s in letterFreq.most_common():
        f = "{0:0.4f}".format(s[1])
        print(f'    "{s[0]}": {f},')
    print("}")
    print()
    print('CZECH_LETTERS_BY_FREQUENCY = "".join(CZECH_LETTER_FREQUENCIES)')
    print()

    print("# List of letter indices where number of occurrences is according to the corresponding")
    print("# letter's frequency in Czech, used to generate random pairs for swapping.")
    print("RANDOM_INDEX_DISTRIBUTION = []")
    print("for letter, frequency in CZECH_LETTER_FREQUENCIES.items():")
    print("    index = CZECH_LETTERS_BY_FREQUENCY.index(letter)")
    print("    RANDOM_INDEX_DISTRIBUTION.extend([index] * int(100 * frequency))")
    print()

    CZECH_LETTERS_BY_FREQUENCY = "".join([s[0] for s in letterFreq.most_common()])
    for c in ascii_lowercase:
        if c not in CZECH_LETTERS_BY_FREQUENCY:
            CZECH_LETTERS_BY_FREQUENCY += c


    digram_matrix0 = count_freq(text)

    digram_matrix = np.zeros((26, 26))
    for rowc in ascii_lowercase:
        for colc in ascii_lowercase:
            row0 = ord(rowc) - ord('a')
            col0 = ord(colc) - ord('a')

            row = CZECH_LETTERS_BY_FREQUENCY.index(rowc)
            col = CZECH_LETTERS_BY_FREQUENCY.index(colc)

            digram_matrix[row][col] = digram_matrix0[row0][col0]


    print("CZECH_DIGRAM_MATRIX = np.array([")
    out = "    #  "
    for c in CZECH_LETTERS_BY_FREQUENCY:
        out += f"{c}      "
    print(f"{out[:-6]}")
    for row in range(26):
        out = "    ["
        for col in range(26):
            out += "{0:0.3f}, ".format(digram_matrix[row][col])
        print(f"{out[:-2]}], # {CZECH_LETTERS_BY_FREQUENCY[row]}")
    print("])")