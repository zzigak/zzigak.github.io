from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    n, m, s = map(int, input().split())
    s -= 1
    edges = [tuple(map(int, input().split())) for _ in range(m)]
    adj = build_directed_graph(n, edges)
    # compute SCCs
    comp, compN = strongly_connected_components(adj)
    # build component graph
    cadj = [[] for _ in range(compN)]
    for u in range(n):
        cu = comp[u]
        for v in adj[u]:
            cv = comp[v]
            if cu != cv:
                cadj[cu].append(cv)
    # remove duplicate edges
    for u in range(compN):
        cadj[u] = list(set(cadj[u]))
    # mark reachable components from s
    scomp = comp[s]
    reachable = [False]*compN
    stack = [scomp]
    reachable[scomp] = True
    while stack:
        u = stack.pop()
        for v in cadj[u]:
            if not reachable[v]:
                reachable[v] = True
                stack.append(v)
    # compute indegree among unreachable components
    indeg = [0]*compN
    for u in range(compN):
        if not reachable[u]:
            for v in cadj[u]:
                if not reachable[v]:
                    indeg[v] += 1
    # count components with zero indegree among unreachable
    ans = sum(1 for u in range(compN) if not reachable[u] and indeg[u] == 0)
    print(ans)

if __name__ == "__main__":
    main()