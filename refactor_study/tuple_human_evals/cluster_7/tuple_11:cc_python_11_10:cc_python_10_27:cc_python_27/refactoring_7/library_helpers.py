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
def trie_new():
    return [[0, -1, -1]]

def trie_insert(nodes, x, bit_max, delta):
    cur = 0
    for i in range(bit_max, -1, -1):
        nodes[cur][0] += delta
        b = (x >> i) & 1
        nc = nodes[cur][1 + b]
        if nc < 0:
            nc = len(nodes)
            nodes[cur][1 + b] = nc
            nodes.append([0, -1, -1])
        cur = nc
    nodes[cur][0] += delta

def trie_count_less(nodes, x, limit, bit_max):
    res = 0
    cur = 0
    for i in range(bit_max, -1, -1):
        if cur < 0:
            break
        kbit = (limit >> i) & 1
        b = (x >> i) & 1
        if kbit:
            child = nodes[cur][1 + b]
            if child >= 0:
                res += nodes[child][0]
            cur = nodes[cur][1 + (b ^ 1)]
        else:
            cur = nodes[cur][1 + b]
    return res

def count_bit_inversions(arr):
    c0 = c1 = inv10 = inv01 = 0
    for v in arr:
        if v & 1:
            inv01 += c0
            c1 += 1
        else:
            inv10 += c1
            c0 += 1
    return inv10, inv01

def shift_array(arr):
    return [v >> 1 for v in arr]

def solve_small(a):
    l = len(a)
    d = 0
    for i, v in enumerate(a):
        d |= v << i
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
    ul = len(usable)
    best = None
    for mask in range(1 << ul):
        start = 0
        for idx in range(ul):
            if (mask >> idx) & 1:
                start ^= usable[idx]
        if start == d:
            answer = []
            for idx in range(ul):
                if (mask >> idx) & 1:
                    used = usable[idx]
                    pos = 1
                    op = []
                    while used:
                        if used & 1:
                            op.append(pos)
                        used >>= 1
                        pos += 1
                    answer.append(op)
            if best is None or len(answer) < len(best):
                best = answer
    return best

def flip_positions(a, ops, positions):
    for p in positions:
        a[p-1] ^= 1
    ops.append(positions)
