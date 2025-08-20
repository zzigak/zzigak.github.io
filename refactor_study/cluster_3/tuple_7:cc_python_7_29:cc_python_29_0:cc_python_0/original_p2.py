# Query for: node_29:cc_python_29
# =========================
"""
A tree is a graph with n vertices and exactly n - 1 edges; this graph should meet the following condition: there exists exactly one shortest (by number of edges) path between any pair of its vertices.

A subtree of a tree T is a tree with both vertices and edges as subsets of vertices and edges of T.

You're given a tree with n vertices. Consider its vertices numbered with integers from 1 to n. Additionally an integer is written on every vertex of this tree. Initially the integer written on the i-th vertex is equal to vi. In one move you can apply the following operation:

  1. Select the subtree of the given tree that includes the vertex with number 1. 
  2. Increase (or decrease) by one all the integers which are written on the vertices of that subtree. 



Calculate the minimum number of moves that is required to make all the integers written on the vertices of the given tree equal to zero.

Input

The first line of the input contains n (1 ≤ n ≤ 105). Each of the next n - 1 lines contains two integers ai and bi (1 ≤ ai, bi ≤ n; ai ≠ bi) indicating there's an edge between vertices ai and bi. It's guaranteed that the input graph is a tree. 

The last line of the input contains a list of n space-separated integers v1, v2, ..., vn (|vi| ≤ 109).

Output

Print the minimum number of operations needed to solve the task.

Please, do not write the %lld specifier to read or write 64-bit integers in С++. It is preferred to use the cin, cout streams or the %I64d specifier.

Examples

Input

3
1 2
1 3
1 -1 1


Output

3
"""

# Original Problem: node_29:cc_python_29
# =========================
import sys

def minp():
	return sys.stdin.readline().strip()

n = int(minp())
e = [0]
p = [None]*(n+1)
for i in range(n):
	e.append([])
for i in range(n-1):
	a, b = map(int,minp().split())
	e[a].append(b)
	e[b].append(a)
v = list(map(int,minp().split()))
plus = [0]*(n+1)
minus = [0]*(n+1)

was = [False]*(n+1)
was[1] = True
i = 0
j = 1
q = [0]*(n+100)
q[0] = 1
p[1] = 0
while i < j:
	x = q[i]
	i += 1
	for y in e[x]:
		if not was[y]:
			was[y] = True
			p[y] = x
			q[j] = y
			j += 1

i = j-1
while i >= 0:
	x = q[i]
	i -= 1
	s = minus[x] - plus[x]
	z = v[x-1] + s
	pp = p[x]
	#print(x, p[x], plus[x], minus[x], '-', s[x], v[x-1]+s[x], v[0]+s[1])
	#print(-(plus[x]-minus[x]),s[x])
	minus[pp] = max(minus[x],minus[pp])
	plus[pp] = max(plus[x],plus[pp])
	if z > 0:
		plus[pp] = max(plus[pp],plus[x]+z)
	elif z < 0:
		minus[pp] = max(minus[pp],minus[x]-z)
#print(v[0])
#print(plus[0], minus[0])
print(plus[0] + minus[0])

