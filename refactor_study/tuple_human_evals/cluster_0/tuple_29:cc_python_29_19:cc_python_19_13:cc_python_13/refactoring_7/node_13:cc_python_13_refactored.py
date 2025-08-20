from codebank import *

def main():
    n = read_int()
    if n % 2:
        print(-1)
        return
    adj = build_adj_list(n)
    parent, post_order = get_parent_and_postorder(adj)
    sz = [1] * n
    for v in post_order:
        if v != 0:
            sz[parent[v]] += sz[v]
    cnt = sum(1 for v in range(1, n) if sz[v] % 2 == 0)
    print(cnt)

if __name__ == "__main__":
    main()