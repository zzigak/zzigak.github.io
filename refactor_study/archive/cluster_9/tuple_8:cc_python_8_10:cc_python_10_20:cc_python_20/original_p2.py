# Query for: node_20:cc_python_20
# =========================
"""
There are n cities and m roads in Berland. Each road connects a pair of cities. The roads in Berland are one-way.

What is the minimum number of new roads that need to be built to make all the cities reachable from the capital?

New roads will also be one-way.

Input

The first line of input consists of three integers n, m and s (1 ≤ n ≤ 5000, 0 ≤ m ≤ 5000, 1 ≤ s ≤ n) — the number of cities, the number of roads and the index of the capital. Cities are indexed from 1 to n.

The following m lines contain roads: road i is given as a pair of cities u_i, v_i (1 ≤ u_i, v_i ≤ n, u_i ≠ v_i). For each pair of cities (u, v), there can be at most one road from u to v. Roads in opposite directions between a pair of cities are allowed (i.e. from u to v and from v to u).

Output

Print one integer — the minimum number of extra roads needed to make all the cities reachable from city s. If all the cities are already reachable from s, print 0.

Examples

Input

9 9 1
1 2
1 3
2 3
1 5
5 6
6 1
1 8
9 8
7 1


Output

3


Input

5 4 5
1 2
2 3
3 4
4 1


Output

1

Note

The first example is illustrated by the following:

<image>

For example, you can add roads (6, 4), (7, 9), (1, 7) to make all the cities reachable from s = 1.

The second example is illustrated by the following:

<image>

In this example, you can add any one of the roads (5, 1), (5, 2), (5, 3), (5, 4) to make all the cities reachable from s = 5.
"""

# Original Problem: node_20:cc_python_20
# =========================
def main():
    import sys
    sys.setrecursionlimit(10**5)
    from collections import deque
    n, m, s = map(int, input().split())
    s -= 1
    graph = [[] for _ in range(n)]
    for _ in range(m):
        u, v = map(int, input().split())
        graph[u-1].append(v-1)

    seen = [False]*n
    li = deque()

    def visit(node):
        if not seen[node]:
            seen[node] = True
            for c_node in graph[node]:
                visit(c_node)
            li.appendleft(node)

    def visit2(node):
        if not seen[node]:
            seen[node] = True
            for c_node in graph[node]:
                visit2(c_node)

    for i in range(n):
        visit(i)
    seen = [False]*n
    cnt = 0
    visit2(s)
    for i in li:
        if seen[i]:
            continue
        visit2(i)
        cnt += 1
    print(cnt)

if __name__ == "__main__":
    try:
        main()
    except:
        print('error!')
        exit(0)

