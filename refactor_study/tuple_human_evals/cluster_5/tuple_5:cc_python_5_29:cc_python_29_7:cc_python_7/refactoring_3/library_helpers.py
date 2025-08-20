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
def bit_update(bit, n, idx, val):
    """
    Update Fenwick tree `bit` of size `n` by adding `val` at position `idx`.
    """
    while idx <= n:
        bit[idx] += val
        idx += idx & -idx

def bit_query(bit, idx):
    """
    Query Fenwick tree `bit` for the prefix sum up to `idx`.
    """
    s = 0
    while idx > 0:
        s += bit[idx]
        idx -= idx & -idx
    return s

def compute_z(s):
    """
    Compute the Z-array of string `s`.
    Z[i] = longest substring starting at i that is also a prefix of s.
    """
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

def find_longest_border(s):
    """
    Find the longest substring which is prefix, suffix, and appears elsewhere in `s`.
    Return that substring or None.
    """
    Z = compute_z(s)
    n = len(s)
    # collect all border lengths = n - i for positions where suffix matches prefix
    borders = [n - i for i, z in enumerate(Z) if i + z == n]
    if not borders:
        return None
    max_z = max(Z)
    # try longest border first
    for l in sorted(borders, reverse=True):
        if max_z >= l:
            return s[:l]
    return None

def count_dp(s, bad, mod):
    """
    Given binary string `s`, count ways to parse suffixes into letters,
    where substrings of length 1..4 not in `bad` form letters.
    Return DP array f of size len(s)+1, f[i]=#ways to parse s[i:].
    """
    n = len(s)
    f = [0] * (n + 1)
    f[n] = 1
    for j in range(n - 1, -1, -1):
        total = 0
        # try code lengths 1..4
        for k in range(j + 1, min(j + 4, n) + 1):
            if s[j:k] not in bad:
                total = (total + f[k]) % mod
        f[j] = total
    return f
