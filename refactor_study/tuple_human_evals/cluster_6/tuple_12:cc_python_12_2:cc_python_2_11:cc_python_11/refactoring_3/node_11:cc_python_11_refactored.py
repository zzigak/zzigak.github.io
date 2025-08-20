from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    k, n, m = map(int, input().split())
    a = list(map(int, input().split()))
    l = [[[] for _ in range(3)] for _ in range(k)]
    for idx in range(1, n+1):
        t, i, b = map(int, input().split())
        l[i-1][t-1].append((b, idx))
    for i in range(k):
        for j in range(3):
            l[i][j].sort(reverse=True)
    ops = []
    for i in range(k):
        adds = l[i][1][:]
        if l[i][0] and l[i][0][0][0] > a[i]:
            adds.append((l[i][0][0][0] - a[i], l[i][0][0][1]))
            adds.sort(reverse=True)
        s = a[i]
        for add, idx in adds:
            ops.append(((s+add)/s, idx))
            s += add
        for mul, idx in l[i][2]:
            ops.append((mul, idx))
    top_ops = get_top_n(ops, m, key=lambda x: x[0])
    st = {idx for _, idx in top_ops}
    res = []
    for i in range(k):
        for j in range(3):
            for _, idx in l[i][j]:
                if idx in st:
                    res.append(idx)
    print(len(res))
    if res:
        print(*res)

if __name__ == "__main__":
    main()