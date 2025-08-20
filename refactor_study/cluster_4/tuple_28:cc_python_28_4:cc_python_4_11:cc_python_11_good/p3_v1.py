# ########## PROGRAM: node_4:cc_python_4 ##########

from codebank import *
from itertools import combinations
from collections import defaultdict

def main():
    n = int(input())
    pts = [tuple(map(int, input().split())) for _ in range(n)]
    groups = defaultdict(set)
    for p, q in combinations(pts, 2):
        dir, c = compute_line_key(p, q)
        groups[dir].add(c)
    total = sum(len(v) for v in groups.values())
    res = 0
    for cnt in (len(v) for v in groups.values()):
        res += cnt * (total - cnt)
    print(res // 2)

if __name__ == "__main__":
    main()