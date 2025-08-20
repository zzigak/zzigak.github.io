from codebank import *

def main():
    import sys
    data = sys.stdin.read().split()
    it = iter(data)
    n = int(next(it))
    a = [int(next(it)) for _ in range(n)]
    arr, m = compress(a)
    bit1 = [0]*(m+1)
    bit2 = [0]*(m+1)
    ans = 0
    for cur in reversed(arr):
        c = bit_query(bit1, cur-1)
        bit_update(bit1, m, cur, 1)
        bit_update(bit2, m, cur, c)
        ans += bit_query(bit2, cur-1)
    print(ans)

if __name__ == "__main__":
    main()