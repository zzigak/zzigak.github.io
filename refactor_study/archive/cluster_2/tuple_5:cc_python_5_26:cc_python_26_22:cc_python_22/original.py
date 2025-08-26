# This file contains original problem queries and their corresponding Python code.

# Query for: node_22:cc_python_22
# =========================
"""
This is the easy version of the problem. The difference between the versions is the constraints on a_i. You can make hacks only if all versions of the problem are solved.

Little Dormi has recently received a puzzle from his friend and needs your help to solve it. 

The puzzle consists of an upright board with n rows and m columns of cells, some empty and some filled with blocks of sand, and m non-negative integers a_1,a_2,…,a_m (0 ≤ a_i ≤ n). In this version of the problem, a_i will be equal to the number of blocks of sand in column i.

When a cell filled with a block of sand is disturbed, the block of sand will fall from its cell to the sand counter at the bottom of the column (each column has a sand counter). While a block of sand is falling, other blocks of sand that are adjacent at any point to the falling block of sand will also be disturbed and start to fall. Specifically, a block of sand disturbed at a cell (i,j) will pass through all cells below and including the cell (i,j) within the column, disturbing all adjacent cells along the way. Here, the cells adjacent to a cell (i,j) are defined as (i-1,j), (i,j-1), (i+1,j), and (i,j+1) (if they are within the grid). Note that the newly falling blocks can disturb other blocks.

In one operation you are able to disturb any piece of sand. The puzzle is solved when there are at least a_i blocks of sand counted in the i-th sand counter for each column from 1 to m.

You are now tasked with finding the minimum amount of operations in order to solve the puzzle. Note that Little Dormi will never give you a puzzle that is impossible to solve.

Input

The first line consists of two space-separated positive integers n and m (1 ≤ n ⋅ m ≤ 400 000).

Each of the next n lines contains m characters, describing each row of the board. If a character on a line is '.', the corresponding cell is empty. If it is '#', the cell contains a block of sand.

The final line contains m non-negative integers a_1,a_2,…,a_m (0 ≤ a_i ≤ n) — the minimum amount of blocks of sand that needs to fall below the board in each column. In this version of the problem, a_i will be equal to the number of blocks of sand in column i.

Output

Print one non-negative integer, the minimum amount of operations needed to solve the puzzle.

Examples

Input


5 7
#....#.
.#.#...
#....#.
#....##
#.#....
4 1 1 1 0 3 1


Output


3


Input


3 3
#.#
#..
##.
3 1 1


Output


1

Note

For example 1, by disturbing both blocks of sand on the first row from the top at the first and sixth columns from the left, and the block of sand on the second row from the top and the fourth column from the left, it is possible to have all the required amounts of sand fall in each column. It can be proved that this is not possible with fewer than 3 operations, and as such the answer is 3. Here is the puzzle from the first example.

<image>

For example 2, by disturbing the cell on the top row and rightmost column, one can cause all of the blocks of sand in the board to fall into the counters at the bottom. Thus, the answer is 1. Here is the puzzle from the second example.

<image>
"""

# Original Problem: node_22:cc_python_22
# =========================
import sys
input = lambda: sys.stdin.readline().rstrip()

def scc(E):
    n = len(E)
    iE = [[] for _ in range(n)]
    for i, e in enumerate(E):
        for v in e:
            iE[v].append(i)
    T = []
    done = [0] * n # 0 -> 1 -> 2
    ct = 0
    for i0 in range(n):
        if done[i0]: continue
        Q = [~i0, i0]
        while Q:
            i = Q.pop()
            if i < 0:
                if done[~i] == 2: continue
                done[~i] = 2
                T.append(~i)
                ct += 1
                continue
            if i >= 0:
                if done[i]: continue
                done[i] = 1
            for j in E[i]:
                if done[j]: continue
                Q.append(~j)
                Q.append(j)
    
    done = [0] * n
    SCC = []
    ### ID ���K�v�ȂƂ�
    I = [0] * n
    ###
    for i0 in T[::-1]:
        if done[i0]: continue
        L = []
        Q = [~i0, i0]
        while Q:
            i = Q.pop()
            if i < 0:
                if done[~i] == 2: continue
                done[~i] = 2
                L.append(~i)
                ###
                I[~i] = len(SCC)
                ###
                continue
            if i >= 0:
                if done[i]: continue
                done[i] = 1
            for j in iE[i]:
                if done[j]: continue
                Q.append(~j)
                Q.append(j)
        SCC.append(L)
    # return SCC, I
    
    ### �� Edge ���K�v�ȂƂ� �i��� return �������j
    # nE = [set() for _ in range(len(SCC))]
    # iE = [set() for _ in range(len(SCC))]
    ciE = [1] * len(SCC)
    for i, e in enumerate(E):
        for j in e:
            if I[i] == I[j]: continue
            # print("i, j, I[i], I[j] =", i, j, I[i], I[j])
            # nE[I[i]].add(I[j])
            # iE[I[j]].add(I[i])
            ciE[I[j]] = 0
    # nE = [list(e) for e in nE]
    # iE = [list(e) for e in iE]
    return ciE
    # return SCC, I, nE, iE, ciE

N, M = map(int, input().split())
Z = [[1 if a == "#" else 0 for a in input()] for _ in range(N)]

su = sum([int(a) for a in input().split()])

I = []
ZZ = [[-1] * M for _ in range(N)]
for j in range(M):
    for i in range(N)[::-1]:
        if Z[i][j]:
            ZZ[i][j] = len(I)
            I.append((i << 20) ^ j)
        elif i < N - 1:
            ZZ[i][j] = ZZ[i+1][j]

mmm = (1 << 20) - 1
E = [[] for _ in range(su)]
for k in range(su):
    ij = I[k]
    i = ij >> 20
    j = ij & mmm
    if i < N - 1 and ZZ[i+1][j] >= 0:
        E[k].append(ZZ[i+1][j])
    if i and Z[i-1][j]:
        E[k].append(ZZ[i-1][j])
    if j and ZZ[i][j-1] >= 0:
        E[k].append(ZZ[i][j-1])
    if j < M - 1 and ZZ[i][j+1] >= 0:
        E[k].append(ZZ[i][j+1])

ciE = scc(E)

print(sum(ciE))


# EoP (End of Problem details for node_22:cc_python_22)
# ######################################################################

# Query for: node_26:cc_python_26
# =========================
"""
Nastia has an unweighted tree with n vertices and wants to play with it!

The girl will perform the following operation with her tree, as long as she needs:

  1. Remove any existing edge. 
  2. Add an edge between any pair of vertices. 



What is the minimum number of operations Nastia needs to get a bamboo from a tree? A bamboo is a tree in which no node has a degree greater than 2.

Input

The first line contains a single integer t (1 ≤ t ≤ 10 000) — the number of test cases.

The first line of each test case contains a single integer n (2 ≤ n ≤ 10^5) — the number of vertices in the tree.

Next n - 1 lines of each test cases describe the edges of the tree in form a_i, b_i (1 ≤ a_i, b_i ≤ n, a_i ≠ b_i).

It's guaranteed the given graph is a tree and the sum of n in one test doesn't exceed 2 ⋅ 10^5.

Output

For each test case in the first line print a single integer k — the minimum number of operations required to obtain a bamboo from the initial tree.

In the next k lines print 4 integers x_1, y_1, x_2, y_2 (1 ≤ x_1, y_1, x_2, y_{2} ≤ n, x_1 ≠ y_1, x_2 ≠ y_2) — this way you remove the edge (x_1, y_1) and add an undirected edge (x_2, y_2).

Note that the edge (x_1, y_1) must be present in the graph at the moment of removing.

Example

Input


2
7
1 2
1 3
2 4
2 5
3 6
3 7
4
1 2
1 3
3 4


Output


2
2 5 6 7
3 6 4 5
0

Note

Note the graph can be unconnected after a certain operation.

Consider the first test case of the example: 

<image> The red edges are removed, and the green ones are added.
"""

# Original Problem: node_26:cc_python_26
# =========================
def dfs(x, e, v, g):
  v[x] = True
  c = 0
  for y in e[x]:
    if not y in v:
      if dfs(y, e, v, g):
        c += 1
        if c > 2:
          g.append((x, y))
      else:
        g.append((x, y))

  if c < 2:
    return True

  if x != 1:
    return False

def leaf(x, e):
  p = 0
  while True:
    u = 0
    for y in e[x]:
      if y != p:
        u = y
        break
    if u == 0: break
    p = x
    x = u
  return x

def solve(n, e):
  g = []
  dfs(1, e, {}, g)

  for x, y in g:
    e[x].remove(y)
    e[y].remove(x)

  z = []
  l = leaf(1, e)
  for p, y, in g:
    r = leaf(y, e)
    z.append((p, y, l, r))
    l = leaf(r, e)

  print(len(z))
  if len(z) > 0:
    print('\n'.join(map(lambda x: ' '.join(map(str, x)), z)))


def main():
  t = int(input())
  for i in range(t):
    n = int(input())
    e = {}
    for i in range(n - 1):
      a, b = map(int, input().split())
      if not a in e: e[a] = []
      if not b in e: e[b] = []
      e[a].append(b)
      e[b].append(a)
    solve(n, e)


import threading
import sys

sys.setrecursionlimit(10 ** 5 + 1)
threading.stack_size(262000)
main = threading.Thread(target=main)
main.start()
main.join()


# EoP (End of Problem details for node_26:cc_python_26)
# ######################################################################

# Query for: node_5:cc_python_5
# =========================
"""
Mr. Kitayuta has just bought an undirected graph consisting of n vertices and m edges. The vertices of the graph are numbered from 1 to n. Each edge, namely edge i, has a color ci, connecting vertex ai and bi.

Mr. Kitayuta wants you to process the following q queries.

In the i-th query, he gives you two integers — ui and vi.

Find the number of the colors that satisfy the following condition: the edges of that color connect vertex ui and vertex vi directly or indirectly.

Input

The first line of the input contains space-separated two integers — n and m (2 ≤ n ≤ 100, 1 ≤ m ≤ 100), denoting the number of the vertices and the number of the edges, respectively.

The next m lines contain space-separated three integers — ai, bi (1 ≤ ai < bi ≤ n) and ci (1 ≤ ci ≤ m). Note that there can be multiple edges between two vertices. However, there are no multiple edges of the same color between two vertices, that is, if i ≠ j, (ai, bi, ci) ≠ (aj, bj, cj).

The next line contains a integer — q (1 ≤ q ≤ 100), denoting the number of the queries.

Then follows q lines, containing space-separated two integers — ui and vi (1 ≤ ui, vi ≤ n). It is guaranteed that ui ≠ vi.

Output

For each query, print the answer in a separate line.

Examples

Input

4 5
1 2 1
1 2 2
2 3 1
2 3 3
2 4 3
3
1 2
3 4
1 4


Output

2
1
0


Input

5 7
1 5 1
2 5 1
3 5 1
4 5 1
1 2 2
2 3 2
3 4 2
5
1 5
5 1
2 5
1 5
1 4


Output

1
1
1
1
2

Note

Let's consider the first sample. 

<image> The figure above shows the first sample. 

  * Vertex 1 and vertex 2 are connected by color 1 and 2. 
  * Vertex 3 and vertex 4 are connected by color 3. 
  * Vertex 1 and vertex 4 are not connected by any single color.
"""

# Original Problem: node_5:cc_python_5
# =========================
def build_graph():
    line1 = input().strip().split()
    n = int(line1[0])
    m = int(line1[1])
    graph = {}
    for _ in range(m):
        line = input().strip().split()
        u = int(line[0])
        v = int(line[1])
        c = int(line[2])
        if c not in graph:
            graph[c] = {j: [] for j in range(1, n+1)}
        graph[c][u].append(v)
        graph[c][v].append(u)
    return graph

def no_of_paths(u, v, graph):
    x = 0
    for c in graph:
        parent = {}
        parent = dfs_visit(v, graph[c], parent)
        if u in parent:
            x += 1
    return x

def dfs_visit(i, adj_list, parent):
    for j in adj_list[i]:
        if j not in parent:
            parent[j] = i
            dfs_visit(j, adj_list, parent)
    return parent


if __name__ == "__main__":
    graph = build_graph()
    for _ in range(int(input())):
        line = input().strip().split()
        print(no_of_paths(int(line[0]), int(line[1]), graph))


# End of all problems.
