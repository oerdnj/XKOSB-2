#!/usr/bin/env python3

import sys
from collections import Counter
from consts import CZECH_LETTER_FREQUENCIES, CZECH_INDEX_OF_COINCIDENCE, CZECH_ALPHABET_SIZE
from utils import index_of_coincidence, read_text, mono_encrypt, mono_decrypt, letter_freq, looks_like_text, gen_caesar_table

def caesar_encrypt(input, n):
    return mono_encrypt(input, gen_caesar_table(n))

def caesar_decrypt(input, n):
    return mono_decrypt(input, gen_caesar_table(n))

def caesar_guess(db, text):
    f = letter_freq(text)
    input_mc = f.most_common(CZECH_ALPHABET_SIZE)
    freq_mc  = Counter(CZECH_LETTER_FREQUENCIES).most_common(CZECH_ALPHABET_SIZE)


    assert(len(input_mc) == CZECH_ALPHABET_SIZE)
    assert(len(freq_mc) == CZECH_ALPHABET_SIZE)

    found = None
    i = 0
    for c in freq_mc:
        i += 1
        key = ord(input_mc[0][0]) - ord(c[0])
        if key < 0:
            key += CZECH_ALPHABET_SIZE
        elif key > CZECH_ALPHABET_SIZE:
            key -= CZECH_ALPHABET_SIZE
        dt = caesar_decrypt(text, key)
        found = looks_like_text(db, dt)
        if found > len(dt) / 4 / 2:
            return key, i, dt

    return None, i, None


def usage():
    print(f"{sys.argv[0]} [encrypt=key|decrypt=key|guess] text")
    sys.exit(1)


def main(db):
    from pprint import pprint

    if len(sys.argv) != 3:
        usage()

    op = sys.argv[1]
    text = read_text(sys.argv[2])

    if op[0] == "e":
        try:
            i = op.index("=")
            key = int(op[i+1:])
        except:
            print("Invalid key")
            usage()
        print(caesar_encrypt(text, key))
    elif op[0] == "d":
        try:
            i = op.index("=")
            key = int(op[i+1:])
        except:
            print("Invalid key")
            usage()
        print(caesar_decrypt(text, key))
    elif op[0] == "g":
        ioc = index_of_coincidence(text)

        if ioc < CZECH_INDEX_OF_COINCIDENCE - 0.005 or ioc > CZECH_INDEX_OF_COINCIDENCE + 0.005:
            print("WARNING: This doesn't look like Czech monoalphabetical cipher")

        key, steps, found = caesar_guess(db, text)

        if key is not None:
            print(f"Found in {steps} steps; Key is {key}")
            print(found)
        else:
            print("Result not found, is this Caesar's cipher?")
    else:
        print("Invalid operation")
        usage()


if __name__ == '__main__':
    from lmdbm import Lmdb
    with Lmdb.open("cs.lmdb", "r") as db:
        main(db)
