from codebank import *

def main():
    n = int(input())
    pts = [tuple(map(int, input().split())) for _ in range(n)]
    dirs = defaultdict(set)
    for (x1,y1),(x2,y2) in combinations(pts, 2):
        dx, dy = x2-x1, y2-y1
        d = normalize_direction(dx, dy)
        c = d[0]*y1 - d[1]*x1
        dirs[d].add(c)
    total = sum(len(v) for v in dirs.values())
    res = sum(k*(total-k) for k in (len(v) for v in dirs.values())) // 2
    print(res)

if __name__ == "__main__":
    main()