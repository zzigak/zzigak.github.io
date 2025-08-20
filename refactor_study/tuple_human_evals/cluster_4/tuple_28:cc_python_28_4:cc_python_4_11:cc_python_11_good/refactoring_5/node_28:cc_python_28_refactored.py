from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    n = int(input())
    pts = [tuple(map(int, input().split())) for _ in range(n)]
    lines = {}
    for i in range(n):
        x1, y1 = pts[i]
        for j in range(i+1, n):
            x2, y2 = pts[j]
            dx, dy = x2 - x1, y2 - y1
            d = normalize_direction(dx, dy)
            a, b = d
            c = a*y1 - b*x1
            lines.setdefault(d, set()).add(c)
    total = sum(len(s) for s in lines.values())
    res = total*(total-1)//2
    for s in lines.values():
        k = len(s)
        res -= k*(k-1)//2
    print(res)

if __name__ == "__main__":
    main()