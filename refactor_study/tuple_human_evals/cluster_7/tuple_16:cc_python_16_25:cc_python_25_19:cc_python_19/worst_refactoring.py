# ########## LIBRARY HELPERS ##########

# ==== RETRIEVED HELPER FUNCTIONS ====
def min_pair_combinations(m):
    # Success rate: 1/1

    half = m // 2
    return half * (half - 1) // 2 + (m - half) * (m - half - 1) // 2

def compute_prime_mask(n, primes):
    # Success rate: 1/1

    mask = 0
    for (i, p) in enumerate(primes):
        while n % p == 0:
            n //= p
            mask ^= 1 << i
    return mask

def precompute_pow2(n, mod):
    # Success rate: 1/1

    pows = [1] * (n + 1)
    for i in range(1, n + 1):
        pows[i] = pows[i - 1] * 2 % mod
    return pows

def find_zero_xor_triple(l, r, limit=2000):
    # Success rate: 1/1

    end = min(r, l + limit)
    for i in range(l, end + 1):
        for j in range(i + 1, end + 1):
            c = i ^ j
            if c != i and c != j and (l <= c <= r):
                return (i, j, c)
    return None

def xor_subset_dp(mask_freq, mod):
    # Success rate: 1/1

    dp = {0: 1}
    for (mask, cnt) in mask_freq.items():
        half = pow(2, cnt - 1, mod)
        new_dp = {}
        for (prev, val) in dp.items():
            new_dp[prev] = (new_dp.get(prev, 0) + val * half) % mod
            new_dp[prev ^ mask] = (new_dp.get(prev ^ mask, 0) + val * half) % mod
        dp = new_dp
    return dp.get(0, 0)

def prefix_xors(arr):
    # Success rate: 2/2

    pref = [0]
    for x in arr:
        pref.append(pref[-1] ^ x)
    return pref

def xor_upto(n):
    # Success rate: 1/1

    r = n % 4
    if r == 0:
        return n
    if r == 1:
        return 1
    if r == 2:
        return n + 1
    return 0

def count_pairs_bit(vals, b1):
    # Success rate: 1/1

    import bisect
    b2 = 2 * b1
    cnt = 0
    for (j, v) in enumerate(vals):
        (L1, R1) = (b1 - v, b2 - 1 - v)
        cnt += bisect.bisect_right(vals, R1, j + 1) - bisect.bisect_left(vals, L1, j + 1)
        (L2, R2) = (b2 + b1 - v, 2 * b2 - 1 - v)
        cnt += bisect.bisect_right(vals, R2, j + 1) - bisect.bisect_left(vals, L2, j + 1)
    return cnt & 1

def count_pairs(freq_dict):
    # Success rate: 1/1

    return sum((v * (v - 1) // 2 for v in freq_dict.values()))


# ==== NEW HELPER FUNCTIONS ====
def compute_full_mask(i):
    """Return mask of all 1s of the bit-length of i."""
    return (1 << i.bit_length()) - 1

def build_max_beauty_perm(n):
    """Build permutation of 0..n maximizing sum of i^p[i]."""
    ans = [0] * (n + 1)
    used = set()
    for i in range(n, -1, -1):
        if i in used:
            continue
        mask = compute_full_mask(i)
        j = i ^ mask
        ans[i], ans[j] = j, i
        used.add(i)
        used.add(j)
    beauty = sum(i ^ ans[i] for i in range(n + 1))
    return ans, beauty

def solve_xor_sum(u, v):
    """
    Find shortest array whose xor is u and sum is v.
    Return list or None if impossible.
    """
    if u > v or (v - u) % 2:
        return None
    if u == v:
        return [] if u == 0 else [u]
    x = (v - u) // 2
    # try two elements
    if ((u + x) ^ x) == u:
        return [u + x, x]
    # fallback to three elements
    return [u, x, x]

def build_trie(keys):
    """
    Build a binary trie with counts for 30-bit numbers.
    Each node: [left_index, right_index, count].
    """
    tree = [[0, 0, 0]]
    for x in keys:
        now = 0
        tree[now][2] += 1
        for i in range(29, -1, -1):
            b = (x >> i) & 1
            if tree[now][b] == 0:
                tree[now][b] = len(tree)
                tree.append([0, 0, 0])
            now = tree[now][b]
            tree[now][2] += 1
    return tree

def trie_pop_min_xor(tree, x):
    """
    Pop one key from trie to minimize x^key and return that minimal xor.
    Decrements counts along the path.
    """
    now = 0
    res = 0
    for i in range(29, -1, -1):
        b = (x >> i) & 1
        nxt = tree[now][b]
        if nxt and tree[nxt][2] > 0:
            now = nxt
        else:
            now = tree[now][b ^ 1]
            res |= (1 << i)
        tree[now][2] -= 1
    return res


# ########################################
#
#  PROGRAM REFACTORINGS
#
# ########################################

# ########## PROGRAM: node_16:cc_python_16 ##########

from codebank import *

def main():
    import sys
    data = sys.stdin.readline()
    if not data:
        return
    n = int(data)
    perm, beauty = build_max_beauty_perm(n)
    print(beauty)
    print(*perm)

if __name__ == "__main__":
    main()

# ########## PROGRAM: node_19:cc_python_19 ##########

from codebank import *

def main():
    import sys
    data = sys.stdin.readline
    n = int(data())
    A = list(map(int, data().split()))
    P = list(map(int, data().split()))
    trie = build_trie(P)
    O = [trie_pop_min_xor(trie, a) for a in A]
    print(*O)

if __name__ == "__main__":
    main()

# ########## PROGRAM: node_25:cc_python_25 ##########

from codebank import *

def main():
    import sys
    u, v = map(int, sys.stdin.readline().split())
    res = solve_xor_sum(u, v)
    if res is None:
        print(-1)
    else:
        print(len(res))
        if res:
            print(*res)

if __name__ == "__main__":
    main()
