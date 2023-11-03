#!/usr/bin/env python3

import sys

from lmdbm import Lmdb
from collections import Counter
from unidecode import unidecode

def main():
    words = {}
    print(f"reading from {sys.argv[1]}")
    with open(sys.argv[1], "r") as file:
        for line in file:
            word = unidecode(line.strip().lower())
            words[word] = ""
    print(f"writing to {sys.argv[2]}")
    with Lmdb.open(sys.argv[2], "c") as db:
        db.update(words)

if __name__ == '__main__':
    main()
