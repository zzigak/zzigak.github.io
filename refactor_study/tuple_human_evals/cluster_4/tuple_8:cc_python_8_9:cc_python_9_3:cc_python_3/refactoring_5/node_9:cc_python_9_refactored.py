from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    n = int(input())
    pts = [tuple(map(int, input().split())) for _ in range(n)]
    # by pigeonhole, if n>11 every point is bad
    if n > 11:
        print(0)
        return
    good = []
    for i, a in enumerate(pts):
        bad = False
        # look for any acute angle at a
        for j, b in enumerate(pts):
            if j == i: continue
            for k, c in enumerate(pts):
                if k <= j or k == i: continue
                if dot_nd(sub_nd(b, a), sub_nd(c, a)) > 0:
                    bad = True
                    break
            if bad:
                break
        if not bad:
            good.append(i+1)
    print(len(good))
    for idx in good:
        print(idx)

if __name__ == "__main__":
    main()