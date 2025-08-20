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
def trie_init():
    # Returns a trie represented by [children_list, count_list]
    return [[[-1, -1]], [0]]

def trie_add(trie, num, delta=1, bits=28):
    # Inserts or removes (delta=±1) num into trie
    ch, cnt = trie
    node = 0
    cnt[node] += delta
    for b in range(bits, -1, -1):
        bit = (num >> b) & 1
        nxt = ch[node][bit]
        if nxt == -1:
            nxt = len(ch)
            ch[node][bit] = nxt
            ch.append([-1, -1])
            cnt.append(0)
        node = nxt
        cnt[node] += delta

def trie_count_xor_less(trie, x, limit, bits=28):
    # Counts how many y in trie satisfy (x xor y) < limit
    ch, cnt = trie
    res = 0
    node = 0
    for b in range(bits, -1, -1):
        if node == -1: break
        bx = (x >> b) & 1
        bl = (limit >> b) & 1
        if bl:
            c = ch[node][bx]
            if c != -1:
                res += cnt[c]
            node = ch[node][bx ^ 1]
        else:
            node = ch[node][bx]
    return res

def process_bit(arr):
    # Processes one bit layer: returns inv1, inv2 and arr>>1
    from collections import defaultdict
    h0 = defaultdict(int)
    h1 = defaultdict(int)
    inv1 = inv2 = 0
    new = []
    for v in arr:
        p = v >> 1
        b = v & 1
        if b == 0:
            inv1 += h1[p]
            h0[p] += 1
        else:
            inv2 += h0[p]
            h1[p] += 1
        new.append(p)
    return inv1, inv2, new

def apply_op(a, ops, x, y, z):
    # Applies flip at positions x,y,z (1-based) and records it
    ops.append([x, y, z])
    a[x-1] ^= 1; a[y-1] ^= 1; a[z-1] ^= 1

def solve_small(a):
    # Brute-force small n<=10 via bitmasking of usable triples
    l = len(a)
    d = sum(a[i] << i for i in range(l))
    if d == 0:
        return []
    usable = []
    masks = {3:0b111, 5:0b10101, 7:0b1001001}
    for sz, m in masks.items():
        for i in range(l - sz + 1):
            usable.append(m << i)
    best = None
    ul = len(usable)
    for m in range(1 << ul):
        s = 0
        ops = []
        for i in range(ul):
            if (m >> i) & 1:
                s ^= usable[i]
                ops.append(i)
        if s == d:
            ans = []
            for idx in ops:
                mask = usable[idx]
                pos = 1
                triple = []
                while mask:
                    if mask & 1:
                        triple.append(pos)
                    mask >>= 1; pos += 1
                ans.append(triple)
            if best is None or len(ans) < len(best):
                best = ans
    return best
