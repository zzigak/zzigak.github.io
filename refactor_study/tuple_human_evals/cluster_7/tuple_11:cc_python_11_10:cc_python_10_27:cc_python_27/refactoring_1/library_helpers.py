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
def init_trie():
    return [0, None, None]

def trie_insert(root, num, max_bit):
    root[0] += 1
    node = root
    for b in range(max_bit, -1, -1):
        bit = (num >> b) & 1
        child = node[1 + bit]
        if child is None:
            child = [0, None, None]
            node[1 + bit] = child
        child[0] += 1
        node = child

def trie_delete(root, num, max_bit):
    root[0] -= 1
    node = root
    for b in range(max_bit, -1, -1):
        bit = (num >> b) & 1
        child = node[1 + bit]
        child[0] -= 1
        node = child

def count_xor_less(root, num, limit, max_bit):
    node = root
    total = 0
    for b in range(max_bit, -1, -1):
        if node is None:
            break
        pbit = (num >> b) & 1
        lbit = (limit >> b) & 1
        if lbit == 1:
            child = node[1 + pbit]
            if child:
                total += child[0]
            node = node[1 + (pbit ^ 1)]
        else:
            node = node[1 + pbit]
    return total

def compute_bit_inversions(vals):
    from collections import defaultdict
    cnt0 = defaultdict(int)
    cnt1 = defaultdict(int)
    inv0 = inv1 = 0
    for v in vals:
        prefix = v >> 1
        bit = v & 1
        if bit == 0:
            inv0 += cnt1[prefix]
            cnt0[prefix] += 1
        else:
            inv1 += cnt0[prefix]
            cnt1[prefix] += 1
    return inv0, inv1

def shift_list(vals):
    return [v >> 1 for v in vals]

def find_small_operations(a):
    l = len(a)
    d = 0
    for i, v in enumerate(a):
        if v:
            d |= 1 << i
    if d == 0:
        return []
    usable = []
    if l >= 3:
        for i in range(l - 2):
            usable.append(0b111 << i)
    if l >= 5:
        for i in range(l - 4):
            usable.append(0b10101 << i)
    if l >= 7:
        for i in range(l - 6):
            usable.append(0b1001001 << i)
    best = None
    for mask in range(1 << len(usable)):
        s = 0
        for i in range(len(usable)):
            if (mask >> i) & 1:
                s ^= usable[i]
        if s == d:
            ops = []
            for i in range(len(usable)):
                if (mask >> i) & 1:
                    used = usable[i]
                    t = [pos + 1 for pos in range(l) if (used >> pos) & 1]
                    ops.append(t)
            if best is None or len(ops) < len(best):
                best = ops
    return best
