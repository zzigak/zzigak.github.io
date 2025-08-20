from codebank import process_bit

def main():
    import sys
    input = sys.stdin.readline
    n = int(input())
    arr = list(map(int, input().split()))
    xori = 0
    ans = 0
    for i in range(32):
        inv1, inv2, arr = process_bit(arr)
        if inv1 <= inv2:
            ans += inv1
        else:
            ans += inv2
            xori |= 1 << i
    print(ans, xori)

if __name__ == "__main__":
    main()