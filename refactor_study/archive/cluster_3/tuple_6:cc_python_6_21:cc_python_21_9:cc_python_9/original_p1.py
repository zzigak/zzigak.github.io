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

