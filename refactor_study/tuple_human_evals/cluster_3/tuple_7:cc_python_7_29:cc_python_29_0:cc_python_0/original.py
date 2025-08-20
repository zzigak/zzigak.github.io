# This file contains original problem queries and their corresponding Python code.

# Query for: node_0:cc_python_0
# =========================
"""
Igor is a post-graduate student of chemistry faculty in Berland State University (BerSU). He needs to conduct a complicated experiment to write his thesis, but laboratory of BerSU doesn't contain all the materials required for this experiment.

Fortunately, chemical laws allow material transformations (yes, chemistry in Berland differs from ours). But the rules of transformation are a bit strange.

Berland chemists are aware of n materials, numbered in the order they were discovered. Each material can be transformed into some other material (or vice versa). Formally, for each i (2 ≤ i ≤ n) there exist two numbers xi and ki that denote a possible transformation: ki kilograms of material xi can be transformed into 1 kilogram of material i, and 1 kilogram of material i can be transformed into 1 kilogram of material xi. Chemical processing equipment in BerSU allows only such transformation that the amount of resulting material is always an integer number of kilograms.

For each i (1 ≤ i ≤ n) Igor knows that the experiment requires ai kilograms of material i, and the laboratory contains bi kilograms of this material. Is it possible to conduct an experiment after transforming some materials (or none)?

Input

The first line contains one integer number n (1 ≤ n ≤ 105) — the number of materials discovered by Berland chemists.

The second line contains n integer numbers b1, b2... bn (1 ≤ bi ≤ 1012) — supplies of BerSU laboratory.

The third line contains n integer numbers a1, a2... an (1 ≤ ai ≤ 1012) — the amounts required for the experiment.

Then n - 1 lines follow. j-th of them contains two numbers xj + 1 and kj + 1 that denote transformation of (j + 1)-th material (1 ≤ xj + 1 ≤ j, 1 ≤ kj + 1 ≤ 109).

Output

Print YES if it is possible to conduct an experiment. Otherwise print NO.

Examples

Input

3
1 2 3
3 2 1
1 1
1 1


Output

YES


Input

3
3 2 1
1 2 3
1 1
1 2


Output

NO
"""

# Original Problem: node_0:cc_python_0
# =========================
import sys

# @profile
def main():
    f = sys.stdin
    # f = open('input.txt', 'r')
    # fo = open('log.txt', 'w')
    n = int(f.readline())
    # b = []
    # for i in range(n):
    #    b.append()
    b = list(map(int, f.readline().strip().split(' ')))
    a = list(map(int, f.readline().strip().split(' ')))
    # return
    b = [b[i] - a[i] for i in range(n)]
    c = [[0, 0]]
    for i in range(n - 1):
        line = f.readline().strip().split(' ')
        c.append([int(line[0]), int(line[1])])
    # print(c)
    for i in range(n - 1, 0, -1):
        # print(i)
        fa = c[i][0] - 1
        if b[i] >= 0:
            b[fa] += b[i]
        else:
            b[fa] += b[i] * c[i][1]
            if b[fa] < -1e17:
                print('NO')
                return 0
    # for x in b:
    #    fo.write(str(x) + '\n')
    if b[0] >= 0:
        print('YES')
    else:
        print('NO')

main()


# EoP (End of Problem details for node_0:cc_python_0)
# ######################################################################

# Query for: node_29:cc_python_29
# =========================
"""
A tree is a graph with n vertices and exactly n - 1 edges; this graph should meet the following condition: there exists exactly one shortest (by number of edges) path between any pair of its vertices.

A subtree of a tree T is a tree with both vertices and edges as subsets of vertices and edges of T.

You're given a tree with n vertices. Consider its vertices numbered with integers from 1 to n. Additionally an integer is written on every vertex of this tree. Initially the integer written on the i-th vertex is equal to vi. In one move you can apply the following operation:

  1. Select the subtree of the given tree that includes the vertex with number 1. 
  2. Increase (or decrease) by one all the integers which are written on the vertices of that subtree. 



Calculate the minimum number of moves that is required to make all the integers written on the vertices of the given tree equal to zero.

Input

The first line of the input contains n (1 ≤ n ≤ 105). Each of the next n - 1 lines contains two integers ai and bi (1 ≤ ai, bi ≤ n; ai ≠ bi) indicating there's an edge between vertices ai and bi. It's guaranteed that the input graph is a tree. 

The last line of the input contains a list of n space-separated integers v1, v2, ..., vn (|vi| ≤ 109).

Output

Print the minimum number of operations needed to solve the task.

Please, do not write the %lld specifier to read or write 64-bit integers in С++. It is preferred to use the cin, cout streams or the %I64d specifier.

Examples

Input

3
1 2
1 3
1 -1 1


Output

3
"""

# Original Problem: node_29:cc_python_29
# =========================
import sys

def minp():
	return sys.stdin.readline().strip()

n = int(minp())
e = [0]
p = [None]*(n+1)
for i in range(n):
	e.append([])
for i in range(n-1):
	a, b = map(int,minp().split())
	e[a].append(b)
	e[b].append(a)
v = list(map(int,minp().split()))
plus = [0]*(n+1)
minus = [0]*(n+1)

was = [False]*(n+1)
was[1] = True
i = 0
j = 1
q = [0]*(n+100)
q[0] = 1
p[1] = 0
while i < j:
	x = q[i]
	i += 1
	for y in e[x]:
		if not was[y]:
			was[y] = True
			p[y] = x
			q[j] = y
			j += 1

i = j-1
while i >= 0:
	x = q[i]
	i -= 1
	s = minus[x] - plus[x]
	z = v[x-1] + s
	pp = p[x]
	#print(x, p[x], plus[x], minus[x], '-', s[x], v[x-1]+s[x], v[0]+s[1])
	#print(-(plus[x]-minus[x]),s[x])
	minus[pp] = max(minus[x],minus[pp])
	plus[pp] = max(plus[x],plus[pp])
	if z > 0:
		plus[pp] = max(plus[pp],plus[x]+z)
	elif z < 0:
		minus[pp] = max(minus[pp],minus[x]-z)
#print(v[0])
#print(plus[0], minus[0])
print(plus[0] + minus[0])


# EoP (End of Problem details for node_29:cc_python_29)
# ######################################################################

# Query for: node_7:cc_python_7
# =========================
"""
You are given a tree consisting of n vertices. A tree is a connected undirected graph with n-1 edges. Each vertex v of this tree has a color assigned to it (a_v = 1 if the vertex v is white and 0 if the vertex v is black).

You have to solve the following problem for each vertex v: what is the maximum difference between the number of white and the number of black vertices you can obtain if you choose some subtree of the given tree that contains the vertex v? The subtree of the tree is the connected subgraph of the given tree. More formally, if you choose the subtree that contains cnt_w white vertices and cnt_b black vertices, you have to maximize cnt_w - cnt_b.

Input

The first line of the input contains one integer n (2 ≤ n ≤ 2 ⋅ 10^5) — the number of vertices in the tree.

The second line of the input contains n integers a_1, a_2, ..., a_n (0 ≤ a_i ≤ 1), where a_i is the color of the i-th vertex.

Each of the next n-1 lines describes an edge of the tree. Edge i is denoted by two integers u_i and v_i, the labels of vertices it connects (1 ≤ u_i, v_i ≤ n, u_i ≠ v_i).

It is guaranteed that the given edges form a tree.

Output

Print n integers res_1, res_2, ..., res_n, where res_i is the maximum possible difference between the number of white and black vertices in some subtree that contains the vertex i.

Examples

Input


9
0 1 1 1 0 0 0 0 1
1 2
1 3
3 4
3 5
2 6
4 7
6 8
5 9


Output


2 2 2 2 2 1 1 0 2 


Input


4
0 0 1 0
1 2
1 3
1 4


Output


0 -1 1 -1 

Note

The first example is shown below:

<image>

The black vertices have bold borders.

In the second example, the best subtree for vertices 2, 3 and 4 are vertices 2, 3 and 4 correspondingly. And the best subtree for the vertex 1 is the subtree consisting of vertices 1 and 3.
"""

# Original Problem: node_7:cc_python_7
# =========================
import os
import sys
from io import BytesIO, IOBase
from types import GeneratorType
from collections import defaultdict

BUFSIZE = 8192


class FastIO(IOBase):
    newlines = 0

    def __init__(self, file):
        self._fd = file.fileno()
        self.buffer = BytesIO()
        self.writable = "x" in file.mode or "r" not in file.mode
        self.write = self.buffer.write if self.writable else None

    def read(self):
        while True:
            b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
            if not b:
                break
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
        self.newlines = 0
        return self.buffer.read()

    def readline(self):
        while self.newlines == 0:
            b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
            self.newlines = b.count(b"\n") + (not b)
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
        self.newlines -= 1
        return self.buffer.readline()

    def flush(self):
        if self.writable:
            os.write(self._fd, self.buffer.getvalue())
            self.buffer.truncate(0), self.buffer.seek(0)


class IOWrapper(IOBase):
    def __init__(self, file):
        self.buffer = FastIO(file)
        self.flush = self.buffer.flush
        self.writable = self.buffer.writable
        self.write = lambda s: self.buffer.write(s.encode("ascii"))
        self.read = lambda: self.buffer.read().decode("ascii")
        self.readline = lambda: self.buffer.readline().decode("ascii")


sys.stdin, sys.stdout = IOWrapper(sys.stdin), IOWrapper(sys.stdout)
input = lambda: sys.stdin.readline().rstrip("\r\n")
sys.setrecursionlimit(2 * 10 ** 5)



ans=0

def bootstrap(f, stack=[]):
    def wrappedfunc(*args, **kwargs):
        if stack:
            return f(*args, **kwargs)
        else:
            to = f(*args, **kwargs)
            while True:
                if type(to) is GeneratorType:
                    stack.append(to)
                    to = next(to)
                else:
                    stack.pop()
                    if not stack:
                        break
                    to = stack[-1].send(to)
            return to

    return wrappedfunc


@bootstrap
def dfs(now, lay, fa):
    SUM[now] = 0
    NUM[now] = C[now]
    for to in A[now]:
        if to != fa:
            yield dfs(to, lay + 1, now)
            SUM[now] += SUM[to]
            SUM[now] += NUM[to]
            NUM[now] += NUM[to]
    yield


@bootstrap
def change(now, fa):
    global ans
    ans = max(ans, SUM[now])
    for to in A[now]:
        if to != fa:
            SUM[now] -= SUM[to]
            SUM[now] -= NUM[to]
            NUM[now] -= NUM[to]
            NUM[to] += NUM[now]
            SUM[to] += SUM[now]
            SUM[to] += NUM[now]

            yield change(to, now)

            SUM[to] -= SUM[now]
            SUM[to] -= NUM[now]
            NUM[to] -= NUM[now]
            NUM[now] += NUM[to]
            SUM[now] += SUM[to]
            SUM[now] += NUM[to]
    yield


n = int(input())
A = [[] for i in range(n + 1)]
C = [0] + (list(map(int, input().split())))
NUM = [0] * (n + 1)
SUM = [0] * (n + 1)
for i in range(n - 1):
    x, y = map(int, input().split())
    A[x].append(y)
    A[y].append(x)
dfs(1, 0, 0)
change(1, 0)
print(ans)
# print(NUM)
# print(SUM)


# End of all problems.
