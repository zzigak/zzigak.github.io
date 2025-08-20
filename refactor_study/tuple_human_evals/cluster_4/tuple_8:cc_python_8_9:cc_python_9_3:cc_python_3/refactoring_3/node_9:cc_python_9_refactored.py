from codebank import *

def main():
    n = int(input())
    pts = [tuple(map(int, input().split())) for _ in range(n)]
    good = []
    if n <= 11:
        for i, a in enumerate(pts):
            bad = False
            for b in pts:
                if b is a: continue
                v1 = sub(b, a)
                for c in pts:
                    if c is a or c is b: continue
                    v2 = sub(c, a)
                    if dot(v1, v2) > 0:
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