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
def trie_update(trie, num, delta, max_bit):
    cur = 0
    trie[cur][2] += delta
    for bit in range(max_bit, -1, -1):
        b = (num >> bit) & 1
        nxt = trie[cur][b]
        if not nxt and delta > 0:
            nxt = len(trie)
            trie[cur][b] = nxt
            trie.append([0, 0, 0])
        if not nxt:
            return
        cur = nxt
        trie[cur][2] += delta

def trie_count_less(trie, num, limit, max_bit):
    total = 0
    cur = 0
    for bit in range(max_bit, -1, -1):
        lb = (limit >> bit) & 1
        nb = (num >> bit) & 1
        if lb:
            child = trie[cur][nb]
            if child:
                total += trie[child][2]
            cur = trie[cur][nb ^ 1]
        else:
            cur = trie[cur][nb]
        if not cur:
            break
    return total

def calc_bit_inversions_and_shift(arr):
    hashi0 = {}
    hashi1 = {}
    inv1 = inv2 = 0
    arr2 = []
    for j in arr:
        p = j >> 1
        bit = j & 1
        if bit == 0 and p in hashi1:
            inv1 += hashi1[p]
        if bit == 1 and p in hashi0:
            inv2 += hashi0[p]
        if bit:
            hashi1[p] = hashi1.get(p, 0) + 1
        else:
            hashi0[p] = hashi0.get(p, 0) + 1
        arr2.append(p)
    return inv1, inv2, arr2

def brute_solve_small(a):
    l = len(a)
    d = sum((a[i] << i) for i in range(l))
    if d == 0:
        return []
    usable = []
    ops = []
    if l >= 3:
        for i in range(l - 2):
            m = 0b111 << i
            usable.append(m); ops.append((i+1, i+2, i+3))
    if l >= 5:
        for i in range(l - 4):
            m = 0b10101 << i
            usable.append(m); ops.append((i+1, i+3, i+5))
    if l >= 7:
        for i in range(l - 6):
            m = 0b1001001 << i
            usable.append(m); ops.append((i+1, i+4, i+7))
    ul = len(usable)
    best = None
    for mask in range(1 << ul):
        s = 0; idx = 0; m = mask; cur_ops = []
        while m:
            if m & 1:
                s ^= usable[idx]
                cur_ops.append(ops[idx])
            m >>= 1; idx += 1
        if s == d and (best is None or len(cur_ops) < len(best)):
            best = list(cur_ops)
    return best
