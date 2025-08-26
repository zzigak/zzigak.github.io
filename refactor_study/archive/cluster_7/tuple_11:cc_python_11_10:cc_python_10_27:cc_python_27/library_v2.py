# ########## LIBRARY HELPERS ##########

# ==== RETRIEVED HELPER FUNCTIONS ====
def count_xor_combinations(table, target):
    # Success rate: 1/1

    return dfs_xor(table, target, 0, 0)

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

def find_zero_xor_triple(l, r, limit=2000):
    # Success rate: 1/1

    end = min(r, l + limit)
    for i in range(l, end + 1):
        for j in range(i + 1, end + 1):
            c = i ^ j
            if c != i and c != j and (l <= c <= r):
                return (i, j, c)
    return None

def prefix_xors(arr):
    # Success rate: 2/2

    pref = [0]
    for x in arr:
        pref.append(pref[-1] ^ x)
    return pref

def dfs_xor(table, target, index, cur):
    # Success rate: 1/1

    if index == len(table):
        return int(cur == target)
    cnt = 0
    for v in table[index]:
        cnt += dfs_xor(table, target, index + 1, cur ^ v)
    return cnt

def trie_find_min_xor(trie, x, max_bit):
    # Success rate: 1/1

    now = 0
    ans = 0
    for i in range(max_bit, -1, -1):
        bit = x >> i & 1
        if trie[now][bit] and trie[trie[now][bit]][2] > 0:
            now = trie[now][bit]
        else:
            now = trie[now][bit ^ 1]
            ans |= 1 << i
        trie[now][2] -= 1
    return ans

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


# ==== NEW HELPER FUNCTIONS ====
def trie_insert(root, num, delta, max_bit=28):
    node = root
    node['cnt'] = node.get('cnt', 0) + delta
    for i in range(max_bit, -1, -1):
        b = (num >> i) & 1
        if b not in node:
            node[b] = {'cnt': 0}
        node = node[b]
        node['cnt'] = node.get('cnt', 0) + delta

def trie_count_less(root, x, limit, max_bit=28):
    node = root
    res = 0
    for i in range(max_bit, -1, -1):
        if not node:
            break
        xb = (x >> i) & 1
        lb = (limit >> i) & 1
        if lb:
            child = node.get(xb)
            if child:
                res += child.get('cnt', 0)
            node = node.get(1 - xb)
        else:
            node = node.get(xb)
    return res

def count_bit_inversions(arr):
    inv1 = inv2 = 0
    c0 = {}
    c1 = {}
    for v in arr:
        p = v >> 1
        bit = v & 1
        if bit == 0:
            inv1 += c1.get(p, 0)
            c0[p] = c0.get(p, 0) + 1
        else:
            inv2 += c0.get(p, 0)
            c1[p] = c1.get(p, 0) + 1
    return inv1, inv2

def solve_small(a):
    l = len(a)
    d = 0
    for i, bit in enumerate(a):
        if bit:
            d |= (1 << i)
    if d == 0:
        return []
    usable = []
    if l >= 3:
        for i in range(l - 3 + 1):
            usable.append(0b111 << i)
    if l >= 5:
        for i in range(l - 5 + 1):
            usable.append(0b10101 << i)
    if l >= 7:
        for i in range(l - 7 + 1):
            usable.append(0b1001001 << i)
    ul = len(usable)
    best = None
    for m in range(1 << ul):
        start = 0
        for i in range(ul):
            if (m >> i) & 1:
                start ^= usable[i]
        if start == d:
            ans = []
            for i in range(ul):
                if (m >> i) & 1:
                    bits = []
                    us = usable[i]
                    idx = 1
                    while us:
                        if us & 1:
                            bits.append(idx)
                        us >>= 1
                        idx += 1
                    ans.append(bits)
            if best is None or len(ans) < len(best):
                best = ans
    return best


# ########################################
#
