from codebank import *

def main():
    n = int(input())
    A = [tuple(map(int, input().split())) for _ in range(n)]
    if n > 11:
        print(0)
        return
    good = []
    for i, a in enumerate(A):
        bad = False
        for j in range(n):
            if j == i: continue
            for k in range(j+1, n):
                if k == i: continue
                if dot(sub(A[j], a), sub(A[k], a)) > 0:
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