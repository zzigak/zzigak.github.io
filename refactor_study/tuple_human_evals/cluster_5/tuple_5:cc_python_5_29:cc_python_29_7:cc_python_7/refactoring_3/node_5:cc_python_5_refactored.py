from codebank import *

def main():
    import sys
    data = sys.stdin.read().split()
    n = int(data[0])
    a = list(map(int, data[1:]))
    # coordinate compression
    sorted_a = sorted(a)
    rank = {v: i for i, v in enumerate(sorted_a)}
    # Fenwick trees for counts and pair-counts
    bit0 = [0] * (n + 1)
    bit1 = [0] * (n + 1)
    ans = 0
    for x in reversed(a):
        i = rank[x] + 1
        # add number of decreasing pairs starting at this element
        ans += bit_query(bit1, i - 1)
        # update count of elements to the right
        bit_update(bit0, n, i, 1)
        # dp2 = number of elements smaller to the right
        dp2 = bit_query(bit0, i - 1)
        # update number of pairs for future queries
        bit_update(bit1, n, i, dp2)
    print(ans)

if __name__ == "__main__":
    main()