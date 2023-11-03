#!/usr/bin/env python3

import sys
from collections import Counter
from consts import CZECH_LETTER_FREQUENCIES, CZECH_INDEX_OF_COINCIDENCE, CZECH_ALPHABET_SIZE
from utils import index_of_coincidence, read_text, mono_encrypt, mono_decrypt, letter_freq, looks_like_text, gen_caesar_table

'''
References:
1. https://www.dcode.fr/multiplicative-cipher
'''

COPRIMES_26 = [3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]

# Init the tables
MTE = {}
MTD = {}

for key in COPRIMES_26:
    MTE[key] = {}
    MTD[key] = {}
    for c in range(ord('a'), ord('z') + 1):
        d = chr(c)
        e = chr(ord('a') + (((c - ord('a')) * key) % 26))
        MTE[key][d] = e
        MTD[key][e] = d
    assert(len(MTE[key]) == 26)
    assert(len(MTD[key]) == 26)

def multi_encrypt(input, n):
    assert(n in COPRIMES_26)
    ct = ""
    for c in input:
        ct += MTE[n][c]

    return ct


def multi_decrypt(input, n):
    assert(n in COPRIMES_26)

    ot = ""
    for c in input:
        ot += MTD[n][c]

    return ot


def multi_key(c, freq_mc):
    counter = Counter()
    for key in COPRIMES_26:
        i = 0
        for (cc, ff) in freq_mc:
            i += 1
            if cc == 'a':
                continue
            if MTD[key][c] == cc:
                counter[key] = i
                break

    return counter.most_common()[-1][0]


def multi_guess(db, text):
    f = letter_freq(text)

    input_mc = f.most_common(26)
    freq_mc  = Counter(CZECH_LETTER_FREQUENCIES).most_common(26)

    assert(len(input_mc) == 26)
    assert(len(freq_mc) == 26)

    foundCount = Counter()

    keys = []
    for (c, freq) in input_mc:
        if c == 'a':     # A is always A
            continue
        keys.append(multi_key(c, freq_mc))

    i = 0
    for key in keys:
        dt = multi_decrypt(text, key)
        found = looks_like_text(db, dt)
        if found > len(dt) / 4 / 2:
            return key, i, dt
        i += 1

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
        print(multi_encrypt(text, key))
    elif op[0] == "d":
        try:
            i = op.index("=")
            key = int(op[i+1:])
        except:
            print("Invalid key")
            usage()
        print(multi_decrypt(text, key))
    elif op[0] == "g":
        ioc = index_of_coincidence(text)

        if ioc < CZECH_INDEX_OF_COINCIDENCE - 0.005 or ioc > CZECH_INDEX_OF_COINCIDENCE + 0.005:
            print("WARNING: This doesn't look like Czech monoalphabetical cipher")

        key, steps, found = multi_guess(db, text)

        if key is not None:
            print(f"Found in {steps} steps; Key is {key}")
            print(found)
        else:
            print("Result not found, is this Multiplicative cipher?")
    else:
        print("Invalid operation")
        usage()


if __name__ == '__main__':
    from lmdbm import Lmdb
    with Lmdb.open("cs.lmdb", "r") as db:
        main(db)
