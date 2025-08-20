from codebank import *

def compute_max_fuel(adj, w):
    n = len(adj)
    par, order = parorder(adj, 0)
    children = get_children(par)
    best_down = [0]*n
    ans = 0
    for u in reversed(order):
        bests = []
        for v in children[u]:
            # find cost
            for x, c in adj[u]:
                if x == v:
                    cost = c; break
            contrib = best_down[v] - cost
            if contrib > 0:
                bests.append(contrib)
        bests.sort(reverse=True)
        if bests:
            best_down[u] = w[u] + bests[0]
        else:
            best_down[u] = w[u]
        # combine two best
        tot = w[u] + (bests[0] if bests else 0) + (bests[1] if len(bests)>1 else 0)
        ans = max(ans, tot)
    return ans

def main():
    n = int(input())
    w = read_ints()
    adj = read_weighted_tree(n)
    print(compute_max_fuel(adj, w))

if __name__ == "__main__":
    main()