#!/usr/bin/env python3

from collections import Counter
from utils import read_text, toidx, tochr, fitness
import numpy as np
from consts import CZECH_ALPHABET_SIZE
from math import log10
import sys

FREQ_NONE = -24.0

MATRIX_SIZE = (CZECH_ALPHABET_SIZE, CZECH_ALPHABET_SIZE, CZECH_ALPHABET_SIZE, CZECH_ALPHABET_SIZE)

def gen_tetragrams(text):
    arr = np.zeros(MATRIX_SIZE, dtype=float)

    N = 0
    for i in range(len(text) - 3):
        a = toidx(text[i])
        b = toidx(text[i+1])
        c = toidx(text[i+2])
        d = toidx(text[i+3])

        arr[a][b][c][d] += 1

        N += 1

    for a in range(CZECH_ALPHABET_SIZE):
        for b in range(CZECH_ALPHABET_SIZE):
            for c in range(CZECH_ALPHABET_SIZE):
                for d in range(CZECH_ALPHABET_SIZE):
                    if arr[a][b][c][d] == 0.0:
                        arr[a][b][c][d] = FREQ_NONE
                    else:
                        arr[a][b][c][d] = log10(arr[a][b][c][d]/N)

    return arr

if __name__ == '__main__':
    text = read_text(sys.argv[1])

    tetragrams = gen_tetragrams(text)

    tetragrams.dump("tetragrams.pickle")

    c_arr = np.zeros((CZECH_ALPHABET_SIZE * CZECH_ALPHABET_SIZE * CZECH_ALPHABET_SIZE * CZECH_ALPHABET_SIZE), dtype=float)

    for a in range(CZECH_ALPHABET_SIZE):
        for b in range(CZECH_ALPHABET_SIZE):
            for c in range(CZECH_ALPHABET_SIZE):
                for d in range(CZECH_ALPHABET_SIZE):
                    c_arr[a * CZECH_ALPHABET_SIZE * CZECH_ALPHABET_SIZE * CZECH_ALPHABET_SIZE +
                          b * CZECH_ALPHABET_SIZE * CZECH_ALPHABET_SIZE +
                          c * CZECH_ALPHABET_SIZE +
                          d] = tetragrams[a][b][c][d]

    fit = fitness(text, tetragrams)

    print(f"double average_fitness = {fit};")
    print()
    print("double tetragrams[] = {")
    for i in c_arr:
        print(f"	{i},")
    print("	};")
