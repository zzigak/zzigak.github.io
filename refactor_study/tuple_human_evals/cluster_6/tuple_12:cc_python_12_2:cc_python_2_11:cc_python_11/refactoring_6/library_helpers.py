# ==== RETRIEVED HELPER FUNCTIONS (NONE) ====

# ==== NEW HELPER FUNCTIONS ====
def read_ints():
    return map(int, input().split())

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def reduce_fraction(n, d):
    g = gcd(n, d)
    return n//g, d//g

def compute_princess_win_prob(w, b):
    p = [[0.0]*(b+1) for _ in range(w+1)]
    for i in range(1, w+1):
        p[i][0] = 1.0
    for i in range(1, w+1):
        for j in range(1, b+1):
            total = i + j
            p[i][j] = i/total
            if j >= 3:
                p[i][j] += (j/total)*((j-1)/(total-1))*((j-2)/(total-2))*p[i][j-3]
            if j >= 2:
                p[i][j] += (j/total)*((j-1)/(total-1))*(i/(total-2))*p[i-1][j-2]
    return p[w][b]

def group_improvements(n, k):
    l = [[[] for _ in range(3)] for _ in range(k)]
    for idx in range(1, n+1):
        t, i, b = map(int, input().split())
        l[i-1][t-1].append((b, idx))
    return l

def collect_operations(a_i, assigns, adds, muls):
    ops = []
    adds_sorted = sorted(adds, reverse=True)
    if assigns and assigns[0][0] > a_i:
        diff, idx = assigns[0][0] - a_i, assigns[0][1]
        adds_sorted = sorted(adds + [(diff, idx)], reverse=True)
    s = a_i
    for add, idx in adds_sorted:
        ops.append(((s+add)/s, idx))
        s += add
    for mul, idx in muls:
        ops.append((mul, idx))
    return ops

def top_m_by(ops, m):
    return set(idx for _, idx in sorted(ops, reverse=True)[:m])

def print_selected_indices(l, selected):
    for skill_ops in l:
        for ops_list in skill_ops:
            for _, idx in ops_list:
                if idx in selected:
                    print(idx, end=' ')
