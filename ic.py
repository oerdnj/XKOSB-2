#!/usr/bin/env python3

import sys
import consts
import numpy as np
from consts import CZECH_INDEX_OF_COINCIDENCE
from utils import index_of_coincidence, indexes_of_coincidence, read_text

if __name__ == '__main__':
    cipher_text = read_text(sys.argv[1])

    print("Czech IoC: {0:0.5f}".format(CZECH_INDEX_OF_COINCIDENCE))
    print("Text  IoC: {0:0.5f}".format(index_of_coincidence(cipher_text)))

    ics = indexes_of_coincidence(cipher_text)

    for ic in ics[:5]:
        print(ic)
