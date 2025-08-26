# This file contains original problem queries and their corresponding Python code.

# Query for: node_16:cc_python_16
# =========================
"""
Little penguin Polo likes permutations. But most of all he likes permutations of integers from 0 to n, inclusive.

For permutation p = p0, p1, ..., pn, Polo has defined its beauty — number <image>.

Expression <image> means applying the operation of bitwise excluding "OR" to numbers x and y. This operation exists in all modern programming languages, for example, in language C++ and Java it is represented as "^" and in Pascal — as "xor".

Help him find among all permutations of integers from 0 to n the permutation with the maximum beauty.

Input

The single line contains a positive integer n (1 ≤ n ≤ 106).

Output

In the first line print integer m the maximum possible beauty. In the second line print any permutation of integers from 0 to n with the beauty equal to m.

If there are several suitable permutations, you are allowed to print any of them.

Examples

Input

4


Output

20
0 2 1 4 3
"""

# Original Problem: node_16:cc_python_16
# =========================
import sys
from math import gcd,sqrt,ceil
from collections import defaultdict,Counter,deque
from bisect import bisect_left,bisect_right
import math
from itertools import permutations

# input=sys.stdin.readline
# def print(x):
#     sys.stdout.write(str(x)+"\n")

# sys.stdin = open('input.txt', 'r')
# sys.stdout = open('output.txt', 'w')
import os
import sys
from io import BytesIO, IOBase

BUFSIZE = 8192


class FastIO(IOBase):
    newlines = 0

    def __init__(self, file):
        self._fd = file.fileno()
        self.buffer = BytesIO()
        self.writable = "x" in file.mode or "r" not in file.mode
        self.write = self.buffer.write if self.writable else None

    def read(self):
        while True:
            b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
            if not b:
                break
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
        self.newlines = 0
        return self.buffer.read()

    def readline(self):
        while self.newlines == 0:
            b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
            self.newlines = b.count(b"\n") + (not b)
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
        self.newlines -= 1
        return self.buffer.readline()

    def flush(self):
        if self.writable:
            os.write(self._fd, self.buffer.getvalue())
            self.buffer.truncate(0), self.buffer.seek(0)


class IOWrapper(IOBase):
    def __init__(self, file):
        self.buffer = FastIO(file)
        self.flush = self.buffer.flush
        self.writable = self.buffer.writable
        self.write = lambda s: self.buffer.write(s.encode("ascii"))
        self.read = lambda: self.buffer.read().decode("ascii")
        self.readline = lambda: self.buffer.readline().decode("ascii")


sys.stdin, sys.stdout = IOWrapper(sys.stdin), IOWrapper(sys.stdout)
input = lambda: sys.stdin.readline().rstrip("\r\n")

# import sys
# import io, os
# input = io.BytesIO(os.read(0,os.fstat(0).st_size)).readline
def get_sum(bit,i):
    s = 0

    i+=1
    while i>0:
        s+=bit[i]
        i-=i&(-i)

    return s

def update(bit,n,i,v):
    i+=1

    while i<=n:
        bit[i]+=v
        i+=i&(-i)


def modInverse(b,m):
    g = math.gcd(b, m)
    if (g != 1):
        return -1
    else:
        return pow(b, m - 2, m)

def primeFactors(n):

    sa = set()
    sa.add(n)
    while n % 2 == 0:
        sa.add(2)
        n = n // 2


    for i in range(3,int(math.sqrt(n))+1,2):


        while n % i== 0:
            sa.add(i)
            n = n // i

    # sa.add(n)
    return sa


def seive(n):

    pri = [True]*(n+1)
    p = 2
    while p*p<=n:

        if pri[p] == True:

            for i in range(p*p,n+1,p):
                pri[i] = False

        p+=1

    return pri

def debug(n):
    l = [i for i in range(n+1)]
    z = permutations(l)
    maxi = 0
    for i in z:
        fin = 0
        for j in range(n+1):
            fin+=j^i[j]

        maxi = max(maxi,fin)

    return maxi


n = int(input())
hash = defaultdict(int)
ans = [0]*(n+1)
seti = set()
for i in range(n,0,-1):
    if i not in seti:
       z1 = i^int('1'*len((bin(i)[2:])),2)

       seti.add(z1)
       ans[z1] = i
       ans[i] = z1
       # print(ans)

fin = 0
for i in range(n+1):
    fin+=i^ans[i]
print(fin)
print(*ans)


# EoP (End of Problem details for node_16:cc_python_16)
# ######################################################################

# Query for: node_19:cc_python_19
# =========================
"""
Alice has a very important message M consisting of some non-negative integers that she wants to keep secret from Eve. Alice knows that the only theoretically secure cipher is one-time pad. Alice generates a random key K of the length equal to the message's length. Alice computes the bitwise xor of each element of the message and the key (<image>, where <image> denotes the [bitwise XOR operation](https://en.wikipedia.org/wiki/Bitwise_operation#XOR)) and stores this encrypted message A. Alice is smart. Be like Alice.

For example, Alice may have wanted to store a message M = (0, 15, 9, 18). She generated a key K = (16, 7, 6, 3). The encrypted message is thus A = (16, 8, 15, 17).

Alice realised that she cannot store the key with the encrypted message. Alice sent her key K to Bob and deleted her own copy. Alice is smart. Really, be like Alice.

Bob realised that the encrypted message is only secure as long as the key is secret. Bob thus randomly permuted the key before storing it. Bob thinks that this way, even if Eve gets both the encrypted message and the key, she will not be able to read the message. Bob is not smart. Don't be like Bob.

In the above example, Bob may have, for instance, selected a permutation (3, 4, 1, 2) and stored the permuted key P = (6, 3, 16, 7).

One year has passed and Alice wants to decrypt her message. Only now Bob has realised that this is impossible. As he has permuted the key randomly, the message is lost forever. Did we mention that Bob isn't smart?

Bob wants to salvage at least some information from the message. Since he is not so smart, he asks for your help. You know the encrypted message A and the permuted key P. What is the lexicographically smallest message that could have resulted in the given encrypted text?

More precisely, for given A and P, find the lexicographically smallest message O, for which there exists a permutation π such that <image> for every i.

Note that the sequence S is lexicographically smaller than the sequence T, if there is an index i such that Si < Ti and for all j < i the condition Sj = Tj holds. 

Input

The first line contains a single integer N (1 ≤ N ≤ 300000), the length of the message. 

The second line contains N integers A1, A2, ..., AN (0 ≤ Ai < 230) representing the encrypted message.

The third line contains N integers P1, P2, ..., PN (0 ≤ Pi < 230) representing the permuted encryption key.

Output

Output a single line with N integers, the lexicographically smallest possible message O. Note that all its elements should be non-negative.

Examples

Input

3
8 4 13
17 2 7


Output

10 3 28


Input

5
12 7 87 22 11
18 39 9 12 16


Output

0 14 69 6 44


Input

10
331415699 278745619 998190004 423175621 42983144 166555524 843586353 802130100 337889448 685310951
226011312 266003835 342809544 504667531 529814910 684873393 817026985 844010788 993949858 1031395667


Output

128965467 243912600 4281110 112029883 223689619 76924724 429589 119397893 613490433 362863284

Note

In the first case, the solution is (10, 3, 28), since <image>, <image> and <image>. Other possible permutations of key yield messages (25, 6, 10), (25, 3, 15), (10, 21, 10), (15, 21, 15) and (15, 6, 28), which are all lexicographically larger than the solution.
"""

# Original Problem: node_19:cc_python_19
# =========================
def add(x):
    global tree
    now = 0
    tree[now][2] += 1
    for i in range(29, -1, -1):
        bit = (x>>i)&1
        if tree[now][bit]==0:
            tree[now][bit]=len(tree)
            tree.append([0, 0, 0])
        now = tree[now][bit]
        tree[now][2] += 1

def find_min(x):
    global tree
    now = ans = 0
    for i in range(29, -1, -1):
        bit = (x>>i)&1
        if tree[now][bit] and tree[tree[now][bit]][2]:
            now = tree[now][bit]
        else:
            now = tree[now][bit^1]
            ans |= (1<<i)
        tree[now][2] -= 1
    return ans

tree = [[0, 0, 0]]
n = int(input())
a = list(map(int, input().split()))
list(map(add, map(int, input().split())))
[print(x, end=' ') for x in list(map(find_min, a))]


# EoP (End of Problem details for node_19:cc_python_19)
# ######################################################################

# Query for: node_25:cc_python_25
# =========================
"""
Given 2 integers u and v, find the shortest array such that [bitwise-xor](https://en.wikipedia.org/wiki/Bitwise_operation#XOR) of its elements is u, and the sum of its elements is v.

Input

The only line contains 2 integers u and v (0 ≤ u,v ≤ 10^{18}).

Output

If there's no array that satisfies the condition, print "-1". Otherwise:

The first line should contain one integer, n, representing the length of the desired array. The next line should contain n positive integers, the array itself. If there are multiple possible answers, print any.

Examples

Input


2 4


Output


2
3 1

Input


1 3


Output


3
1 1 1

Input


8 5


Output


-1

Input


0 0


Output


0

Note

In the first sample, 3⊕ 1 = 2 and 3 + 1 = 4. There is no valid array of smaller length.

Notice that in the fourth sample the array is empty.
"""

# Original Problem: node_25:cc_python_25
# =========================
u, v = list(map(int, input().split()))
if u > v:
    print(-1)
elif u == 0 and v == 0:
    print(0)
elif u == v:
    print(1)
    print(u)
else:
    a, b, c = u, (v - u) // 2, (v - u) // 2
    d, e = (v - u) // 2 + u, (v - u) // 2
    if d + e == v and d ^ e == u:
        print(2)
        print(d, e)
    elif a+b+c == v and a ^ b ^ c == u:
        print(3)
        print(a, b, c)
    else:
        print(-1)


# End of all problems.
