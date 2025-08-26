# Query for: node_29:cc_python_29
# =========================
"""
Permutation p is an ordered set of integers p1, p2, ..., pn, consisting of n distinct positive integers, each of them doesn't exceed n. We'll denote the i-th element of permutation p as pi. We'll call number n the size or the length of permutation p1, p2, ..., pn.

We'll call position i (1 ≤ i ≤ n) in permutation p1, p2, ..., pn good, if |p[i] - i| = 1. Count the number of permutations of size n with exactly k good positions. Print the answer modulo 1000000007 (109 + 7).

Input

The single line contains two space-separated integers n and k (1 ≤ n ≤ 1000, 0 ≤ k ≤ n).

Output

Print the number of permutations of length n with exactly k good positions modulo 1000000007 (109 + 7).

Examples

Input

1 0


Output

1


Input

2 1


Output

0


Input

3 2


Output

4


Input

4 1


Output

6


Input

7 4


Output

328

Note

The only permutation of size 1 has 0 good positions.

Permutation (1, 2) has 0 good positions, and permutation (2, 1) has 2 positions.

Permutations of size 3:

  1. (1, 2, 3) — 0 positions
  2. <image> — 2 positions
  3. <image> — 2 positions
  4. <image> — 2 positions
  5. <image> — 2 positions
  6. (3, 2, 1) — 0 positions
"""

# Original Problem: node_29:cc_python_29
# =========================
mod=10**9+7
n,k=map(int,input().split())

A=[0]*(n+1)
B=[0]*(n+1)
C=[0]*(n+1)
F=[0]*(n+1)
G=[0]*(n+1)

F[0]=G[0]=1
for i in range(1,n+1):
	G[i]=F[i]=F[i-1]*i%mod
	G[i]=pow(F[i],(mod-2),mod)

for i in range(0,n):
	if i*2>n:
		break
	B[i]=(F[n-i]*G[i]*G[n-i*2])%mod
for i in range(0,n//2+1):
	for j in range(0,n//2+1):
		A[i+j]=(A[i+j]+B[i]*B[j])%mod
for i in range(0,n+1):
	A[i]=A[i]*F[n-i]%mod
for i in range(0,n+1):
	for j in range(0,i+1):
		C[j]=(C[j]+A[i]*F[i]*G[j]*G[i-j]*(1-(i-j)%2*2))%mod
print(C[k]%mod)

