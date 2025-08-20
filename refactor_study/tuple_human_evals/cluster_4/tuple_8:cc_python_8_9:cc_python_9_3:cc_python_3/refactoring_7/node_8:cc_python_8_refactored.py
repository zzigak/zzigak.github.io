from codebank import sub, norm_sq, collinear

def main():
    import sys
    data = sys.stdin.read().split()
    it = iter(data)
    n = int(next(it))
    pts = []
    for idx in range(1, n+1):
        x = int(next(it)); y = int(next(it))
        pts.append((x, y, idx))
    # choose reference point x
    x = pts.pop()
    # find nearest neighbor to x
    j_idx, _ = min(enumerate(pts), key=lambda iv: norm_sq(sub(x, iv[1])))
    y = pts.pop(j_idx)
    # find nearest to x that isn't collinear with x,y
    best = None
    k_pt = None
    for p in pts:
        if collinear(x, y, p):
            continue
        d = norm_sq(sub(x, p))
        if best is None or d < best:
            best = d
            k_pt = p
    # output the three indices
    print(x[2], y[2], k_pt[2])

if __name__ == "__main__":
    main()