# ########## PROGRAM: node_20:cc_python_20 ##########

from codebank import kosaraju_scc, dfs

def main():
    import sys
    input = sys.stdin.readline
    n, m, s = map(int, input().split())
    s -= 1
    graph = [[] for _ in range(n)]
    for _ in range(m):
        u, v = map(int, input().split())
        graph[u-1].append(v-1)
    comp_id, comp_cnt = kosaraju_scc(graph)
    comp_graph = [set() for _ in range(comp_cnt)]
    for u in range(n):
        cu = comp_id[u]
        for v in graph[u]:
            cv = comp_id[v]
            if cu != cv:
                comp_graph[cu].add(cv)
    reachable = [False] * comp_cnt
    dfs(comp_graph, comp_id[s], reachable)
    indegree = [0] * comp_cnt
    for u in range(comp_cnt):
        if reachable[u]:
            continue
        for v in comp_graph[u]:
            if not reachable[v]:
                indegree[v] += 1
    ans = sum(1 for u in range(comp_cnt) if not reachable[u] and indegree[u] == 0)
    print(ans)

if __name__ == "__main__":
    main()