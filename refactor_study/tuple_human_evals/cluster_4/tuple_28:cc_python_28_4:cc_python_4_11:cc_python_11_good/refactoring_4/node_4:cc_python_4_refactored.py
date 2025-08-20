from codebank import *
from itertools import combinations
from collections import defaultdict

def main():
    n = int(input())
    points = [tuple(map(int, input().split())) for _ in range(n)]
    lines = defaultdict(set)
    for p, q in combinations(points, 2):
        dir, c = line_key(p, q)
        lines[dir].add(c)
    total = sum(len(s) for s in lines.values())
    result = sum(cnt * (total - cnt) for cnt in (len(s) for s in lines.values())) // 2
    print(result)

if __name__ == "__main__":
    main()