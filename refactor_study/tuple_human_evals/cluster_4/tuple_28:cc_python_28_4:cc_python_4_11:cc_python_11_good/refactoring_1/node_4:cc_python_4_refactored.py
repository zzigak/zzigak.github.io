from codebank import *

def main():
    n = int(input())
    pts = [tuple(map(int, input().split())) for _ in range(n)]
    lines = defaultdict(set)
    for i in range(n):
        for j in range(i+1, n):
            p, q = pts[i], pts[j]
            dx = q[0] - p[0]
            dy = q[1] - p[1]
            dxn, dyn = normalize_direction(dx, dy)
            c = dyn*p[0] - dxn*p[1]
            lines[(dxn, dyn)].add(c)
    total = sum(len(v) for v in lines.values())
    result = total*(total-1)//2
    for v in lines.values():
        k = len(v)
        result -= k*(k-1)//2
    print(result)

if __name__ == "__main__":
    main()