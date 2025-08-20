from codebank import *

def main():
    n = int(input())
    beaver = read_ints()
    adj = read_tree(n)
    start = int(input().split()[-1]) - 1  # fix reading start
    # compute degrees
    deg = [len(adj[i]) for i in range(n)]
    deg[start] += 10**6
    if n == 1:
        print(0); return
    dp = [0]*n
    stack = [i for i in range(n) if i != start and deg[i] == 1]
    while stack:
        v = stack.pop()
        deg[v] = 0
        childs = []
        child_dp = []
        for u in adj[v]:
            if deg[u] == 0:
                childs.append(u)
                child_dp.append(dp[u])
            else:
                deg[u] -= 1
                if deg[u] == 1 and u != start:
                    stack.append(u)
        child_dp.sort(reverse=True)
        x = min(beaver[v] - 1, len(child_dp))
        dp[v] = 1 + sum(child_dp[:x]) + x
        beaver[v] -= x + 1
        for u in childs:
            y = min(beaver[v], beaver[u])
            beaver[v] -= y
            dp[v] += 2*y
    # now at start
    cdp = sorted((dp[v] for v in adj[start]), reverse=True)
    x = min(beaver[start], len(adj[start]))
    ans = sum(cdp[:x]) + x
    beaver[start] -= x
    for v in adj[start]:
        y = min(beaver[start], beaver[v])
        beaver[start] -= y
        ans += 2*y
    print(ans)

if __name__ == "__main__":
    main()