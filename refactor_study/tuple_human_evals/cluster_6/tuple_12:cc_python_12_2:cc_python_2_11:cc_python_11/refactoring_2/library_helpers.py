# ==== RETRIEVED HELPER FUNCTIONS (NONE) ====

# ==== NEW HELPER FUNCTIONS ====
def read_ints():
    return list(map(int, input().split()))

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def reduce_fraction(numer, denom):
    g = gcd(numer, denom)
    return numer // g, denom // g

def classify_operations(k, ops):
    lst = [[[], [], []] for _ in range(k)]
    for t, i, b, idx in ops:
        lst[i-1][t-1].append((b, idx))
    return lst

def select_best_adds_per_skill(skill_val, assigns, adds):
    best = list(adds)
    if assigns:
        max_asg = max(assigns, key=lambda x: x[0])
        if max_asg[0] > skill_val:
            best.append((max_asg[0] - skill_val, max_asg[1]))
    best.sort(key=lambda x: x[0], reverse=True)
    return best

def build_operation_candidates(a_list, list_by_skill):
    ops = []
    for i, val in enumerate(a_list):
        assigns, adds, mults = list_by_skill[i]
        best_adds = select_best_adds_per_skill(val, assigns, adds)
        s = val
        for add, idx in best_adds:
            ops.append(((s + add) / s, idx))
            s += add
        for mul, idx in mults:
            ops.append((mul, idx))
    return ops

def select_top_indices(op_list, m):
    op_list.sort(key=lambda x: x[0], reverse=True)
    return {idx for _, idx in op_list[:m]}

def flatten_selected_ops(list_by_skill, selected_set):
    res = []
    for skill_ops in list_by_skill:
        for type_list in skill_ops:
            for _, idx in type_list:
                if idx in selected_set:
                    res.append(idx)
    return res

def compute_dp_probability(w, b):
    p = [[0.0] * (b + 1) for _ in range(w + 1)]
    for i in range(1, w + 1):
        p[i][0] = 1.0
    for i in range(1, w + 1):
        for j in range(1, b + 1):
            total = i + j
            prob = i / total
            if j >= 3:
                prob += (j / total) * ((j - 1) / (total - 1)) * ((j - 2) / (total - 2)) * p[i][j - 3]
            if j >= 2:
                prob += (j / total) * ((j - 1) / (total - 1)) * (i / (total - 2)) * p[i - 1][j - 2]
            p[i][j] = prob
    return p[w][b]
