# This file contains original problem queries and their corresponding Python code.

# Query for: node_28:cc_python_28
# =========================
"""
— This is not playing but duty as allies of justice, Nii-chan!

— Not allies but justice itself, Onii-chan!

With hands joined, go everywhere at a speed faster than our thoughts! This time, the Fire Sisters — Karen and Tsukihi — is heading for somewhere they've never reached — water-surrounded islands!

There are three clusters of islands, conveniently coloured red, blue and purple. The clusters consist of a, b and c distinct islands respectively.

Bridges have been built between some (possibly all or none) of the islands. A bridge bidirectionally connects two different islands and has length 1. For any two islands of the same colour, either they shouldn't be reached from each other through bridges, or the shortest distance between them is at least 3, apparently in order to prevent oddities from spreading quickly inside a cluster.

The Fire Sisters are ready for the unknown, but they'd also like to test your courage. And you're here to figure out the number of different ways to build all bridges under the constraints, and give the answer modulo 998 244 353. Two ways are considered different if a pair of islands exist, such that there's a bridge between them in one of them, but not in the other.

Input

The first and only line of input contains three space-separated integers a, b and c (1 ≤ a, b, c ≤ 5 000) — the number of islands in the red, blue and purple clusters, respectively.

Output

Output one line containing an integer — the number of different ways to build bridges, modulo 998 244 353.

Examples

Input

1 1 1


Output

8


Input

1 2 2


Output

63


Input

1 3 5


Output

3264


Input

6 2 9


Output

813023575

Note

In the first example, there are 3 bridges that can possibly be built, and no setup of bridges violates the restrictions. Thus the answer is 23 = 8.

In the second example, the upper two structures in the figure below are instances of valid ones, while the lower two are invalid due to the blue and purple clusters, respectively.

<image>
"""

# Original Problem: node_28:cc_python_28
# =========================
a,b,c = list(map(int, input().split(' ')))


MOD = 998244353

def d(a, b):
	s = 1
	for i in range(a, b+1):
		s*=i
		s%=MOD
	return s




def cnk(n,k):
	s = 1
	for i in range(n-k+1, n+1):
		s*=i
	for i in range(1,k+1):
		s/=i
	return s


def factorial(n):
	s = 1
	for i in range(1, n+1):
		s*=i	
	return s



def pow(a, b):
	c = 1

	while b>0:
		if b%2==0:
			b//=2
			a *=a
			a%=MOD
		else:
			b-=1
			c*=a
			c%=MOD
	return c


def inv(i):
	return pow(i, MOD-2)
"""
def factinv(i):

	return 1.0/factorial(i)

"""
fi = [1, 1]
def sp(n, m):
	s = 1
	d1 = 1
	d2 = 1
	#print(d1,d2,"!")
	for i in range(1, n+1):
		d1*=n-i+1
		d2*=m-i+1

		#print(i, d1,d2)
		d1%=MOD
		d2%=MOD
		s+= d1*d2 *(fi[i]%MOD)
		#print(d1*d2 *(fi[i]%MOD))
		s%= MOD

	return s



s = 1
for i in range(2, max(a,max(b,c))+1):
	s *=i
	s %= MOD
	fi.append(inv(s))


print((sp(a,b)*sp(a,c)*sp(b,c))%MOD)
#print(sp(1,2))
#print(sp(2,2))
#print()


# EoP (End of Problem details for node_28:cc_python_28)
# ######################################################################

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


# EoP (End of Problem details for node_29:cc_python_29)
# ######################################################################

# Query for: node_3:cc_python_3
# =========================
"""
Karen has just arrived at school, and she has a math test today!

<image>

The test is about basic addition and subtraction. Unfortunately, the teachers were too busy writing tasks for Codeforces rounds, and had no time to make an actual test. So, they just put one question in the test that is worth all the points.

There are n integers written on a row. Karen must alternately add and subtract each pair of adjacent integers, and write down the sums or differences on the next row. She must repeat this process on the values on the next row, and so on, until only one integer remains. The first operation should be addition.

Note that, if she ended the previous row by adding the integers, she should start the next row by subtracting, and vice versa.

The teachers will simply look at the last integer, and then if it is correct, Karen gets a perfect score, otherwise, she gets a zero for the test.

Karen has studied well for this test, but she is scared that she might make a mistake somewhere and it will cause her final answer to be wrong. If the process is followed, what number can she expect to be written on the last row?

Since this number can be quite large, output only the non-negative remainder after dividing it by 109 + 7.

Input

The first line of input contains a single integer n (1 ≤ n ≤ 200000), the number of numbers written on the first row.

The next line contains n integers. Specifically, the i-th one among these is ai (1 ≤ ai ≤ 109), the i-th number on the first row.

Output

Output a single integer on a line by itself, the number on the final row after performing the process above.

Since this number can be quite large, print only the non-negative remainder after dividing it by 109 + 7.

Examples

Input

5
3 6 9 12 15


Output

36


Input

4
3 7 5 2


Output

1000000006

Note

In the first test case, the numbers written on the first row are 3, 6, 9, 12 and 15.

Karen performs the operations as follows:

<image>

The non-negative remainder after dividing the final number by 109 + 7 is still 36, so this is the correct output.

In the second test case, the numbers written on the first row are 3, 7, 5 and 2.

Karen performs the operations as follows:

<image>

The non-negative remainder after dividing the final number by 109 + 7 is 109 + 6, so this is the correct output.
"""

# Original Problem: node_3:cc_python_3
# =========================
from sys import exit, stdin, stdout
n = int(stdin.readline())
a = [int(i) for i in stdin.readline().split()]
if n == 1:
    print(a[0])
    exit(0)
mod = 1000000007
f = [0] * (n + 1)
f[0] = 1
for i in range(1, n + 1):
    f[i] = (f[i-1] * i) % mod

def f_pow(a, k):
    if k == 0:
        return 1
    if k % 2 == 1:
        return f_pow(a, k - 1) * a % mod
    else:
        return f_pow(a * a % mod, k // 2) % mod

def c(n, k):
    d = f[k] * f[n - k] % mod
    return f[n] * f_pow(d, mod - 2) % mod
     
oper = 1
while not (oper and n % 2 == 0):
    for i in range(n - 1):
        a[i] = a[i] + oper * a[i + 1]
        oper *= -1
    n -= 1
oper *= 1 if (n//2 % 2) != 0 else -1

sm1 = 0
sm2 = 0
for i in range(n):
    if i % 2 == 0:
        sm1 = (sm1 + c(n // 2 - 1, i // 2) * a[i]) % mod
    else:
        sm2 = (sm2 + c(n // 2 - 1, i // 2) * a[i]) % mod
stdout.write(str((sm1 + oper * sm2) % mod))


# End of all problems.
