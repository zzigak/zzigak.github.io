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
def trie_init(max_bit):
    return [[0, 0, 0]]

def trie_insert(trie, num, max_bit):
    cur = 0
    trie[cur][2] += 1
    for i in range(max_bit, -1, -1):
        b = (num >> i) & 1
        nxt = trie[cur][b]
        if nxt == 0:
            trie.append([0, 0, 0])
            nxt = len(trie) - 1
            trie[cur][b] = nxt
        cur = nxt
        trie[cur][2] += 1

def trie_delete(trie, num, max_bit):
    cur = 0
    trie[cur][2] -= 1
    for i in range(max_bit, -1, -1):
        b = (num >> i) & 1
        cur = trie[cur][b]
        trie[cur][2] -= 1

def trie_count_less_xor(trie, p, limit, max_bit):
    cur = 0
    res = 0
    for i in range(max_bit, -1, -1):
        if cur == 0 and trie[cur][2] == 0 and trie[cur][0] == 0 and trie[cur][1] == 0:
            break
        pbit = (p >> i) & 1
        lbit = (limit >> i) & 1
        if lbit:
            c0 = trie[cur][pbit]
            if c0:
                res += trie[c0][2]
            cur = trie[cur][pbit ^ 1]
        else:
            cur = trie[cur][pbit]
        if cur == 0:
            break
    return res

def compute_inv_and_flip(arr):
    hashi0 = {}
    hashi1 = {}
    inv1 = inv2 = 0
    for num in arr:
        key = num >> 1
        if num & 1:
            inv2 += hashi0.get(key, 0)
        else:
            inv1 += hashi1.get(key, 0)
        if num & 1:
            hashi1[key] = hashi1.get(key, 0) + 1
        else:
            hashi0[key] = hashi0.get(key, 0) + 1
    if inv2 < inv1:
        return inv2, 1
    return inv1, 0

def apply_flip(a, x, y, z, ops):
    a[x-1] ^= 1
    a[y-1] ^= 1
    a[z-1] ^= 1
    ops.append((x, y, z))

def solve_small(a):
    l = len(a)
    d = sum(a[i] << i for i in range(l))
    usable = []
    if l >= 3:
        usable += [0b111 << i for i in range(l - 2)]
    if l >= 5:
        usable += [0b10101 << i for i in range(l - 4)]
    if l >= 7:
        usable += [0b1001001 << i for i in range(l - 6)]
    best = None
    ul = len(usable)
    for mask in range(1 << ul):
        val = 0
        for j in range(ul):
            if (mask >> j) & 1:
                val ^= usable[j]
        if val == d:
            ops = []
            for j in range(ul):
                if (mask >> j) & 1:
                    bits = []
                    bm = usable[j]
                    for k in range(l):
                        if (bm >> k) & 1:
                            bits.append(k+1)
                    ops.append(tuple(bits))
            if best is None or len(ops) < len(best):
                best = ops
    return best

def process_large(a):
    ops = []
    while len(a) > 10:
        l = len(a)
        last = a[-3:]
        if last == [1, 1, 1]:
            apply_flip(a, l-2, l-1, l, ops)
        elif last == [1, 1, 0]:
            apply_flip(a, l-3, l-2, l-1, ops)
            a[-4] ^= 1
        elif last == [1, 0, 1]:
            apply_flip(a, l-4, l-2, l, ops)
            a[-5] ^= 1
        elif last == [0, 1, 1]:
            nxt = a[-6:-3]
            if nxt == [1, 1, 1]:
                apply_flip(a, l-8, l-4, l, ops)
                apply_flip(a, l-5, l-3, l-1, ops)
                a[-9] ^= 1
            elif nxt == [1, 1, 0]:
                apply_flip(a, l-8, l-4, l, ops)
                apply_flip(a, l-9, l-5, l-1, ops)
                a[-9] ^= 1
                a[-10] ^= 1
            elif nxt == [1, 0, 1]:
                apply_flip(a, l-6, l-3, l, ops)
                apply_flip(a, l-9, l-5, l-1, ops)
                a[-7] ^= 1
                a[-10] ^= 1
            elif nxt == [0, 1, 1]:
                apply_flip(a, l-6, l-3, l, ops)
                apply_flip(a, l-7, l-4, l-1, ops)
                a[-7] ^= 1
                a[-8] ^= 1
            elif nxt == [1, 0, 0]:
                apply_flip(a, l-2, l-1, l, ops)
                apply_flip(a, l-8, l-5, l-2, ops)
                a[-9] ^= 1
            elif nxt == [0, 1, 0]:
                apply_flip(a, l-2, l-1, l, ops)
                apply_flip(a, l-6, l-4, l-2, ops)
                a[-7] ^= 1
            elif nxt == [0, 0, 1]:
                apply_flip(a, l-10, l-5, l, ops)
                apply_flip(a, l-5, l-3, l-1, ops)
                a[-11] ^= 1
            elif nxt == [0, 0, 0]:
                apply_flip(a, l-8, l-4, l, ops)
                apply_flip(a, l-7, l-4, l-1, ops)
                a[-9] ^= 1
                a[-8] ^= 1
        elif last == [1, 0, 0]:
            apply_flip(a, l-4, l-3, l-2, ops)
            a[-5] ^= 1
            a[-4] ^= 1
        elif last == [0, 1, 0]:
            apply_flip(a, l-5, l-3, l-1, ops)
            a[-6] ^= 1
            a[-4] ^= 1
        elif last == [0, 0, 1]:
            apply_flip(a, l-6, l-3, l, ops)
            a[-7] ^= 1
            a[-4] ^= 1
        a.pop(); a.pop(); a.pop()
    return ops
