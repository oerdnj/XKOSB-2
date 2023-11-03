# Mono/Poly Cipher Solver

The project consist of couple of utilities in Python to help breaking
ciphers and a C program from [4] adapted for the Czech language.

The cipher breaking tools are:
1. ic.py [file|-] - generate Index of Coincidence for mono and polyalphabetic ciphers
2. kasiski.py [file|-] - Use Kasiski's Test to guess the polyalphabetic cipher key length(s)
3. caesar.py [encrypt=N|decrypt=N|guess] [<file>|-] - Caesar's cipher
4. multiplicative.py [encrypt=N|decrypt=N|guess] [file|-] - Multiplicative cipher
5. mono.py [encrypt=KEY|decrypt=KEY] [file|-] - Generic monoalphabetic cipher
6. mono-guess-simanneal1.py [file|-] - Simulated Annealing with Tetragrams Fitness function
7. mono-guess-lahc1.py [file|-] - Late Acceptance Hill Climbing with Tetragrams Fitness function
8. slippery/ - Slippery Hill Climibing from [4] with Czech language monogram and tetragram frequencies

Couple of utilities:
1. gen_monograms.py [corpus] - generate single letter (monogram) frequencies from corpus file
2. gen_tetragrams.py [corpus] - generate tetragrams frequencies from corpus file
3. freq.py [corpus] - generate consts.py
4. import_dict.py - import dictionary into lmdb file

Notes:
1. The Czech word dictionary was generated using: aspell dump master cs > cs.dict
2. The Czech corpus was generated using PDF books found at Gymnázium
   Josefa Božka website, converted tto text with pdftotext and
   concatenated into single library file

References:
1. Helen Fouché Gaines, “Cryptanalysis: A Study of Ciphers and Their Solution.” New Dover ed. (New York: Dover Publications, Inc., 1956). https://archive.org/details/cryptanalysis00heel
2. Dunin, E. and Schmeh K. “Codebreaking: A Practical Guide.” (San Francisco: No Starch Press, 2023).
3. Jakobsen, Thomas. “A Fast Method for Cryptanalysis of Substitution Ciphers.” Cryptologia 19 (1995): 265-274.
4. Kaeding, Thomas. “Slippery hill-climbing technique for ciphertext-only cryptanalysis of periodic polyalphabetic substitution ciphers.” Cryptologia 44 (2020): 205 - 222.