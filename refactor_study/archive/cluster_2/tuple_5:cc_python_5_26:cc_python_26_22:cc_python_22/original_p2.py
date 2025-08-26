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

