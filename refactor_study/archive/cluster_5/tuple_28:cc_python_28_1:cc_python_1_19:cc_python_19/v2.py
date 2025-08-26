# ########## LIBRARY HELPERS ##########

# ==== RETRIEVED HELPER FUNCTIONS ====

# Selected Helper Functions

def read_str():
    """Read a full line string from input."""
    return input().strip()
# Selected because: the solution needs to read the input string s efficiently.


# Selected Helper Functions

def read_int():
    """Reads a single integer from input."""
    return int(input())

# ==== NEW HELPER FUNCTIONS ====
def truncate_str(s, max_len=10):
    """Truncates s to first 5+'...'+last 2 if len(s)>max_len."""
    return s if len(s)<=max_len else s[:5]+'...'+s[-2:]


# ########################################
#
#  PROGRAM REFACTORINGS
#
# ########################################

# ########## PROGRAM: node_19:cc_python_19 ##########

from codebank import *

def main():
    MOD = 10**9+7
    s = read_str()
    count_a = 0
    result = 0
    for ch in s:
        if ch == 'a':
            count_a = (count_a*2 + 1) % MOD
        else:
            result = (result + count_a) % MOD
    print(result)

if __name__ == "__main__":
    main()

# ########## PROGRAM: node_1:cc_python_1 ##########

from codebank import *

def cnt(s, ALPH):
    runs = {ch:0 for ch in ALPH}
    i, n = 0, len(s)
    while i < n:
        j = i+1
        while j < n and s[j] == s[i]:
            j += 1
        runs[s[i]] = max(runs[s[i]], j-i)
        i = j
    return runs

def nxt(c, t, ALPH, MAX):
    nc = cnt(t, ALPH)
    # carry over chars present before but not in t
    for ch in ALPH:
        if c[ch] and not nc[ch]:
            nc[ch] = 1
    # prefix and suffix runs
    f = 0
    while f < len(t) and t[f] == t[0]:
        f += 1
    r = 0
    while r < len(t) and t[-1-r] == t[-1]:
        r += 1
    if t[0] == t[-1]:
        if f == len(t):
            nc[t[0]] = max(nc[t[0]], c[t[0]] + (c[t[0]]+1)*len(t))
        elif c[t[0]]:
            nc[t[0]] = max(nc[t[0]], f + 1 + r)
    else:
        nc[t[0]] = max(nc[t[0]], f + (1 if c[t[0]] else 0))
        nc[t[-1]] = max(nc[t[-1]], r + (1 if c[t[-1]] else 0))
    return {ch: min(MAX, nc[ch]) for ch in ALPH}

def main():
    n = read_int()
    ALPH = 'abcdefghijklmnopqrstuvwxyz'
    MAX = 10**9
    c = cnt(read_str(), ALPH)
    for _ in range(n-1):
        c = nxt(c, read_str(), ALPH, MAX)
    print(max(c.values()))

if __name__ == "__main__":
    main()

# ########## PROGRAM: node_28:cc_python_28 ##########

from codebank import *

def main():
    s = read_str()
    n = len(s)
    if n == 1:
        print(1, s)
        return
    X, Y = [], []
    # base cases for last two suffixes
    X.append(s[-1]); Y.append(1)
    if s[-2] != s[-1]:
        X.append(s[-2]+s[-1]); Y.append(2)
    else:
        X.append(''); Y.append(0)
    # DP from i=n-3 down to 0
    for i in range(n-3, -1, -1):
        c = s[i]
        k1 = c + X[-1]
        ng = Y[-1] + 1
        k1 = truncate_str(k1)
        if c == s[i+1] and k1 > X[-2]:
            k1, ng = X[-2], Y[-2]
        X.append(k1); Y.append(ng)
    # output for each suffix
    for i in range(n-1, -1, -1):
        print(Y[i], X[i])

if __name__ == "__main__":
    main()
