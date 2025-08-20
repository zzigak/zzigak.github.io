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