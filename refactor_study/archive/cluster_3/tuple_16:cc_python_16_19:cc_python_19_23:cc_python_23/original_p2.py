# Query for: node_19:cc_python_19
# =========================
"""
Parsa has a humongous tree on n vertices.

On each vertex v he has written two integers l_v and r_v.

To make Parsa's tree look even more majestic, Nima wants to assign a number a_v (l_v ≤ a_v ≤ r_v) to each vertex v such that the beauty of Parsa's tree is maximized.

Nima's sense of the beauty is rather bizarre. He defines the beauty of the tree as the sum of |a_u - a_v| over all edges (u, v) of the tree.

Since Parsa's tree is too large, Nima can't maximize its beauty on his own. Your task is to find the maximum possible beauty for Parsa's tree.

Input

The first line contains an integer t (1≤ t≤ 250) — the number of test cases. The description of the test cases follows.

The first line of each test case contains a single integer n (2≤ n≤ 10^5) — the number of vertices in Parsa's tree.

The i-th of the following n lines contains two integers l_i and r_i (1 ≤ l_i ≤ r_i ≤ 10^9).

Each of the next n-1 lines contains two integers u and v (1 ≤ u , v ≤ n, u≠ v) meaning that there is an edge between the vertices u and v in Parsa's tree.

It is guaranteed that the given graph is a tree.

It is guaranteed that the sum of n over all test cases doesn't exceed 2 ⋅ 10^5.

Output

For each test case print the maximum possible beauty for Parsa's tree.

Example

Input


3
2
1 6
3 8
1 2
3
1 3
4 6
7 9
1 2
2 3
6
3 14
12 20
12 19
2 12
10 17
3 17
3 2
6 5
1 5
2 6
4 6


Output


7
8
62

Note

The trees in the example:

<image>

In the first test case, one possible assignment is a = \{1, 8\} which results in |1 - 8| = 7.

In the second test case, one of the possible assignments is a = \{1, 5, 9\} which results in a beauty of |1 - 5| + |5 - 9| = 8
"""

# Original Problem: node_19:cc_python_19
# =========================
import sys
input = sys.stdin.buffer.readline

def main():
    t = int(input()); INF = float("inf")
    for _ in range(t):
        n = int(input())
        L = []; R = []
        for i in range(n):
            l,r = map(int,input().split())
            L.append(l); R.append(r)
        G = [[] for _ in range(n)]
        for i in range(n-1):
            a,b = map(int,input().split())
            a-=1;b-=1 #0-index
            G[a].append(b)
            G[b].append(a)

        root = 0
        #depth = [-1]*n
        #depth[0] = 0
        par = [-1]*n
        #depth_list = defaultdict(list)
        #depth_list[0].append(root)
        stack = []
        stack.append(~0)
        stack.append(0)
        dp = [[0, 0] for _ in range(n)]
        #cnt = 0
        while stack:
            #cnt += 1
            v = stack.pop()
            if v >= 0:
                for u in G[v]:
                    if u == par[v]: continue
                    par[u] = v
                    stack.append(~u)
                    stack.append(u)
            
            else:
                u = ~v #child
                v = par[u] #parent
                if v == -1: continue
                zero = max(dp[u][0] + abs(L[v] - L[u]), dp[u][1] + abs(L[v] - R[u]))
                one = max(dp[u][0] + abs(R[v] - L[u]), dp[u][1] + abs(R[v] - R[u]))
                dp[v][0] += zero
                dp[v][1] += one
        ans = max(dp[0])
        #print("CNT",cnt)
        #print(dp)
        print(ans)

if __name__ == "__main__":
    main()

