# This file contains original problem queries and their corresponding Python code.

# Query for: node_21:cc_python_21
# =========================
"""
"Eat a beaver, save a tree!" — That will be the motto of ecologists' urgent meeting in Beaverley Hills.

And the whole point is that the population of beavers on the Earth has reached incredible sizes! Each day their number increases in several times and they don't even realize how much their unhealthy obsession with trees harms the nature and the humankind. The amount of oxygen in the atmosphere has dropped to 17 per cent and, as the best minds of the world think, that is not the end.

In the middle of the 50-s of the previous century a group of soviet scientists succeed in foreseeing the situation with beavers and worked out a secret technology to clean territory. The technology bears a mysterious title "Beavermuncher-0xFF". Now the fate of the planet lies on the fragile shoulders of a small group of people who has dedicated their lives to science.

The prototype is ready, you now need to urgently carry out its experiments in practice.

You are given a tree, completely occupied by beavers. A tree is a connected undirected graph without cycles. The tree consists of n vertices, the i-th vertex contains ki beavers. 

"Beavermuncher-0xFF" works by the following principle: being at some vertex u, it can go to the vertex v, if they are connected by an edge, and eat exactly one beaver located at the vertex v. It is impossible to move to the vertex v if there are no beavers left in v. "Beavermuncher-0xFF" cannot just stand at some vertex and eat beavers in it. "Beavermuncher-0xFF" must move without stops.

Why does the "Beavermuncher-0xFF" works like this? Because the developers have not provided place for the battery in it and eating beavers is necessary for converting their mass into pure energy.

It is guaranteed that the beavers will be shocked by what is happening, which is why they will not be able to move from a vertex of the tree to another one. As for the "Beavermuncher-0xFF", it can move along each edge in both directions while conditions described above are fulfilled.

The root of the tree is located at the vertex s. This means that the "Beavermuncher-0xFF" begins its mission at the vertex s and it must return there at the end of experiment, because no one is going to take it down from a high place. 

Determine the maximum number of beavers "Beavermuncher-0xFF" can eat and return to the starting vertex.

Input

The first line contains integer n — the number of vertices in the tree (1 ≤ n ≤ 105). The second line contains n integers ki (1 ≤ ki ≤ 105) — amounts of beavers on corresponding vertices. Following n - 1 lines describe the tree. Each line contains two integers separated by space. These integers represent two vertices connected by an edge. Vertices are numbered from 1 to n. The last line contains integer s — the number of the starting vertex (1 ≤ s ≤ n).

Output

Print the maximum number of beavers munched by the "Beavermuncher-0xFF".

Please, do not use %lld specificator to write 64-bit integers in C++. It is preferred to use cout (also you may use %I64d).

Examples

Input

5
1 3 1 3 2
2 5
3 4
4 5
1 5
4


Output

6


Input

3
2 1 1
3 2
1 2
3


Output

2
"""

# Original Problem: node_21:cc_python_21
# =========================
import sys
from array import array  # noqa: F401


def input():
    return sys.stdin.buffer.readline().decode('utf-8')


n = int(input())
beaver = list(map(int, input().split()))
adj = [[] for _ in range(n)]
deg = [0] * n

for u, v in (map(int, input().split()) for _ in range(n - 1)):
    adj[u - 1].append(v - 1)
    adj[v - 1].append(u - 1)
    deg[u - 1] += 1
    deg[v - 1] += 1

start = int(input()) - 1
deg[start] += 1000000

if n == 1:
    print(0)
    exit()

dp = [0] * n
stack = [i for i in range(n) if i != start and deg[i] == 1]
while stack:
    v = stack.pop()
    deg[v] = 0
    child = []
    child_dp = []

    for dest in adj[v]:
        if deg[dest] == 0:
            child.append(dest)
            child_dp.append(dp[dest])

        else:
            deg[dest] -= 1
            if deg[dest] == 1:
                stack.append(dest)

    child_dp.sort(reverse=True)
    x = min(beaver[v] - 1, len(child))
    dp[v] = 1 + sum(child_dp[:x]) + x
    beaver[v] -= x + 1
    for c in child:
        x = min(beaver[v], beaver[c])
        beaver[v] -= x
        dp[v] += 2 * x


x = min(beaver[start], len(adj[start]))
child_dp = sorted((dp[v] for v in adj[start]), reverse=True)
ans = sum(child_dp[:x]) + x
beaver[start] -= x

for c in adj[start]:
    x = min(beaver[start], beaver[c])
    beaver[start] -= x
    ans += 2 * x

print(ans)


# EoP (End of Problem details for node_21:cc_python_21)
# ######################################################################

# Query for: node_6:cc_python_6
# =========================
"""
The Fair Nut is going to travel to the Tree Country, in which there are n cities. Most of the land of this country is covered by forest. Furthermore, the local road system forms a tree (connected graph without cycles). Nut wants to rent a car in the city u and go by a simple path to city v. He hasn't determined the path, so it's time to do it. Note that chosen path can consist of only one vertex.

A filling station is located in every city. Because of strange law, Nut can buy only w_i liters of gasoline in the i-th city. We can assume, that he has infinite money. Each road has a length, and as soon as Nut drives through this road, the amount of gasoline decreases by length. Of course, Nut can't choose a path, which consists of roads, where he runs out of gasoline. He can buy gasoline in every visited city, even in the first and the last.

He also wants to find the maximum amount of gasoline that he can have at the end of the path. Help him: count it.

Input

The first line contains a single integer n (1 ≤ n ≤ 3 ⋅ 10^5) — the number of cities.

The second line contains n integers w_1, w_2, …, w_n (0 ≤ w_{i} ≤ 10^9) — the maximum amounts of liters of gasoline that Nut can buy in cities.

Each of the next n - 1 lines describes road and contains three integers u, v, c (1 ≤ u, v ≤ n, 1 ≤ c ≤ 10^9, u ≠ v), where u and v — cities that are connected by this road and c — its length.

It is guaranteed that graph of road connectivity is a tree.

Output

Print one number — the maximum amount of gasoline that he can have at the end of the path.

Examples

Input

3
1 3 3
1 2 2
1 3 2


Output

3


Input

5
6 3 2 5 0
1 2 10
2 3 3
2 4 1
1 5 1


Output

7

Note

The optimal way in the first example is 2 → 1 → 3. 

<image>

The optimal way in the second example is 2 → 4. 

<image>
"""

# Original Problem: node_6:cc_python_6
# =========================
from sys import stdin
input=lambda : stdin.readline().strip()
from math import ceil,sqrt,factorial,gcd
from collections import deque
n=int(input())
l=list(map(int,input().split()))
visited=set()
graph={i:set() for i in range(1,n+1)}
d={}
papa=[0 for i in range(n+1)]
level=[[] for i in range(n+1)]
z=[[0] for i in range(n+1)]
for i in range(n-1):
	a,b,c=map(int,input().split())
	graph[a].add(b)
	graph[b].add(a)
	d[(a,b)]=c
stack=deque()
# print(graph)
for i in graph:
	if len(graph[i])==1:
		stack.append([i,0])
m=0
while stack:
	# print(stack)
	x,y=stack.popleft()
	if len(graph[x])>=1:
		for i in graph[x]:
			t=i
			break
		if (t,x) in d:
			q=d[(t,x)]
		else:
			q=d[(x,t)]
		z[t].append(y+l[x-1]-q)
		graph[t].remove(x)
		if len(graph[t])==1:
			stack.append([t,max(z[t])])
for i in range(1,n+1):
	z[i].sort()
	if len(z[i])>=3:
		m=max(m,l[i-1]+z[i][-2]+z[i][-1])
	m=max(m,z[i][-1]+l[i-1])
print(m)


# EoP (End of Problem details for node_6:cc_python_6)
# ######################################################################

# Query for: node_9:cc_python_9
# =========================
"""
Recently Bob invented a new game with a tree (we should remind you, that a tree is a connected graph without cycles): he deletes any (possibly, zero) amount of edges of the tree, and counts the product of sizes of the connected components left after the deletion. Your task is to find out the maximum number that Bob can get in his new game for a given tree.

Input

The first input line contains integer number n (1 ≤ n ≤ 700) — amount of vertices in the tree. The following n - 1 lines contain the description of the edges. Each line contains the pair of vertices' indexes, joined by an edge, ai, bi (1 ≤ ai, bi ≤ n). It's guaranteed that the graph described in the input is a tree.

Output

Output the only number — the maximum product of sizes of the connected components, that Bob can get after deleting some of the tree's edges.

Examples

Input

5
1 2
2 3
3 4
4 5


Output

6

Input

8
1 2
1 3
2 4
2 5
3 6
3 7
6 8


Output

18

Input

3
1 2
1 3


Output

3
"""

# Original Problem: node_9:cc_python_9
# =========================
from fractions import Fraction
n = int(input())

adj = [list() for x in  range(n)]
H = [0] * n
F = [0] * n
FoH = [list() for x in range(n)]
sz = 0
order = [0] * n
pi = [-1] * n

def dfs(u, p = -1):
  global pi, order, sz
  pi[u] = p
  for v in adj[u]:
    if v != p:
      dfs(v, u)
  order[sz] = u
  sz += 1


T1 = [0] * n
T2 = [0] * n
T3 = [0] * n

def solve(u, p = -1):
  global H, F, FoH
  F[u] = 1
  for v in adj[u]:
    if v != p:
      F[u] *= H[v]
      FoH[u].append(Fraction(F[v], H[v]))
  ans = F[u]
  FoH[u].sort()
  FoH[u].reverse()
  pd = 1
  s = 0
  for x in FoH[u]:
    pd *= x
    s += 1
    ans = max(ans, int(pd * F[u]) * (s+1))
  for v in adj[u]:
    if v != p:
      pd = 1
      s = 0
      for x in FoH[v]:
        pd *= x
        s += 1
        ans = max(ans, int(pd * F[u] * F[v]) // H[v] * (s+2))
  #print(u+1, ':', FoH[u], ans)
  H[u] = ans

for i in range(1, n):
  u, v = [int(x) for x in input().split()]
  u -= 1
  v -= 1
  adj[u].append(v)
  adj[v].append(u)

dfs(0)
for x in order:
  solve(x, pi[x])
print(H[0])


# End of all problems.
