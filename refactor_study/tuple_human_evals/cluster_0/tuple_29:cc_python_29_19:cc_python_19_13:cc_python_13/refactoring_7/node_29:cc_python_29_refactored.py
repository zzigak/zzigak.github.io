from codebank import *

def main():
    n = read_int()
    colors = read_ints()
    adj = build_adj_list(n)
    total_red = colors.count(1)
    total_blue = colors.count(2)
    parent, post_order = get_parent_and_postorder(adj)
    count_red = [0] * n
    count_blue = [0] * n
    ans = 0
    for v in post_order:
        if colors[v] == 1:
            count_red[v] += 1
        elif colors[v] == 2:
            count_blue[v] += 1
        if v != 0:
            if (count_red[v] == total_red and count_blue[v] == 0) or \
               (count_blue[v] == total_blue and count_red[v] == 0):
                ans += 1
            p = parent[v]
            count_red[p] += count_red[v]
            count_blue[p] += count_blue[v]
    print(ans)

if __name__ == "__main__":
    main()