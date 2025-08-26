# ########## LIBRARY HELPERS ##########

# ==== RETRIEVED HELPER FUNCTIONS (NONE) ====

# ==== NEW HELPER FUNCTIONS ====
def read_ints():
    return list(map(int, input().split()))

def print_float(x, prec=9):
    print(f"{x:.{prec}f}")

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def simplify_fraction(n, d):
    g = gcd(n, d)
    return n // g, d // g

def make_2d(rows, cols, fill_value):
    return [[fill_value for _ in range(cols)] for _ in range(rows)]

def compute_princess_win(w, b):
    p = make_2d(w+1, b+1, 0.0)
    for i in range(1, w+1):
        p[i][0] = 1.0
    for i in range(1, w+1):
        for j in range(1, b+1):
            total = i + j
            prob = i / total
            if j >= 3:
                prob += (j/total) * ((j-1)/(total-1)) * ((j-2)/(total-2)) * p[i][j-3]
            if j >= 2:
                prob += (j/total) * ((j-1)/(total-1)) * (i/(total-2)) * p[i-1][j-2]
            p[i][j] = prob
    return p[w][b]

def compute_die_probability(x, y):
    need = 7 - max(x, y)
    if need <= 0:
        return 0, 1
    return simplify_fraction(need, 6)

def select_best_improvements(k, m, a, improvements):
    # improvements: list of (t, i, b, idx)
    by_skill = [ {1:[], 2:[], 3:[]} for _ in range(k) ]
    for t, i, b, idx in improvements:
        by_skill[i-1][t].append((b, idx))
    ops = []
    for skill_idx in range(k):
        ai = a[skill_idx]
        assign = by_skill[skill_idx][1]
        add = by_skill[skill_idx][2]
        mul = by_skill[skill_idx][3]
        add.sort(reverse=True)
        if assign and assign[0][0] > ai:
            delta, idx = assign[0]
            add.append((delta - ai, idx))
        add.sort(reverse=True)
        s = ai
        for delta, idx in add:
            ops.append(((s + delta) / s, idx))
            s += delta
        for factor, idx in mul:
            ops.append((factor, idx))
    ops.sort(key=lambda x: x[0], reverse=True)
    top = ops[:m]
    return [idx for _, idx in top]


# ########################################
#
#  PROGRAM REFACTORINGS
#
# ########################################

# ########## PROGRAM: node_11:cc_python_11 ##########

from codebank import *

def main():
    k, n, m = read_ints()
    a = read_ints()
    improvements = []
    for idx in range(1, n+1):
        t, i, b = read_ints()
        improvements.append((t, i, b, idx))
    res = select_best_improvements(k, m, a, improvements)
    print(len(res))
    if res:
        print(*res)

if __name__ == "__main__":
    main()

# ########## PROGRAM: node_12:cc_python_12 ##########

from codebank import *

def main():
    w, b = read_ints()
    prob = compute_princess_win(w, b)
    print_float(prob, 9)

if __name__ == "__main__":
    main()

# ########## PROGRAM: node_2:cc_python_2 ##########

from codebank import *

def main():
    x, y = read_ints()
    n, d = compute_die_probability(x, y)
    print(f"{n}/{d}")

if __name__ == "__main__":
    main()
