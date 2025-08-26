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

