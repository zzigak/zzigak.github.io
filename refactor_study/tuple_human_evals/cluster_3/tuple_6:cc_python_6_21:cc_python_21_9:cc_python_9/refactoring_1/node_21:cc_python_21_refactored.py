from codebank import *

def main():
    import sys
    n = int(sys.stdin.readline())
    beaver = list(map(int, sys.stdin.readline().split()))
    adj = [[] for _ in range(n)]
    deg = [0]*n
    for _ in range(n-1):
        u, v = read_ints()
        u -= 1; v -= 1
        adj[u].append(v); adj[v].append(u)
        deg[u] += 1; deg[v] += 1
    start = int(sys.stdin.readline())-1
    deg[start] += 10**9
    if n==1:
        print(0); return
    dp = [0]*n
    stack = deque(i for i in range(n) if i!=start and deg[i]==1)
    while stack:
        v = stack.popleft()
        deg[v] = 0
        child = []; child_dp = []
        for u in adj[v]:
            if deg[u]==0:
                child.append(u); child_dp.append(dp[u])
            else:
                deg[u] -= 1
                if deg[u]==1 and u!=start:
                    stack.append(u)
        child_dp.sort(reverse=True)
        x = min(beaver[v]-1, len(child))
        dp[v] = 1 + sum(child_dp[:x]) + x
        beaver[v] -= x+1
        for c in child:
            y = min(beaver[v], beaver[c])
            beaver[v] -= y
            dp[v] += 2*y
    x = min(beaver[start], len(adj[start]))
    child_dp = sorted((dp[v] for v in adj[start]), reverse=True)
    ans = sum(child_dp[:x]) + x
    beaver[start] -= x
    for c in adj[start]:
        y = min(beaver[start], beaver[c])
        beaver[start] -= y
        ans += 2*y
    print(ans)

if __name__ == "__main__":
    main()