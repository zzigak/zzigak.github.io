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

