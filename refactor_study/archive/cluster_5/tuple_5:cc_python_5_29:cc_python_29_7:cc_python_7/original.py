# This file contains original problem queries and their corresponding Python code.

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


# EoP (End of Problem details for node_29:cc_python_29)
# ######################################################################

# Query for: node_5:cc_python_5
# =========================
"""
The Romans have attacked again. This time they are much more than the Persians but Shapur is ready to defeat them. He says: "A lion is never afraid of a hundred sheep". 

Nevertheless Shapur has to find weaknesses in the Roman army to defeat them. So he gives the army a weakness number.

In Shapur's opinion the weakness of an army is equal to the number of triplets i, j, k such that i < j < k and ai > aj > ak where ax is the power of man standing at position x. The Roman army has one special trait — powers of all the people in it are distinct.

Help Shapur find out how weak the Romans are.

Input

The first line of input contains a single number n (3 ≤ n ≤ 106) — the number of men in Roman army. Next line contains n different positive integers ai (1 ≤ i ≤ n, 1 ≤ ai ≤ 109) — powers of men in the Roman army. 

Output

A single integer number, the weakness of the Roman army. 

Please, do not use %lld specificator to read or write 64-bit integers in C++. It is preffered to use cout (also you may use %I64d).

Examples

Input

3
3 2 1


Output

1


Input

3
2 3 1


Output

0


Input

4
10 8 3 1


Output

4


Input

4
1 5 4 3


Output

1
"""

# Original Problem: node_5:cc_python_5
# =========================
from sys import stdin


class order_tree:
    def __init__(self, n):
        self.tree, self.n = [[0, 0] for _ in range(n << 1)], n

    # get interval[l,r)
    def query(self, r, col):
        res = 0
        l = self.n
        r += self.n

        while l < r:
            if l & 1:
                res += self.tree[l][col]
                l += 1

            if r & 1:
                r -= 1
                res += self.tree[r][col]

            l >>= 1
            r >>= 1

        return res

    def update(self, ix, val, col):
        ix += self.n

        # set new value
        self.tree[ix][col] += val

        # move up
        while ix > 1:
            self.tree[ix >> 1][col] = self.tree[ix][col] + self.tree[ix ^ 1][col]
            ix >>= 1


def fast3():
    import os, sys, atexit
    from io import BytesIO
    sys.stdout = BytesIO()
    _write = sys.stdout.write
    sys.stdout.write = lambda s: _write(s.encode())
    atexit.register(lambda: os.write(1, sys.stdout.getvalue()))
    return BytesIO(os.read(0, os.fstat(0).st_size)).readline


input = fast3()
n, a = int(input()), [int(x) for x in input().split()]
tree, ans = order_tree(n), 0
mem = {i: j for j, i in enumerate(sorted(a))}

for i in range(n - 1, -1, -1):
    cur = mem[a[i]]
    ans += tree.query(cur, 1)
    tree.update(cur, 1, 0)
    tree.update(cur, tree.query(cur, 0), 1)

print(ans)


# EoP (End of Problem details for node_5:cc_python_5)
# ######################################################################

# Query for: node_7:cc_python_7
# =========================
"""
In Morse code, an letter of English alphabet is represented as a string of some length from 1 to 4. Moreover, each Morse code representation of an English letter contains only dots and dashes. In this task, we will represent a dot with a "0" and a dash with a "1".

Because there are 2^1+2^2+2^3+2^4 = 30 strings with length 1 to 4 containing only "0" and/or "1", not all of them correspond to one of the 26 English letters. In particular, each string of "0" and/or "1" of length at most 4 translates into a distinct English letter, except the following four strings that do not correspond to any English alphabet: "0011", "0101", "1110", and "1111".

You will work with a string S, which is initially empty. For m times, either a dot or a dash will be appended to S, one at a time. Your task is to find and report, after each of these modifications to string S, the number of non-empty sequences of English letters that are represented with some substring of S in Morse code.

Since the answers can be incredibly tremendous, print them modulo 10^9 + 7.

Input

The first line contains an integer m (1 ≤ m ≤ 3 000) — the number of modifications to S. 

Each of the next m lines contains either a "0" (representing a dot) or a "1" (representing a dash), specifying which character should be appended to S.

Output

Print m lines, the i-th of which being the answer after the i-th modification to S.

Examples

Input

3
1
1
1


Output

1
3
7


Input

5
1
0
1
0
1


Output

1
4
10
22
43


Input

9
1
1
0
0
0
1
1
0
1


Output

1
3
10
24
51
109
213
421
833

Note

Let us consider the first sample after all characters have been appended to S, so S is "111".

As you can see, "1", "11", and "111" all correspond to some distinct English letter. In fact, they are translated into a 'T', an 'M', and an 'O', respectively. All non-empty sequences of English letters that are represented with some substring of S in Morse code, therefore, are as follows.

  1. "T" (translates into "1") 
  2. "M" (translates into "11") 
  3. "O" (translates into "111") 
  4. "TT" (translates into "11") 
  5. "TM" (translates into "111") 
  6. "MT" (translates into "111") 
  7. "TTT" (translates into "111") 



Although unnecessary for this task, a conversion table from English alphabets into Morse code can be found [here](https://en.wikipedia.org/wiki/Morse_code).
"""

# Original Problem: node_7:cc_python_7
# =========================
import os, sys
nums = list(map(int, os.read(0, os.fstat(0).st_size).split()))

MOD = 10 ** 9 + 7
BAD = ([0, 0, 1, 1], [0, 1, 0, 1], [1, 1, 1, 0], [1, 1, 1, 1])

def zfunc(s):
    z = [0] * len(s)
    l = r = 0
    for i in range(1, len(s)):
        if i <= r:
            z[i] = min(r - i + 1, z[i - l])
        while i + z[i] < len(s) and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        if i + z[i] - 1 > r:
            l, r = i, i + z[i] - 1
    return z

n = nums[0]
s = []
sm = 0
ans = []
for i in range(1, n + 1):
    s.append(nums[i])
    cur = 0
    f = [0] * (i + 1)
    f[i] = 1
    for j in range(i - 1, -1, -1):
        for k in range(j, min(j + 4, i)):
            if s[j : k + 1] not in BAD:
                f[j] = (f[j] + f[k + 1])%MOD
    z = zfunc(s[::-1])
    new = i - max(z)
    for x in f[:new]:
        sm = (sm + x)%MOD
    ans.append(sm)
print(*ans, sep='\n')


# End of all problems.
