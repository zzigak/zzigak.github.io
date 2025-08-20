from codebank import *

def main():
    k, n, m = read_ints()
    a = read_ints()
    l = [[[], [], []] for _ in range(k)]
    for idx in range(1, n + 1):
        t, i, b = read_ints()
        l[i - 1][t - 1].append((b, idx))
    ops = build_operations(a, l)
    ops.sort(key=lambda x: x[0], reverse=True)
    chosen = set(idx for _, idx in ops[:m])
    print(len(chosen))
    for i in range(k):
        for j in range(3):
            for _, idx in l[i][j]:
                if idx in chosen:
                    print(idx, end=" ")
    print()

if __name__ == "__main__":
    main()