from codebank import *

def main():
    k, n, m = read_ints()
    a = read_ints()
    l = [[[], [], []] for _ in range(k)]
    for j in range(1, n+1):
        t, i, bval = read_ints()
        l[i-1][t-1].append((bval, j))
    ops = []
    for idx in range(k):
        adds = sorted(l[idx][1], reverse=True)
        if l[idx][0]:
            bv, bi = max(l[idx][0])
            if bv > a[idx]:
                adds = sorted(adds + [(bv - a[idx], bi)], reverse=True)
        s = a[idx]
        for addv, addi in adds:
            ops.append(((s + addv) / s, addi))
            s += addv
        for mulv, muli in l[idx][2]:
            ops.append((mulv, muli))
    selected = select_top_ops_indices(ops, m)
    print(len(selected))
    for idx in range(k):
        for t in range(3):
            for val, op_idx in l[idx][t]:
                if op_idx in selected:
                    print(op_idx, end=" ")
    if selected:
        print()

if __name__ == "__main__":
    main()