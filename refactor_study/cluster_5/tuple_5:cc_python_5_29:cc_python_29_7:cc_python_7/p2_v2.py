# ########## PROGRAM: node_5:cc_python_5 ##########

from codebank import *

def main():
    n = int(input())
    a = read_ints()
    ranks = {v: i+1 for i, v in enumerate(sorted(a))}
    bit0 = [0]*(n+1)
    bit1 = [0]*(n+1)
    ans = 0
    for v in reversed(a):
        r = ranks[v]
        ans += bit_query(bit1, r-1)
        cnt = bit_query(bit0, r-1)
        bit_update(bit0, n, r, 1)
        bit_update(bit1, n, r, cnt)
    print(ans)

if __name__ == "__main__":
    main()