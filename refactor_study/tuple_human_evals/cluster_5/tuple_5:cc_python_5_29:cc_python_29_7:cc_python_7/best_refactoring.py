# ########## LIBRARY HELPERS ##########

# ==== RETRIEVED HELPER FUNCTIONS ====

# Selected Helper Functions

def bit_update(bit, n, idx, val):
    """
    Update Fenwick tree `bit` of size `n` by adding `val` at position `idx`.
    Selected because: the solution plan uses point updates on two BITs.
    """
    while idx <= n:
        bit[idx] += val
        idx += idx & -idx

def bit_query(bit, idx):
    """
    Query Fenwick tree `bit` for the prefix sum up to `idx`.
    Selected because: the solution plan uses prefix-sum queries on two BITs.
    """
    s = 0
    while idx > 0:
        s += bit[idx]
        idx -= idx & -idx
    return s

def read_ints():
    """
    Read a line of space-separated integers.
    Selected because: convenient input parsing for the array of powers.
    """
    return list(map(int, input().split()))


# Selected Helper Functions

# None of the provided helper functions support:
# - computing the Z-function in linear time,
# - scanning the Z-array for prefix-suffix borders,
# - checking for middle occurrences,
# nor are they for reading a string input.
# Therefore, no existing helper functions are directly applicable.


# Selected Helper Functions

# None of the provided helpers directly support the tight-window DP
# or Z-function computations needed for this solution, so no helpers are selected.


# ==== NEW HELPER FUNCTIONS ====

def zfunction(s):
    n = len(s)
    Z = [0]*n
    l = r = 0
    for i in range(1, n):
        if i <= r:
            Z[i] = min(r - i + 1, Z[i - l])
        while i + Z[i] < n and s[Z[i]] == s[i + Z[i]]:
            Z[i] += 1
        if i + Z[i] - 1 > r:
            l, r = i, i + Z[i] - 1
    return Z


# ########################################
#
#  PROGRAM REFACTORINGS
#
# ########################################

# ########## PROGRAM: node_29:cc_python_29 ##########

from codebank import *

def main():
    s = input().strip()
    n = len(s)
    Z = zfunction(s)
    borders = [Z[i] for i in range(1, n) if i + Z[i] == n]
    if not borders:
        print("Just a legend")
        return
    prefix_max = [0]*n
    for i in range(1, n):
        prefix_max[i] = max(prefix_max[i-1], Z[i])
    for L in sorted(borders, reverse=True):
        if prefix_max[n - L - 1] >= L:
            print(s[:L])
            return
    print("Just a legend")

if __name__ == "__main__":
    main()

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

# ########## PROGRAM: node_7:cc_python_7 ##########

from codebank import *
import sys

MOD = 10**9 + 7
BAD = {(0,0,1,1),(0,1,0,1),(1,1,1,0),(1,1,1,1)}

def compute_dp(seq):
    n = len(seq)
    f = [0]*(n+1)
    f[n] = 1
    for j in range(n-1, -1, -1):
        tot = 0
        for k in range(j, min(j+4, n)):
            if tuple(seq[j:k+1]) not in BAD:
                tot = (tot + f[k+1]) % MOD
        f[j] = tot
    return f

def main():
    data = sys.stdin.read().split()
    m = int(data[0])
    bits = list(map(int, data[1:]))
    S = []
    sm = 0
    for b in bits:
        S.append(b)
        f = compute_dp(S)
        new = len(S) - max(zfunction(S[::-1]))
        sm = (sm + sum(f[:new])) % MOD
        print(sm)

if __name__ == "__main__":
    main()
