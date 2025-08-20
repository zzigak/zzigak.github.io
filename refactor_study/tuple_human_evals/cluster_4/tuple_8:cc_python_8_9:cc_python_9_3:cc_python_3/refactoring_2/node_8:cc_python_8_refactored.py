from codebank import *

def main():
    n = int(input())
    points = [tuple(map(int, input().split())) for _ in range(n)]
    x = points[-1]
    # pick y = closest to x among the first n-1 points
    j, y = min(enumerate(points[:-1]), key=lambda ij: dist_sq(x, ij[1]))
    # pick z = closest to x among those not collinear with x,y
    rest = [(i, p) for i, p in enumerate(points[:-1]) if i != j]
    k, z = min(
        (ip for ip in rest if not collinear(x, y, ip[1])),
        key=lambda ip: dist_sq(x, ip[1])
    )
    # output indices: x is n, y is j+1, z is k+1
    print(n, j+1, k+1)

if __name__ == "__main__":
    main()