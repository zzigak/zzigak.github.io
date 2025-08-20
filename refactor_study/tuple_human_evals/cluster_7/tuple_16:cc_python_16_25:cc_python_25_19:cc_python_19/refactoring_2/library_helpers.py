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
def ones_mask(x):
    return (1 << x.bit_length()) - 1 if x else 0

def compute_beauty_permutation(n):
    ans = [0] * (n + 1)
    used = set()
    for i in range(n, 0, -1):
        if i not in used:
            m = ones_mask(i)
            j = i ^ m
            used.add(i); used.add(j)
            ans[i] = j; ans[j] = i
    fin = sum(i ^ ans[i] for i in range(n + 1))
    return fin, ans

def xor_sum_array(u, v):
    if u > v or (v - u) & 1:
        return None
    if u == v:
        return [] if u == 0 else [u]
    a = (v - u) // 2
    if (a & u) == 0:
        return [u + a, a]
    return [u, a, a]

def trie_add(tree, x, bits=30):
    node = 0
    tree[node][2] += 1
    for i in range(bits - 1, -1, -1):
        b = (x >> i) & 1
        nxt = tree[node][b]
        if nxt == 0:
            nxt = len(tree)
            tree[node][b] = nxt
            tree.append([0, 0, 0])
        node = nxt
        tree[node][2] += 1

def trie_pop_min_xor(tree, x, bits=30):
    node = 0
    res = 0
    for i in range(bits - 1, -1, -1):
        b = (x >> i) & 1
        if tree[node][b] and tree[tree[node][b]][2] > 0:
            node = tree[node][b]
        else:
            node = tree[node][b ^ 1]
            res |= (1 << i)
        tree[node][2] -= 1
    return res
