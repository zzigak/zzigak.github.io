# ==== RETRIEVED HELPER FUNCTIONS (NONE) ====

# ==== NEW HELPER FUNCTIONS ====
def read_ints():
    return list(map(int, input().split()))

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def reduce_fraction(a, b):
    g = gcd(a, b)
    return a // g, b // g

def compute_princess_probability(w, b):
    p = [[0.0] * (b + 1) for _ in range(w + 1)]
    for i in range(1, w + 1):
        p[i][0] = 1.0
    for i in range(1, w + 1):
        for j in range(1, b + 1):
            tot = i + j
            res = i / tot
            # princess draws black, then dragon's turn
            if j >= 2:
                # dragon draws black then panic jump
                if j >= 3:
                    res += (j / tot) * ((j - 1) / (tot - 1)) * ((j - 2) / (tot - 2)) * p[i][j - 3]
                # dragon draws black then draws white
                res += (j / tot) * ((j - 1) / (tot - 1)) * (i / (tot - 2)) * p[i - 1][j - 2]
            p[i][j] = res
    return p[w][b]

def skill_gains(a_i, assign_ops, add_ops, mul_ops):
    # assign_ops, add_ops, mul_ops are lists of (b_value, index)
    assigns = sorted(assign_ops, reverse=True)
    adds    = sorted(add_ops,    reverse=True)
    muls    = sorted(mul_ops,    reverse=True)
    # convert best assign to an add if beneficial
    if assigns and assigns[0][0] > a_i:
        adds.insert(0, (assigns[0][0] - a_i, assigns[0][1]))
    gains = []
    s = a_i
    for add, idx in adds:
        gains.append(((s + add) / s, idx))
        s += add
    for mul, idx in muls:
        gains.append((mul, idx))
    return gains

def build_operations(a, l):
    ops = []
    for a_i, ops_list in zip(a, l):
        gains = skill_gains(a_i, ops_list[0], ops_list[1], ops_list[2])
        ops.extend(gains)
    return ops
