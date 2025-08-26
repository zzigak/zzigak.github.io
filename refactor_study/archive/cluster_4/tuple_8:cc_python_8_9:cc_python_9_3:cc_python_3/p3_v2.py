# ########## PROGRAM: node_9:cc_python_9 ##########

from codebank import sub_vec, dot

def main():
    import sys
    input = sys.stdin.readline
    n = int(input())
    pts = [list(map(int, input().split())) for _ in range(n)]
    # In 5D, there can be at most 2*d = 10 good points.
    if n > 11:
        print(0)
        return
    good = []
    for i, a in enumerate(pts):
        bad = False
        for j, b in enumerate(pts):
            if j == i: continue
            for k, c in enumerate(pts[j+1:], start=j+1):
                if k == i: continue
                # acute angle <=> dot((b-a),(c-a)) > 0
                if dot(sub_vec(b, a), sub_vec(c, a)) > 0:
                    bad = True
                    break
            if bad:
                break
        if not bad:
            good.append(i+1)
    print(len(good))
    print('\n'.join(map(str, good)))

if __name__ == "__main__":
    main()