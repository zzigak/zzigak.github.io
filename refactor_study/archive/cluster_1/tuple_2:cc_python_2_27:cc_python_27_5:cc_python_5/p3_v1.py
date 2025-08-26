# ########## PROGRAM: node_5:cc_python_5 ##########

from codebank import *

def main():
    t = int(input())
    for _ in range(t):
        a, b = map(int, input().split())
        if a == b:
            print(0)
            continue
        lo, hi = min(a, b), max(a, b)
        if hi % lo != 0:
            print(-1)
            continue
        ratio = hi // lo
        e = pow2_exp(ratio)
        if e is None:
            print(-1)
        else:
            print(count_shifts(e))

if __name__ == "__main__":
    main()