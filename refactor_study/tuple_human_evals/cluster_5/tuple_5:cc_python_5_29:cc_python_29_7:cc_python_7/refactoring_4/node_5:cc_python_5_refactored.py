from codebank import *
import sys

def main():
    input = sys.stdin.readline
    n = int(input().strip())
    a = read_ints()
    a_comp, m = compress(a)
    bit = [0]*(m+1)
    f = [0]*n
    for i, v in enumerate(a_comp):
        le = bit_query(bit, v)
        f[i] = i - le
        bit_update(bit, m, v, 1)
    bit = [0]*(m+1)
    ans = 0
    for i in range(n-1, -1, -1):
        v = a_comp[i]
        g = bit_query(bit, v-1)
        ans += f[i] * g
        bit_update(bit, m, v, 1)
    print(ans)

if __name__ == "__main__":
    main()