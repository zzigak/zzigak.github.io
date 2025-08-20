# Query for: node_29:cc_python_29
# =========================
"""
Asterix, Obelix and their temporary buddies Suffix and Prefix has finally found the Harmony temple. However, its doors were firmly locked and even Obelix had no luck opening them.

A little later they found a string s, carved on a rock below the temple's gates. Asterix supposed that that's the password that opens the temple and read the string aloud. However, nothing happened. Then Asterix supposed that a password is some substring t of the string s.

Prefix supposed that the substring t is the beginning of the string s; Suffix supposed that the substring t should be the end of the string s; and Obelix supposed that t should be located somewhere inside the string s, that is, t is neither its beginning, nor its end.

Asterix chose the substring t so as to please all his companions. Besides, from all acceptable variants Asterix chose the longest one (as Asterix loves long strings). When Asterix read the substring t aloud, the temple doors opened. 

You know the string s. Find the substring t or determine that such substring does not exist and all that's been written above is just a nice legend.

Input

You are given the string s whose length can vary from 1 to 106 (inclusive), consisting of small Latin letters.

Output

Print the string t. If a suitable t string does not exist, then print "Just a legend" without the quotes.

Examples

Input

fixprefixsuffix


Output

fix

Input

abcdabc


Output

Just a legend
"""

# Original Problem: node_29:cc_python_29
# =========================
from fractions import Fraction
import bisect
import os
from collections import Counter
import bisect
from collections import defaultdict
import math
import random
import heapq as hq
from math import sqrt
import sys
from functools import reduce, cmp_to_key
from collections import deque
import threading
from itertools import combinations
from io import BytesIO, IOBase
from itertools import accumulate


# sys.setrecursionlimit(200000)
# input = io.BytesIO(os.read(0, os.fstat(0).st_size)).readline


def input():
    return sys.stdin.readline().strip()


def iinput():
    return int(input())


def tinput():
    return input().split()


def rinput():
    return map(int, tinput())


def rlinput():
    return list(rinput())


mod = int(1e9)+7


def factors(n):
    return set(reduce(list.__add__,
                      ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))


# ----------------------------------------------------
# sys.stdin = open('input.txt', 'r')
# sys.stdout = open('output.txt', 'w')


def zfunction(s):
    n = len(s)
    l, r = 0, 0
    Z = [0]*n
    for i in range(1, n):
        if i <= r:
            Z[i] = min(r-i+1, Z[i-l])
        while i+Z[i] < n and s[Z[i]] == s[i+Z[i]]:
            Z[i] += 1
        if i+Z[i]-1 > r:
            l, r = i, i+Z[i]-1
    return Z


s = input()
n = len(s)
Z = zfunction(s)
# for i in range(n):
#     Z[i] = min(i,Z[i])
# print(Z)
third = []
for i in range(n):
    if i+Z[i] == n:
        third.append(Z[i])
ll = len(third)
# flg = False
# print(Z)
# print(third)
ans = ""
if ll == 0:
    ans = 'Just a legend'
elif ll == 1:
    if Z.count(third[0]) >= 2 or max(Z) > third[0]:
        ans = s[:third[0]]
    else:
        ans = 'Just a legend'
else:
    if Z.count(third[0]) >= 2 or max(Z) > third[0]:
        ans = s[:third[0]]
    else:
        ans = s[:third[1]]
print(ans)

