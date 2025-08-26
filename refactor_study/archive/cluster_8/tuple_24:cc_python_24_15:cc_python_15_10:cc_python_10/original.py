# This file contains original problem queries and their corresponding Python code.

# Query for: node_10:cc_python_10
# =========================
"""
Your task is to calculate the number of arrays such that:

  * each array contains n elements; 
  * each element is an integer from 1 to m; 
  * for each array, there is exactly one pair of equal elements; 
  * for each array a, there exists an index i such that the array is strictly ascending before the i-th element and strictly descending after it (formally, it means that a_j < a_{j + 1}, if j < i, and a_j > a_{j + 1}, if j ≥ i). 

Input

The first line contains two integers n and m (2 ≤ n ≤ m ≤ 2 ⋅ 10^5).

Output

Print one integer — the number of arrays that meet all of the aforementioned conditions, taken modulo 998244353.

Examples

Input


3 4


Output


6


Input


3 5


Output


10


Input


42 1337


Output


806066790


Input


100000 200000


Output


707899035

Note

The arrays in the first example are:

  * [1, 2, 1]; 
  * [1, 3, 1]; 
  * [1, 4, 1]; 
  * [2, 3, 2]; 
  * [2, 4, 2]; 
  * [3, 4, 3].
"""

# Original Problem: node_10:cc_python_10
# =========================
MOD = 998244353


def add(x, y):
    x += y
    while(x >= MOD):
        x -= MOD
    while(x < 0):
        x += MOD
    return x


def mul(x, y):
    return (x * y) % MOD


def binpow(x, y):
    z = 1
    while(y):
        if(y & 1):
            z = mul(z, x)
        x = mul(x, x)
        y >>= 1
    return z


def inv(x):
    return binpow(x, MOD - 2)


def divide(x, y):
    return mul(x, inv(y))


fact = []
N = 200000


def precalc():
    fact.append(1)
    for i in range(N):
        fact.append(mul(fact[i], i + 1))


def C(n, k):
    return divide(fact[n], mul(fact[k], fact[n - k]))


precalc()

NM = input()
[N, M] = NM.split()
N = int(N)
M = int(M)

res = 0

if (N > 2):
    res = mul(C(M, N - 1), mul(N - 2, binpow(2, N - 3)))


print(res)


# EoP (End of Problem details for node_10:cc_python_10)
# ######################################################################

# Query for: node_15:cc_python_15
# =========================
"""
Let's define a function f(p) on a permutation p as follows. Let g_i be the [greatest common divisor (GCD)](https://en.wikipedia.org/wiki/Greatest_common_divisor) of elements p_1, p_2, ..., p_i (in other words, it is the GCD of the prefix of length i). Then f(p) is the number of distinct elements among g_1, g_2, ..., g_n.

Let f_{max}(n) be the maximum value of f(p) among all permutations p of integers 1, 2, ..., n.

Given an integers n, count the number of permutations p of integers 1, 2, ..., n, such that f(p) is equal to f_{max}(n). Since the answer may be large, print the remainder of its division by 1000 000 007 = 10^9 + 7.

Input

The only line contains the integer n (2 ≤ n ≤ 10^6) — the length of the permutations.

Output

The only line should contain your answer modulo 10^9+7.

Examples

Input


2


Output


1

Input


3


Output


4

Input


6


Output


120

Note

Consider the second example: these are the permutations of length 3:

  * [1,2,3], f(p)=1. 
  * [1,3,2], f(p)=1. 
  * [2,1,3], f(p)=2. 
  * [2,3,1], f(p)=2. 
  * [3,1,2], f(p)=2. 
  * [3,2,1], f(p)=2. 



The maximum value f_{max}(3) = 2, and there are 4 permutations p such that f(p)=2.
"""

# Original Problem: node_15:cc_python_15
# =========================
p=10**9+7
import math
def r(l):
    x=1
    for m in l:
        x=x*m%p
    return x
n=int(input())
a,k,x,t=[],int(math.log2(n)),n,0
while x>0:
    a.append(x-x//2)
    x//=2
b=[n//(3*2**i)-n//(6*2**i) for i in range(k+1)]
d=[n//2**i-n//(3*2**i) for i in range(k+1)]
y=r([i for i in range(2,n+1)])
s=k if n<3*2**(k-1) else 0
for j in range(s,k+1):
    e=[a[i] for i in range(j)]+[d[j]]+[b[i] for i in range(j,k)]
    x=y*r(e)%p
    f=r([sum(e[:i+1]) for i in range(k+1)])
    while f>1:
        x*=p//f+1
        f=f*(p//f+1)%p
    t+=x%p
print(t%p)


# EoP (End of Problem details for node_15:cc_python_15)
# ######################################################################

# Query for: node_24:cc_python_24
# =========================
"""
You are given an array a of length 2n. Consider a partition of array a into two subsequences p and q of length n each (each element of array a should be in exactly one subsequence: either in p or in q).

Let's sort p in non-decreasing order, and q in non-increasing order, we can denote the sorted versions by x and y, respectively. Then the cost of a partition is defined as f(p, q) = ∑_{i = 1}^n |x_i - y_i|.

Find the sum of f(p, q) over all correct partitions of array a. Since the answer might be too big, print its remainder modulo 998244353.

Input

The first line contains a single integer n (1 ≤ n ≤ 150 000).

The second line contains 2n integers a_1, a_2, …, a_{2n} (1 ≤ a_i ≤ 10^9) — elements of array a.

Output

Print one integer — the answer to the problem, modulo 998244353.

Examples

Input


1
1 4


Output


6

Input


2
2 1 2 1


Output


12

Input


3
2 2 2 2 2 2


Output


0

Input


5
13 8 35 94 9284 34 54 69 123 846


Output


2588544

Note

Two partitions of an array are considered different if the sets of indices of elements included in the subsequence p are different.

In the first example, there are two correct partitions of the array a:

  1. p = [1], q = [4], then x = [1], y = [4], f(p, q) = |1 - 4| = 3; 
  2. p = [4], q = [1], then x = [4], y = [1], f(p, q) = |4 - 1| = 3. 



In the second example, there are six valid partitions of the array a: 

  1. p = [2, 1], q = [2, 1] (elements with indices 1 and 2 in the original array are selected in the subsequence p); 
  2. p = [2, 2], q = [1, 1]; 
  3. p = [2, 1], q = [1, 2] (elements with indices 1 and 4 are selected in the subsequence p); 
  4. p = [1, 2], q = [2, 1]; 
  5. p = [1, 1], q = [2, 2]; 
  6. p = [2, 1], q = [2, 1] (elements with indices 3 and 4 are selected in the subsequence p).
"""

# Original Problem: node_24:cc_python_24
# =========================
n=int(input())
a=list(map(int,input().split()))
mod=998244353
def ncr(n, r, p):
    # initialize numerator
    # and denominator
    num = den = 1
    for i in range(r):
        num = (num * (n - i)) % p
        den = (den * (i + 1)) % p
    return (num * pow(den,
                      p - 2, p)) % p
a.sort()
print((ncr(2*n,n,mod)*(sum(a[n:])-sum(a[0:n])))%mod)


# End of all problems.
