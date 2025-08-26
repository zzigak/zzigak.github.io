# ########## PROGRAM: node_9:cc_python_9 ##########

from codebank import sub_general, dot_general

def main():
    n = int(input())
    pts = [list(map(int, input().split())) for _ in range(n)]
    good = []
    if n <= 11:
        for i, a in enumerate(pts):
            ok = True
            for j in range(n):
                if not ok:
                    break
                for k in range(j+1, n):
                    if j == i or k == i:
                        continue
                    v1 = sub_general(pts[j], a)
                    v2 = sub_general(pts[k], a)
                    if dot_general(v1, v2) > 0:
                        ok = False
                        break
            if ok:
                good.append(i+1)
    print(len(good))
    for idx in good:
        print(idx)

if __name__ == "__main__":
    main()