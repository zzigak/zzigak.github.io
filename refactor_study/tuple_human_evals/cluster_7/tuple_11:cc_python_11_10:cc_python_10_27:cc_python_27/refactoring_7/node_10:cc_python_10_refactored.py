from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    n = int(input())
    arr = list(map(int, input().split()))
    MAXB = 30
    x = 0
    total_inv = 0
    groups = [arr]
    for bit in range(MAXB, -1, -1):
        inv10 = 0
        inv01 = 0
        # count inversions for this bit across all groups
        for group in groups:
            cnt0 = 0
            cnt1 = 0
            for v in group:
                if (v >> bit) & 1:
                    inv01 += cnt0
                    cnt1 += 1
                else:
                    inv10 += cnt1
                    cnt0 += 1
        # decide flip or not
        if inv10 <= inv01:
            total_inv += inv10
            # no flip: zeros first, then ones
            new_groups = []
            for group in groups:
                zero = []
                one = []
                for v in group:
                    if (v >> bit) & 1:
                        one.append(v)
                    else:
                        zero.append(v)
                if zero: new_groups.append(zero)
                if one: new_groups.append(one)
            groups = new_groups
        else:
            total_inv += inv01
            x |= (1 << bit)
            # flip: ones first, then zeros
            new_groups = []
            for group in groups:
                zero = []
                one = []
                for v in group:
                    if (v >> bit) & 1:
                        one.append(v)
                    else:
                        zero.append(v)
                if one: new_groups.append(one)
                if zero: new_groups.append(zero)
            groups = new_groups
    print(total_inv, x)

if __name__ == "__main__":
    main()