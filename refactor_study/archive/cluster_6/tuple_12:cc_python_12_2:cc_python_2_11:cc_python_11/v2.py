# ########## LIBRARY HELPERS ##########

# ==== RETRIEVED HELPER FUNCTIONS (NONE) ====

# ==== NEW HELPER FUNCTIONS ====
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def simplify_fraction(n, d):
    g = gcd(n, d)
    return n//g, d//g

def create_2d_list(rows, cols, value=0):
    return [[value]*cols for _ in range(rows)]

def get_princess_win_prob(w, b):
    dp = create_2d_list(w+1, b+1, 0.0)
    for i in range(1, w+1):
        dp[i][0] = 1.0
    for i in range(1, w+1):
        for j in range(1, b+1):
            total = i + j
            res = i/total
            if j >= 3:
                res += (j/total)*((j-1)/(total-1))*((j-2)/(total-2))*dp[i][j-3]
            if j >= 2:
                res += (j/total)*((j-1)/(total-1))*(i/(total-2))*dp[i-1][j-2]
            dp[i][j] = res
    return dp[w][b]

def get_top_n(items, n, key=lambda x: x):
    import heapq
    return heapq.nlargest(n, items, key=key)


# ########################################
#
#  PROGRAM REFACTORINGS
#
# ########################################

# ########## PROGRAM: node_11:cc_python_11 ##########

from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    k, n, m = map(int, input().split())
    a = list(map(int, input().split()))
    l = [[[] for _ in range(3)] for _ in range(k)]
    for idx in range(1, n+1):
        t, i, b = map(int, input().split())
        l[i-1][t-1].append((b, idx))
    for i in range(k):
        for j in range(3):
            l[i][j].sort(reverse=True)
    ops = []
    for i in range(k):
        adds = l[i][1][:]
        if l[i][0] and l[i][0][0][0] > a[i]:
            adds.append((l[i][0][0][0] - a[i], l[i][0][0][1]))
            adds.sort(reverse=True)
        s = a[i]
        for add, idx in adds:
            ops.append(((s+add)/s, idx))
            s += add
        for mul, idx in l[i][2]:
            ops.append((mul, idx))
    top_ops = get_top_n(ops, m, key=lambda x: x[0])
    st = {idx for _, idx in top_ops}
    res = []
    for i in range(k):
        for j in range(3):
            for _, idx in l[i][j]:
                if idx in st:
                    res.append(idx)
    print(len(res))
    if res:
        print(*res)

if __name__ == "__main__":
    main()

# ########## PROGRAM: node_12:cc_python_12 ##########

from codebank import *

def main():
    w, b = map(int, input().split())
    prob = get_princess_win_prob(w, b)
    print(f"{prob:.9f}")

if __name__ == "__main__":
    main()

# ########## PROGRAM: node_2:cc_python_2 ##########

from codebank import *

def main():
    x, y = map(int, input().split())
    z = 7 - max(x, y)
    num, den = simplify_fraction(z, 6)
    print(f"{num}/{den}")

if __name__ == "__main__":
    main()
