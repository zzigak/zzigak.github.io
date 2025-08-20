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
def trie_update(root, num, delta, max_bit):
    node = root
    for i in range(max_bit, -1, -1):
        node['cnt'] = node.get('cnt', 0) + delta
        bit = (num >> i) & 1
        if node.get(bit) is None:
            node[bit] = {'cnt': 0}
        node = node[bit]
    node['cnt'] = node.get('cnt', 0) + delta

def trie_count_less(root, num, limit, max_bit):
    count = 0
    node = root
    for i in range(max_bit, -1, -1):
        if node is None:
            break
        b_num = (num >> i) & 1
        b_lim = (limit >> i) & 1
        if b_lim:
            child = node.get(b_num)
            if child:
                count += child.get('cnt', 0)
            node = node.get(1 - b_num)
        else:
            node = node.get(b_num)
    return count

def bit_inversion_counts(vals):
    inv0 = inv1 = 0
    c0 = {}
    c1 = {}
    for v in vals:
        key = v >> 1
        if v & 1:
            inv1 += c0.get(key, 0)
            c1[key] = c1.get(key, 0) + 1
        else:
            inv0 += c1.get(key, 0)
            c0[key] = c0.get(key, 0) + 1
    return inv0, inv1

def apply_op(a, ops, x, y, z):
    a[x-1] ^= 1
    a[y-1] ^= 1
    a[z-1] ^= 1
    ops.append((x, y, z))

def solve_small(a):
    l = len(a)
    d = sum((a[i] << i) for i in range(l))
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
            ans = []
            for idx in range(ul):
                if (mask >> idx) & 1:
                    bits = usable[idx]
                    pos = 1
                    triple = []
                    while bits:
                        if bits & 1:
                            triple.append(pos)
                        bits >>= 1
                        pos += 1
                    ans.append(triple)
            if best is None or len(ans) < len(best):
                best = ans
    return best

def solve_large(a, ops):
    while len(a) > 10:
        l = len(a)
        last = a[-3:]
        if last == [1, 1, 1]:
            apply_op(a, ops, l-2, l-1, l)
        elif last == [1, 1, 0]:
            apply_op(a, ops, l-3, l-2, l-1)
            a[-4] ^= 1
        elif last == [1, 0, 1]:
            apply_op(a, ops, l-4, l-2, l)
            a[-5] ^= 1
        elif last == [0, 1, 1]:
            nxt = a[-6:-3]
            if nxt == [1, 1, 1]:
                apply_op(a, ops, l-8, l-4, l)
                apply_op(a, ops, l-5, l-3, l-1)
                a[-9] ^= 1
            elif nxt == [1, 1, 0]:
                apply_op(a, ops, l-8, l-4, l)
                apply_op(a, ops, l-9, l-5, l-1)
                a[-9] ^= 1; a[-10] ^= 1
            elif nxt == [1, 0, 1]:
                apply_op(a, ops, l-6, l-3, l)
                apply_op(a, ops, l-9, l-5, l-1)
                a[-7] ^= 1; a[-10] ^= 1
            elif nxt == [0, 1, 1]:
                apply_op(a, ops, l-6, l-3, l)
                apply_op(a, ops, l-7, l-4, l-1)
                a[-7] ^= 1; a[-8] ^= 1
            elif nxt == [1, 0, 0]:
                apply_op(a, ops, l-2, l-1, l)
                apply_op(a, ops, l-8, l-5, l-2)
                a[-9] ^= 1
            elif nxt == [0, 1, 0]:
                apply_op(a, ops, l-2, l-1, l)
                apply_op(a, ops, l-6, l-4, l-2)
                a[-7] ^= 1
            elif nxt == [0, 0, 1]:
                apply_op(a, ops, l-10, l-5, l)
                apply_op(a, ops, l-5, l-3, l-1)
                a[-11] ^= 1
            elif nxt == [0, 0, 0]:
                apply_op(a, ops, l-8, l-4, l)
                apply_op(a, ops, l-7, l-4, l-1)
                a[-9] ^= 1; a[-8] ^= 1
            a.pop(); a.pop(); a.pop()
            continue
        elif last == [1, 0, 0]:
            apply_op(a, ops, l-4, l-3, l-2)
            a[-5] ^= 1; a[-4] ^= 1
        elif last == [0, 1, 0]:
            apply_op(a, ops, l-5, l-3, l-1)
            a[-6] ^= 1; a[-4] ^= 1
        elif last == [0, 0, 1]:
            apply_op(a, ops, l-6, l-3, l)
            a[-7] ^= 1; a[-4] ^= 1
        a.pop(); a.pop(); a.pop()
