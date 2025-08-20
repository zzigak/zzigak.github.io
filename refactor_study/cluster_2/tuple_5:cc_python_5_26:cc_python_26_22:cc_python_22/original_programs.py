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
    ### ID 必要なとき
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
    
    ### 最 Edge が必要なとき （なー return させるj
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