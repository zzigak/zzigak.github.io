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
