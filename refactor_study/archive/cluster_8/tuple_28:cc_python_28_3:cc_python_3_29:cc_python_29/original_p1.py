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

