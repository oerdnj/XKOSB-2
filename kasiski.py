#!/usr/bin/env python3

import sys
from utils import kasiski, read_text

if __name__ == '__main__':
    cipher_text = read_text(sys.argv[1])

    factors = kasiski(cipher_text)

    for factor in factors[:5]:
        print(factor)
