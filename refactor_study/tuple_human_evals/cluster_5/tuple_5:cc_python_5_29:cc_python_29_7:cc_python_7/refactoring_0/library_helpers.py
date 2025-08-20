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

def read_ints():
    """
    Read a line of space-separated integers.
    """
    return list(map(int, input().split()))

def z_function(seq):
    """
    Compute Z-function for sequence or string `seq`.
    """
    n = len(seq)
    Z = [0] * n
    l = r = 0
    for i in range(1, n):
        if i <= r:
            Z[i] = min(r - i + 1, Z[i - l])
        while i + Z[i] < n and seq[Z[i]] == seq[i + Z[i]]:
            Z[i] += 1
        if i + Z[i] - 1 > r:
            l, r = i, i + Z[i] - 1
    return Z

def compute_dp(seq, bad_set, MOD):
    """
    Given a sequence of bits `seq`, compute dp array f where f[j] is the number
    of letter-sequences that translate seq[j:].
    """
    n = len(seq)
    f = [0] * (n + 1)
    f[n] = 1
    for j in range(n - 1, -1, -1):
        for k in range(j, min(j + 4, n)):
            if tuple(seq[j:k+1]) not in bad_set:
                f[j] = (f[j] + f[k + 1]) % MOD
    return f

def new_substr_start(seq):
    """
    Return the smallest start index j such that seq[j:] is a new substring
    (i.e., hasn't appeared before). Uses Z-function on reversed seq.
    """
    z = z_function(seq[::-1])
    return len(seq) - max(z)
