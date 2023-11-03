#!/usr/bin/env python3

from collections import Counter
from unidecode import unidecode
import sys
import re
import math
import numpy as np
from consts import CZECH_INDEX_OF_COINCIDENCE, CZECH_ALPHABET_SIZE
from string import ascii_lowercase

def normalize(input):
    '''
    Remove unicode, upper case and non-alpha characters from the input.
    '''

    re_alpha = re.compile(r'[a-z]')

    return "".join(re_alpha.findall(unidecode(input).lower()))

def index_of_coincidence(input):
    '''
    Formula for IOC: <https://en.wikipedia.org/wiki/Index_of_coincidence>
    c * ((n_a/N * (n_a - 1)/(N - 1)) + (n_b/N * (n_b - 1)/(N - 1)) + ... + (n_z/N * (n_z - 1)/(N - 1))
    Where:
    * c is is the normalizing coefficient (26 for Czech without accents);
    * n_a is the number of times the letter "a" appears in the text;
    * n_b is the number of times the letter "b" appears in the text;
    * [...]
    * n_z is the number of times the letter "z" appears in the text;
    * N is the length of the text
    '''

    letterCounts = Counter(input)
    N = len(input)

    if N == 0:
        return 0.0

    num = sum(ni * (ni-1) for ni in letterCounts.values())
    den = N * (N - 1)

    if (den == 0):
        return 0.0

    total = (26 * num) / (N * (N - 1))

    return round(total, 5)

def indexes_of_coincidence(text, min_num = 2):
    indexes = {}

    for i in range(min_num, 10):
        ics = []
        for j in range(i):
            t = ""
            for x in range(j, len(text), i):
                t += text[x]
            ics.append(index_of_coincidence(t))
        indexes[i] = ics

    scores = Counter()
    out = []
    for i in indexes:
        num = 0.0
        den = 0
        for index in indexes[i]:
            num += index
            den += 1
        total = num / den
        if total > CZECH_INDEX_OF_COINCIDENCE - 0.005:
            scores[i] = total

    return scores.most_common()

def kasiski_compute(text, found, k, word):
    p = found[k][word]

    # assuming len(p) > 1
    factor = p[1] - p[0]
    for i in range(2, len(p)):
        factor = math.gcd(factor, p[i] - p[i - 1])

    return factor

def kasiski(text, min_num = 2):
    factors = Counter()
    words = {}

    found = {}
    for k in range(min_num, len(text)):
        found[k] = {}
        no_match = True
        for i in range(0, len(text) - k):
            word = text[i:i+k]
            if word not in found[k]:
                found[k][word] = [i]
            else:
                found[k][word].append(i)
                no_match = False

        if no_match:
            break

        for word in found[k]:
            if len(found[k][word]) > 2:
                factor = kasiski_compute(text, found, k, word)

                if factor not in factors:
                    factors[factor] = len(word)
                elif factors[factor] < len(word):
                        factors[factor] = len(word)

                if factor not in words:
                    words[factor] = [word]
                else:
                    words[factor].append(word)

    out = []
    for factor, wlen in factors.most_common():
        out.append((factor, words[factor][::-1]))
        if factor == 1:
            break

    return out

def read_text(filename):
    if filename == "-":
        cipher_text = "".join(sys.stdin.readlines())
    else:
        with open(filename, "r") as f:
            cipher_text = f.read()

    return normalize(cipher_text)

def gen_caesar_table(n):
    return ascii_lowercase[n:] + ascii_lowercase[:n]

def mono_encrypt(input, key):
    assert(len(key) == CZECH_ALPHABET_SIZE)
    # prepare the forward table for the key
    table = {}
    for c in range(CZECH_ALPHABET_SIZE):
        table[chr(c + ord('a'))] = key[c]

    output = ""
    for c in input:
        output += table[c]

    return output

def mono_decrypt(input, key):
    # prepare the reverse table for the key
    table = {}
    for c in range(CZECH_ALPHABET_SIZE):
        table[key[c]] = chr(c + ord('a'))

    assert(len(table) == CZECH_ALPHABET_SIZE)

    output = ""
    for c in input:
        output += table[c]

    return output

def letter_freq(text):
    from collections import Counter

    letterCounts = Counter(text)
    N = len(text)

    f = Counter()
    for i in range(ord('a'), ord('z') + 1):
        c = chr(i)
        f[c] = letterCounts[c] * 100 / N

    return f

def looks_like_text(db, ot):
    found = 0
    for i in range(len(ot) - 4):
        for n in range(7, 4, -1):
            s = ot[i:i+n]
            #print(f"looking up {s}")
            if s in db:
                # print(f"found {s} in the db")
                found += 1

    return found

def toidx(c):
    return ord(c) - ord('a')

def tochr(c):
    return chr(c + ord('a'))

def fitness(text, matrix):
    total = 0.0
    N = 0
    for i in range(len(text) - 3):
        a = toidx(text[i])
        b = toidx(text[i+1])
        c = toidx(text[i+2])
        d = toidx(text[i+3])

        total += matrix[a][b][c][d]

        N += 1

    return total / N

def letters_by_frequency(text):
    s = Counter(text)

    f = [letter[0] for letter in s.most_common()]

    # append any missing characters
    for c in ascii_lowercase:
        if c not in f:
            f += c

    return f
