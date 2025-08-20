# ########## PROGRAM: node_8:cc_python_8 ##########

from codebank import sub_vec, dist_sq, collinear

def main():
    import sys
    input = sys.stdin.readline
    n = int(input())
    # pts: list of (coords, original_index)
    pts = [(list(map(int, input().split())), i+1) for i in range(n)]
    p0, idx0 = pts[0]
    # find nearest neighbor to p0
    j = min(range(1, n), key=lambda i: dist_sq(pts[i][0], p0))
    p1, idx1 = pts[j]
    # find next point that is not collinear with p0,p1 and is closest to p0
    k = min(
        (i for i in range(1, n) if i != j and not collinear(p0, p1, pts[i][0])),
        key=lambda i: dist_sq(pts[i][0], p0)
    )
    p2, idx2 = pts[k]
    print(idx0, idx1, idx2)

if __name__ == "__main__":
    main()