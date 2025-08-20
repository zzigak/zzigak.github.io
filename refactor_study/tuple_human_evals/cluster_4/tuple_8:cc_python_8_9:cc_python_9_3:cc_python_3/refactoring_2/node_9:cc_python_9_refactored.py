from codebank import *

def main():
    n = int(input())
    B = [tuple(map(int, input().split())) for _ in range(n)]
    if n > 11:
        print(0)
        return
    goods = []
    for i, a in enumerate(B):
        good = True
        for b in range(n):
            for c in range(b+1, n):
                if b != i and c != i and dot(sub(B[b], a), sub(B[c], a)) > 0:
                    good = False
                    break
            if not good:
                break
        if good:
            goods.append(i+1)
    print(len(goods))
    for idx in goods:
        print(idx)

if __name__ == "__main__":
    main()