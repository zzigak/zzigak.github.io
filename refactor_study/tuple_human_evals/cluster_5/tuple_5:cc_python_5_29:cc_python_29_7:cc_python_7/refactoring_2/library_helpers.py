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
def read_ints():
    return list(map(int, input().split()))

def bit_update(bit, n, idx, val):
    while idx <= n:
        bit[idx] += val
        idx += idx & -idx

def bit_query(bit, idx):
    s = 0
    while idx > 0:
        s += bit[idx]
        idx -= idx & -idx
    return s

def compress_coords(arr):
    su = sorted(set(arr))
    comp = {v: i+1 for i, v in enumerate(su)}
    return [comp[v] for v in arr], len(su)

def zfunction(s):
    n = len(s)
    z = [0]*n
    l = r = 0
    for i in range(1, n):
        if i <= r:
            z[i] = min(r - i + 1, z[i - l])
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        if i + z[i] - 1 > r:
            l, r = i, i + z[i] - 1
    return z
