#!/usr/bin/env python3

from collections import Counter
from utils import read_text, toidx, tochr
import numpy as np
from consts import CZECH_ALPHABET_SIZE
import sys

FREQ_NONE = 0.0

MATRIX_SIZE = (CZECH_ALPHABET_SIZE)

def gen_monograms(text):
    arr = np.zeros(MATRIX_SIZE, dtype=float)

    N = 0
    for i in range(len(text)):
        a = toidx(text[i])

        arr[a] += 1

        N += 1

    for a in range(CZECH_ALPHABET_SIZE):
        if arr[a] == 0.0:
            arr[a] = FREQ_NONE
        else:
            arr[a] = arr[a]/N

    return arr

if __name__ == '__main__':
    text = read_text(sys.argv[1])

    monograms = gen_monograms(text)

    monograms.dump("monograms.pickle")

    print("double monograms[] = {")
    for i in monograms:
        print(f"	{i},")
    print("	};")
