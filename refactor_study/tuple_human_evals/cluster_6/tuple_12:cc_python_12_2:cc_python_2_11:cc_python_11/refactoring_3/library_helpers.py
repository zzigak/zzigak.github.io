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
