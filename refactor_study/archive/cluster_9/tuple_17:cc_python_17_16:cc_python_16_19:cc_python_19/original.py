# This file contains original problem queries and their corresponding Python code.

# Query for: node_16:cc_python_16
# =========================
"""
There are n cities and m bidirectional roads in the country. The roads in the country form an undirected weighted graph. The graph is not guaranteed to be connected. Each road has it's own parameter w. You can travel through the roads, but the government made a new law: you can only go through two roads at a time (go from city a to city b and then from city b to city c) and you will have to pay (w_{ab} + w_{bc})^2 money to go through those roads. Find out whether it is possible to travel from city 1 to every other city t and what's the minimum amount of money you need to get from 1 to t.

Input

First line contains two integers n, m (2 ≤ n ≤ 10^5, 1 ≤ m ≤ min((n ⋅ (n - 1))/(2), 2 ⋅ 10^5)).

Next m lines each contain three integers v_i, u_i, w_i (1 ≤ v_i, u_i ≤ n, 1 ≤ w_i ≤ 50, u_i ≠ v_i). It's guaranteed that there are no multiple edges, i.e. for any edge (u_i, v_i) there are no other edges (u_i, v_i) or (v_i, u_i).

Output

For every city t print one integer. If there is no correct path between 1 and t output -1. Otherwise print out the minimum amount of money needed to travel from 1 to t.

Examples

Input


5 6
1 2 3
2 3 4
3 4 5
4 5 6
1 5 1
2 4 2


Output


0 98 49 25 114 

Input


3 2
1 2 1
2 3 2


Output


0 -1 9 

Note

The graph in the first example looks like this.

<image>

In the second example the path from 1 to 3 goes through 2, so the resulting payment is (1 + 2)^2 = 9.

<image>
"""

# Original Problem: node_16:cc_python_16
# =========================
import sys, io, os
input = io.BytesIO(os.read(0, os.fstat(0).st_size)).readline
read = lambda: map(int, input().split())
from heapq import heappush, heappop

inf = 1e10
n, m = read()
e = {}
for _ in range(m):
    v, u, w = read()
    v -= 1
    u -= 1
    if v not in e:
        e[v] = []
    if u not in e:
        e[u] = []
    e[v].append((u, w))
    e[u].append((v, w))
d = [inf] * n
d[0] = 0
q = []
td = [0] * n
heappush(q, (0, 0))
while q:
    vd, v = heappop(q)
    l = []
    for u, w in e[v]:
        td[u] = w
        l.append(u)
    for u in l:
        tdu = td[u]
        for x, w in e[u]:
            cv = vd + (tdu + w) ** 2
            if cv < d[x]:
                d[x] = cv
                heappush(q, (cv, x))
for i in range(n):
    if d[i] == inf:
        d[i] = -1
print(' '.join(map(str, d)))


# EoP (End of Problem details for node_16:cc_python_16)
# ######################################################################

# Query for: node_17:cc_python_17
# =========================
"""
You are given a weighted undirected graph. The vertices are enumerated from 1 to n. Your task is to find the shortest path between the vertex 1 and the vertex n.

Input

The first line contains two integers n and m (2 ≤ n ≤ 105, 0 ≤ m ≤ 105), where n is the number of vertices and m is the number of edges. Following m lines contain one edge each in form ai, bi and wi (1 ≤ ai, bi ≤ n, 1 ≤ wi ≤ 106), where ai, bi are edge endpoints and wi is the length of the edge.

It is possible that the graph has loops and multiple edges between pair of vertices.

Output

Write the only integer -1 in case of no path. Write the shortest path in opposite case. If there are many solutions, print any of them.

Examples

Input

5 6
1 2 2
2 5 5
2 3 4
1 4 1
4 3 3
3 5 1


Output

1 4 3 5 

Input

5 6
1 2 2
2 5 5
2 3 4
1 4 1
4 3 3
3 5 1


Output

1 4 3 5
"""

# Original Problem: node_17:cc_python_17
# =========================
from collections import defaultdict
from heapq import heappush, heapify, heappop

INF = 10 ** 18
class Graph:
	def __init__(self):
		self.adj_list = defaultdict(list)

	def add_edge(self, src, dest, cost):
		self.adj_list[src].append((dest, cost))
		self.adj_list[dest].append((src, cost))


def dijkstra(graph, src, dest, n):
	dist = [INF] * n
	vis = [False] * n
	dist[src] = 0
	min_queue = [(0, src)]
	heapify(min_queue)
	parent = [-1] * n

	while min_queue:
		d, u = heappop(min_queue)
		if vis[u]:
			continue
		vis[u] = True
		for v, d2 in graph.adj_list[u]:
			if d2 + d < dist[v]:
				dist[v] = d2 + d
				heappush(min_queue, (dist[v], v))
				parent[v] = u

	if dist[dest] == INF:
		return "-1"
	path = []
	curr = dest
	while curr != -1:
		path.append(curr + 1)
		curr = parent[curr]
	path.reverse()
	return " ".join(str(i) for i in path)


def main():
    graph = Graph()
    
    n, m = [int(i) for i in input().split()]
    for i in range(m):
        u, v, w = [int(j) for j in input().split()]
        u -= 1
        v -= 1
        graph.add_edge(u, v, w)

    print(dijkstra(graph, 0, n - 1, n))

if __name__ == '__main__':
    main()


# EoP (End of Problem details for node_17:cc_python_17)
# ######################################################################

# Query for: node_19:cc_python_19
# =========================
"""
You are given an array a consisting of n integers. In one move, you can jump from the position i to the position i - a_i (if 1 ≤ i - a_i) or to the position i + a_i (if i + a_i ≤ n).

For each position i from 1 to n you want to know the minimum the number of moves required to reach any position j such that a_j has the opposite parity from a_i (i.e. if a_i is odd then a_j has to be even and vice versa).

Input

The first line of the input contains one integer n (1 ≤ n ≤ 2 ⋅ 10^5) — the number of elements in a.

The second line of the input contains n integers a_1, a_2, ..., a_n (1 ≤ a_i ≤ n), where a_i is the i-th element of a.

Output

Print n integers d_1, d_2, ..., d_n, where d_i is the minimum the number of moves required to reach any position j such that a_j has the opposite parity from a_i (i.e. if a_i is odd then a_j has to be even and vice versa) or -1 if it is impossible to reach such a position.

Example

Input


10
4 5 7 6 7 5 4 4 6 4


Output


1 1 1 2 -1 1 1 3 1 1
"""

# Original Problem: node_19:cc_python_19
# =========================
input()
n=map(int,input().split())
n=list(n)
ans=len(n)*[-1]
a=[]
go=[[] for _ in range(len(n))]
for i,x in enumerate(n):
    for y in (x,-x):
        y+=i
        if y>=0 and y<len(n):
            if x%2!=n[y]%2:
                ans[i]=1
                a.append(i)
            else:
                go[y].append(i)

while len(a)!=0:
    b=[]
    for x in a:
        for y in go[x]:
            if ans[y]==-1:
                ans[y]=ans[x]+1
                b.append(y)
    a=b
for i,x in enumerate(ans):
    ans[i]=str(x)
print(' '.join(ans))


# End of all problems.
