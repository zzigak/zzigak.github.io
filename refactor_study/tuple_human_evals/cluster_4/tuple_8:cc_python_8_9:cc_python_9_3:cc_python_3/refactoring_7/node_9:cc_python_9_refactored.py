from codebank import sub, dot

def main():
    import sys
    data = sys.stdin.read().split()
    it = iter(data)
    n = int(next(it))
    pts = [tuple(int(next(it)) for _ in range(5)) for _ in range(n)]
    # if more than 11 points, no good points
    if n > 11:
        print(0)
        return
    good = []
    for i, a in enumerate(pts):
        bad = False
        for j, b in enumerate(pts):
            if j == i: continue
            for k, c in enumerate(pts):
                if k <= j or k == i: continue
                # if angle at a is acute, dot>0
                if dot(sub(b, a), sub(c, a)) > 0:
                    bad = True
                    break
            if bad:
                break
        if not bad:
            good.append(i + 1)
    print(len(good))
    for idx in good:
        print(idx)

if __name__ == "__main__":
    main()