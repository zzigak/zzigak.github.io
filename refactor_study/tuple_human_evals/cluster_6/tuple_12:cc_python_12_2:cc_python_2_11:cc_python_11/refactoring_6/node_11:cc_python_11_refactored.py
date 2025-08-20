from codebank import *

def main():
    k, n, m = read_ints()
    a = list(read_ints())
    l = group_improvements(n, k)
    for i in range(k):
        for j in range(3):
            l[i][j].sort(reverse=True)
    ops = []
    for i in range(k):
        ops += collect_operations(a[i], *l[i])
    selected = top_m_by(ops, m)
    print(len(selected))
    print_selected_indices(l, selected)
    print()

if __name__ == "__main__":
    main()