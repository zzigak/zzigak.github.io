from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    n = int(input())
    a = list(map(int, input().split()))
    comp = compress(a)
    bit = [0]*(n+1)
    left_greater = [0]*n
    for j in range(n):
        lg = j - bit_query(bit, comp[j])
        left_greater[j] = lg
        bit_update(bit, comp[j], 1)
    bit = [0]*(n+1)
    ans = 0
    for j in range(n-1, -1, -1):
        small = bit_query(bit, comp[j]-1)
        ans += left_greater[j] * small
        bit_update(bit, comp[j], 1)
    print(ans)

if __name__ == "__main__":
    main()