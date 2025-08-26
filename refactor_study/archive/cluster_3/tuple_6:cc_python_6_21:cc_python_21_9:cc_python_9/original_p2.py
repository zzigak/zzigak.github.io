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

