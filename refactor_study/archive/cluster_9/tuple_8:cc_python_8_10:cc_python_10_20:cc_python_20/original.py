# This file contains original problem queries and their corresponding Python code.

# Query for: node_10:cc_python_10
# =========================
"""
Little town Nsk consists of n junctions connected by m bidirectional roads. Each road connects two distinct junctions and no two roads connect the same pair of junctions. It is possible to get from any junction to any other junction by these roads. The distance between two junctions is equal to the minimum possible number of roads on a path between them.

In order to improve the transportation system, the city council asks mayor to build one new road. The problem is that the mayor has just bought a wonderful new car and he really enjoys a ride from his home, located near junction s to work located near junction t. Thus, he wants to build a new road in such a way that the distance between these two junctions won't decrease. 

You are assigned a task to compute the number of pairs of junctions that are not connected by the road, such that if the new road between these two junctions is built the distance between s and t won't decrease.

Input

The firt line of the input contains integers n, m, s and t (2 ≤ n ≤ 1000, 1 ≤ m ≤ 1000, 1 ≤ s, t ≤ n, s ≠ t) — the number of junctions and the number of roads in Nsk, as well as the indices of junctions where mayors home and work are located respectively. The i-th of the following m lines contains two integers ui and vi (1 ≤ ui, vi ≤ n, ui ≠ vi), meaning that this road connects junctions ui and vi directly. It is guaranteed that there is a path between any two junctions and no two roads connect the same pair of junctions.

Output

Print one integer — the number of pairs of junctions not connected by a direct road, such that building a road between these two junctions won't decrease the distance between junctions s and t.

Examples

Input

5 4 1 5
1 2
2 3
3 4
4 5


Output

0


Input

5 4 3 5
1 2
2 3
3 4
4 5


Output

5


Input

5 6 1 5
1 2
1 3
1 4
4 5
3 5
2 5


Output

3
"""

# Original Problem: node_10:cc_python_10
# =========================
from collections import deque
def bfs(s, graph):
    q = deque()
    d = [0] * len(graph)
    used = [False] * len(graph)
    used[s] = True
    q.append(s)
    while len(q):
        cur = q[0]
        q.popleft()
        for to in graph[cur]:
            if not used[to]:
                used[to] = True
                d[to] = d[cur] + 1
                q.append(to)
    return d
n, m, s, t = map(int, input().split())
graph = [set() for _ in range(n + 1)]
for i in range(m):
    u, v = map(int, input().split())
    graph[u].add(v)
    graph[v].add(u)
ds = bfs(s, graph)
dt = bfs(t, graph)
ans = 0
for u in range(1, n + 1):
    for v in range(u + 1, n + 1):
        if v not in graph[u] and min(ds[u] + dt[v], dt[u] + ds[v]) + 1 >= ds[t]:
            ans += 1
print(ans)


# EoP (End of Problem details for node_10:cc_python_10)
# ######################################################################

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


# EoP (End of Problem details for node_20:cc_python_20)
# ######################################################################

# Query for: node_8:cc_python_8
# =========================
"""
Logical quantifiers are very useful tools for expressing claims about a set. For this problem, let's focus on the set of real numbers specifically. The set of real numbers includes zero and negatives. There are two kinds of quantifiers: universal (∀) and existential (∃). You can read more about them here.

The universal quantifier is used to make a claim that a statement holds for all real numbers. For example:

  * ∀ x,x<100 is read as: for all real numbers x, x is less than 100. This statement is false. 
  * ∀ x,x>x-1 is read as: for all real numbers x, x is greater than x-1. This statement is true. 



The existential quantifier is used to make a claim that there exists some real number for which the statement holds. For example:

  * ∃ x,x<100 is read as: there exists a real number x such that x is less than 100. This statement is true. 
  * ∃ x,x>x-1 is read as: there exists a real number x such that x is greater than x-1. This statement is true. 



Moreover, these quantifiers can be nested. For example:

  * ∀ x,∃ y,x<y is read as: for all real numbers x, there exists a real number y such that x is less than y. This statement is true since for every x, there exists y=x+1. 
  * ∃ y,∀ x,x<y is read as: there exists a real number y such that for all real numbers x, x is less than y. This statement is false because it claims that there is a maximum real number: a number y larger than every x. 



Note that the order of variables and quantifiers is important for the meaning and veracity of a statement.

There are n variables x_1,x_2,…,x_n, and you are given some formula of the form $$$ f(x_1,...,x_n):=(x_{j_1}<x_{k_1})∧ (x_{j_2}<x_{k_2})∧ ⋅⋅⋅∧ (x_{j_m}<x_{k_m}), $$$

where ∧ denotes logical AND. That is, f(x_1,…, x_n) is true if every inequality x_{j_i}<x_{k_i} holds. Otherwise, if at least one inequality does not hold, then f(x_1,…,x_n) is false.

Your task is to assign quantifiers Q_1,…,Q_n to either universal (∀) or existential (∃) so that the statement $$$ Q_1 x_1, Q_2 x_2, …, Q_n x_n, f(x_1,…, x_n) $$$

is true, and the number of universal quantifiers is maximized, or determine that the statement is false for every possible assignment of quantifiers.

Note that the order the variables appear in the statement is fixed. For example, if f(x_1,x_2):=(x_1<x_2) then you are not allowed to make x_2 appear first and use the statement ∀ x_2,∃ x_1, x_1<x_2. If you assign Q_1=∃ and Q_2=∀, it will only be interpreted as ∃ x_1,∀ x_2,x_1<x_2.

Input

The first line contains two integers n and m (2≤ n≤ 2⋅ 10^5; 1≤ m≤ 2⋅ 10^5) — the number of variables and the number of inequalities in the formula, respectively.

The next m lines describe the formula. The i-th of these lines contains two integers j_i,k_i (1≤ j_i,k_i≤ n, j_i≠ k_i).

Output

If there is no assignment of quantifiers for which the statement is true, output a single integer -1.

Otherwise, on the first line output an integer, the maximum possible number of universal quantifiers.

On the next line, output a string of length n, where the i-th character is "A" if Q_i should be a universal quantifier (∀), or "E" if Q_i should be an existential quantifier (∃). All letters should be upper-case. If there are multiple solutions where the number of universal quantifiers is maximum, print any.

Examples

Input


2 1
1 2


Output


1
AE


Input


4 3
1 2
2 3
3 1


Output


-1


Input


3 2
1 3
2 3


Output


2
AAE

Note

For the first test, the statement ∀ x_1, ∃ x_2, x_1<x_2 is true. Answers of "EA" and "AA" give false statements. The answer "EE" gives a true statement, but the number of universal quantifiers in this string is less than in our answer.

For the second test, we can show that no assignment of quantifiers, for which the statement is true exists.

For the third test, the statement ∀ x_1, ∀ x_2, ∃ x_3, (x_1<x_3)∧ (x_2<x_3) is true: We can set x_3=max\\{x_1,x_2\}+1.
"""

# Original Problem: node_8:cc_python_8
# =========================
import sys
input = sys.stdin.readline

############ ---- Input Functions ---- ############
def inp():
    return(int(input()))
def inlt():
    return(list(map(int,input().split())))
def insr():
    s = input().strip()
    return(list(s[:len(s)]))
def invr():
    return(map(int,input().split()))



def from_file(f):
    return f.readline


def build_graph(n, A, reversed=False):
    edges = [[] for _ in range(n)]
    for i, j in A:
        i -= 1
        j -= 1
        if reversed:
            j, i = i, j
        edges[i].append(j)
    return edges


def fill_min(s, edges, visited_dfs, visited, container):
    visited[s] = True
    visited_dfs.add(s)

    for c in edges[s]:
        if c in visited_dfs:
            # cycle
            return -1
        if not visited[c]:
            res = fill_min(c, edges, visited_dfs, visited, container)
            if res == -1:
                return -1
        container[s] = min(container[s], container[c])
    visited_dfs.remove(s)
    return 0


def dfs(s, edges,  visited, container):

    stack = [s]

    colors = {s: 0}

    while stack:
        v = stack.pop()
        if colors[v] == 0:
            colors[v] = 1
            stack.append(v)
        else:
            # all children are visited
            tmp = [container[c] for c in edges[v]]
            if tmp:
                container[v] = min(min(tmp), container[v])
            colors[v] = 2 # finished
            visited[v] = True

        for c in edges[v]:
            if visited[c]:
                continue
            if c not in colors:
                colors[c] = 0 # white
                stack.append(c)
            elif colors[c] == 1:
                # grey
                return -1
    return 0





def iterate_topologically(n, edges, container):
    visited = [False] * n

    for s in range(n):
        if not visited[s]:
            # visited_dfs = set()
            # res = fill_min(s, edges, visited_dfs, visited, container)
            res = dfs(s, edges, visited, container)
            if res == -1:
                return -1
    return 0


def solve(n, A):
    edges = build_graph(n, A, False)
    container_forward = list(range(n))
    container_backward = list(range(n))

    res = iterate_topologically(n, edges, container_forward)
    if res == -1:
        return None

    edges = build_graph(n, A, True)

    iterate_topologically(n, edges, container_backward)
    container = [min(i,j) for i,j in zip(container_forward, container_backward)]

    res = sum((1 if container[i] == i else 0 for i in range(n)))

    s = "".join(["A" if container[i] == i else "E" for i in range(n)])

    return res, s



# with open('5.txt') as f:
#     input = from_file(f)
n, m = invr()
A = []
for _ in range(m):
    i, j = invr()
    A.append((i, j))

result = solve(n, A)
if not result:
    print (-1)
else:
    print(f"{result[0]}")
    print(f"{result[1]}")


# End of all problems.
