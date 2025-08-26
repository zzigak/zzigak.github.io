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
from collections import defaultdict

def init_trie(max_bit):
    # returns a trie as list of [child0, child1, count]
    return [[-1, -1, 0]]

def trie_modify(trie, num, max_bit, delta):
    # insert or delete num with delta=+1 or -1
    node = 0
    trie[node][2] += delta
    for i in range(max_bit, -1, -1):
        b = (num >> i) & 1
        nxt = trie[node][b]
        if nxt == -1:
            nxt = len(trie)
            trie[node][b] = nxt
            trie.append([-1, -1, 0])
        node = nxt
        trie[node][2] += delta

def count_xor_less(trie, x, limit, max_bit):
    # count numbers num in trie so that (num XOR x) < limit
    node = 0
    cnt = 0
    for i in range(max_bit, -1, -1):
        if node == -1:
            break
        xb = (x >> i) & 1
        lb = (limit >> i) & 1
        if lb == 1:
            # we can take branch where num_bit^x_bit == 0
            eq = trie[node][xb]
            if eq != -1:
                cnt += trie[eq][2]
            node = trie[node][xb ^ 1]
        else:
            node = trie[node][xb]
    return cnt

def compute_bit_inversions(arr, bit):
    # for each prefix = num>>(bit+1), count inv0: 1->0 and inv1: 0->1
    inv0 = inv1 = 0
    c0 = defaultdict(int)
    c1 = defaultdict(int)
    shift = bit + 1
    for num in arr:
        prefix = num >> shift
        b = (num >> bit) & 1
        if b == 0:
            inv1 += c1[prefix]
            c0[prefix] += 1
        else:
            inv0 += c0[prefix]
            c1[prefix] += 1
    return inv0, inv1

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
        s = 0
        m = mask
        idx = 0
        while m:
            if m & 1:
                s ^= usable[idx]
            m >>= 1
            idx += 1
        if s == d:
            # build answer
            ans = []
            m2 = mask
            idx = 0
            while m2:
                if m2 & 1:
                    used = usable[idx]
                    t = []
                    pos = 1
                    while used:
                        if used & 1:
                            t.append(pos)
                        used >>= 1
                        pos += 1
                    ans.append(t)
                m2 >>= 1
                idx += 1
            if best is None or len(ans) < len(best):
                best = ans
    return best

def solve_all(a):
    if len(a) <= 10:
        return solve_small(a)
    arr = list(a)
    ops = []
    while len(arr) > 10:
        l = len(arr)
        last = arr[-3:]
        if last == [1,1,1]:
            ops.append([l-2, l-1, l])
        elif last == [1,1,0]:
            ops.append([l-3, l-2, l-1])
            arr[-4] ^= 1
        elif last == [1,0,1]:
            ops.append([l-4, l-2, l])
            arr[-5] ^= 1
        elif last == [0,1,1]:
            nxt = arr[-6:-3]
            if nxt == [1,1,1]:
                ops.append([l-8, l-4, l])
                ops.append([l-5, l-3, l-1])
                arr[-9] ^= 1
            elif nxt == [1,1,0]:
                ops.append([l-8, l-4, l])
                ops.append([l-9, l-5, l-1])
                arr[-9] ^= 1
                arr[-10] ^= 1
            elif nxt == [1,0,1]:
                ops.append([l-6, l-3, l])
                ops.append([l-9, l-5, l-1])
                arr[-7] ^= 1
                arr[-10] ^= 1
            elif nxt == [0,1,1]:
                ops.append([l-6, l-3, l])
                ops.append([l-7, l-4, l-1])
                arr[-7] ^= 1
                arr[-8] ^= 1
            elif nxt == [1,0,0]:
                ops.append([l-2, l-1, l])
                ops.append([l-8, l-5, l-2])
                arr[-9] ^= 1
            elif nxt == [0,1,0]:
                ops.append([l-2, l-1, l])
                ops.append([l-6, l-4, l-2])
                arr[-7] ^= 1
            elif nxt == [0,0,1]:
                ops.append([l-10, l-5, l])
                ops.append([l-5, l-3, l-1])
                arr[-11] ^= 1
            elif nxt == [0,0,0]:
                ops.append([l-8, l-4, l])
                ops.append([l-7, l-4, l-1])
                arr[-9] ^= 1
                arr[-8] ^= 1
            arr.pop(); arr.pop(); arr.pop()
            continue
        elif last == [1,0,0]:
            ops.append([l-4, l-3, l-2])
            arr[-5] ^= 1; arr[-4] ^= 1
        elif last == [0,1,0]:
            ops.append([l-5, l-3, l-1])
            arr[-6] ^= 1; arr[-4] ^= 1
        elif last == [0,0,1]:
            ops.append([l-6, l-3, l])
            arr[-7] ^= 1; arr[-4] ^= 1
        arr.pop(); arr.pop(); arr.pop()
    while len(arr) < 8:
        arr.append(0)
    small = solve_small(arr)
    if small is None:
        return None
    ops += small
    return ops


# ########################################
#
#  PROGRAM REFACTORINGS
#
# ########################################

# ########## PROGRAM: node_10:cc_python_10 ##########

from codebank import *

def main():
    import sys
    data = sys.stdin.read().split()
    n = int(data[0])
    arr = list(map(int, data[1:1+n]))
    ans_inv = 0
    x = 0
    MAXB = 30
    # inv1 = inversions if xbit=0, inv0 = inversions if xbit=1
    for bit in range(MAXB, -1, -1):
        inv0, inv1 = compute_bit_inversions(arr, bit)
        # choose xbit = 0 if inv1 <= inv0, else xbit = 1
        if inv1 <= inv0:
            ans_inv += inv1
        else:
            ans_inv += inv0
            x |= 1 << bit
    print(ans_inv, x)

if __name__ == "__main__":
    main()

# ########## PROGRAM: node_11:cc_python_11 ##########

from codebank import *

CONSTANT = 30

def main():
    import sys
    data = sys.stdin
    q = int(data.readline())
    trie = init_trie(CONSTANT)
    for _ in range(q):
        l = list(map(int, data.readline().split()))
        op = l[0]
        if op == 1:
            trie_modify(trie, l[1], CONSTANT, 1)
        elif op == 2:
            trie_modify(trie, l[1], CONSTANT, -1)
        else:
            print(count_xor_less(trie, l[1], l[2], CONSTANT))

if __name__ == "__main__":
    main()

# ########## PROGRAM: node_27:cc_python_27 ##########

from codebank import *

def main():
    import sys
    stdin = sys.stdin
    n = int(stdin.readline())
    a = list(map(int, stdin.readline().split()))
    ops = solve_all(a)
    if ops is None:
        print("NO")
        return
    print("YES")
    print(len(ops))
    for x, y, z in ops:
        print(x, y, z)

if __name__ == "__main__":
    main()
