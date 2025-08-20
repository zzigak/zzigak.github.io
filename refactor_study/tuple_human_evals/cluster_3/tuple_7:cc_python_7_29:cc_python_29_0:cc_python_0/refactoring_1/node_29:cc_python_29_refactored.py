from codebank import *
def main():
    n = int(input())
    tree = read_tree(n, offset=1)
    v = list(map(int, input().split()))
    par, order = parorder(tree, 1)
    children = get_children(par)
    pos = [0] * (n + 1); neg = [0] * (n + 1)
    for u in reversed(order):
        for w in children[u]:
            if pos[w] > pos[u]: pos[u] = pos[w]
            if neg[w] > neg[u]: neg[u] = neg[w]
        cur = v[u - 1] + pos[u] - neg[u]
        if cur > 0:
            neg[u] += cur
        else:
            pos[u] += -cur
    print(pos[1] + neg[1])
if __name__ == "__main__":
    main()