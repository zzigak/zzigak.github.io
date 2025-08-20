from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    n = int(input())
    a = list(map(int, input().split()))
    arr = compress(a)
    bit0 = [0]*(n+1)
    bit1 = [0]*(n+1)
    ans = 0
    for cur in reversed(arr):
        ans += bit_query(bit1, cur-1)
        cnt = bit_query(bit0, cur-1)
        bit_update(bit0, n, cur, 1)
        bit_update(bit1, n, cur, cnt)
    print(ans)

if __name__ == "__main__":
    main()