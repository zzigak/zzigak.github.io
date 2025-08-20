from codebank import *

def main():
    k, n, m = map(int, input().split())
    a = list(map(int, input().split()))
    groups = [[[], [], []] for _ in range(k)]
    for idx in range(1, n + 1):
        t, i, b = map(int, input().split())
        groups[i - 1][t - 1].append((b, idx))
    ops = []
    for ai, grp in zip(a, groups):
        assigns, adds, muls = grp
        ops.extend(get_skill_ops(ai, assigns, adds, muls))
    # sort by ratio descending (stable for ties)
    ops.sort(key=lambda x: x[0], reverse=True)
    selected = ops[:m]
    # output in order: all adds/assigns then mults, preserving selected order
    add_idxs = [idx for _, idx, flag, _ in selected if flag == 2]
    mul_idxs = [idx for _, idx, flag, _ in selected if flag == 3]
    res = add_idxs + mul_idxs
    print(len(res))
    if res:
        print(" ".join(map(str, res)))

if __name__ == "__main__":
    main()