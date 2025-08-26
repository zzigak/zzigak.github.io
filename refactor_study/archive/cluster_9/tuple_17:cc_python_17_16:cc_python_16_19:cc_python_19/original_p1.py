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

