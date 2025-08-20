from codebank import *

def main():
    n = int(input())
    w = list(map(int, input().split()))
    adj = read_weighted_tree(n)
    par, order = parorder(adj, 0)
    children = get_children(par)
    best_down = [0]*n
    max_path = 0
    for u in reversed(order):
        vals = []
        for v, c in adj[u]:
            if par[v] == u:
                d = best_down[v] - c
                if d > 0:
                    vals.append(d)
        if vals:
            vals.sort(reverse=True)
            best1 = vals[0]
        else:
            best1 = 0
        best_down[u] = w[u] + best1
        max_path = max(max_path, best_down[u])
        if len(vals) > 1:
            max_path = max(max_path, w[u] + vals[0] + vals[1])
    print(max_path)

if __name__ == "__main__":
    main()