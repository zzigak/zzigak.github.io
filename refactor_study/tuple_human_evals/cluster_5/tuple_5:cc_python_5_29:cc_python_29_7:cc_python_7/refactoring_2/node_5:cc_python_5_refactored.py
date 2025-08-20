from codebank import *

def main():
    import sys
    data = sys.stdin.read().split()
    n = int(data[0])
    a = list(map(int, data[1:1+n]))
    ranks, m = compress_coords(a)
    bit = [0]*(m+1)
    prefix_greater = [0]*n
    for i in range(n):
        r = ranks[i]
        prefix_greater[i] = i - bit_query(bit, r)
        bit_update(bit, m, r, 1)
    bit = [0]*(m+1)
    suffix_smaller = [0]*n
    for i in range(n-1, -1, -1):
        r = ranks[i]
        suffix_smaller[i] = bit_query(bit, r-1)
        bit_update(bit, m, r, 1)
    ans = 0
    for j in range(n):
        ans += prefix_greater[j] * suffix_smaller[j]
    print(ans)

if __name__ == "__main__":
    main()