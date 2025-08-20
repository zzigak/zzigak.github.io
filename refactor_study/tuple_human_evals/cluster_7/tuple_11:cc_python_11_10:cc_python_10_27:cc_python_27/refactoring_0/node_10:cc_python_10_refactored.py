from codebank import *

def main():
    import sys
    data = sys.stdin.read().split()
    n = int(data[0])
    arr = list(map(int, data[1:1+n]))
    ans_inv = 0
    x = 0
    MAXB = 30
    # inv1 = inversions if xbit=0, inv0 = inversions if xbit=1
    for bit in range(MAXB, -1, -1):
        inv0, inv1 = compute_bit_inversions(arr, bit)
        # choose xbit = 0 if inv1 <= inv0, else xbit = 1
        if inv1 <= inv0:
            ans_inv += inv1
        else:
            ans_inv += inv0
            x |= 1 << bit
    print(ans_inv, x)

if __name__ == "__main__":
    main()