from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    n = int(input())
    # store points with original indices
    pts = [(tuple(map(int, input().split())), i+1) for i in range(n)]
    # pick arbitrary point x
    x_pt, x_idx = pts.pop()
    # find closest neighbor y
    j = min(range(len(pts)), key=lambda i: norm_sq(sub(x_pt, pts[i][0])))
    y_pt, y_idx = pts.pop(j)
    # find closest non‐collinear point z
    z_idx = min(
        ((norm_sq(sub(x_pt, p)), idx) for p, idx in pts
         if not collinear(x_pt, y_pt, p)),
        key=lambda x: x[0]
    )[1]
    print(x_idx, y_idx, z_idx)

if __name__ == "__main__":
    main()