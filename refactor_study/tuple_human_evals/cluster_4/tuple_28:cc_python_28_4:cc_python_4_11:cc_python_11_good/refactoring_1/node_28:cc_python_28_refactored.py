from codebank import *

def main():
    n = int(input())
    pts = [tuple(map(int, input().split())) for _ in range(n)]
    lines = defaultdict(set)
    for p, q in combinations(pts, 2):
        dx = q[0] - p[0]
        dy = q[1] - p[1]
        dxn, dyn = normalize_direction(dx, dy)
        # line normal = (-dyn, dxn), c = dyn*x - dxn*y
        c = dyn*p[0] - dxn*p[1]
        lines[(dxn, dyn)].add(c)
    total = sum(len(v) for v in lines.values())
    # total intersecting = total choose 2 minus sum over parallels
    result = total*(total-1)//2
    for v in lines.values():
        k = len(v)
        result -= k*(k-1)//2
    print(result)

if __name__ == "__main__":
    main()