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

def read_str():
    """Reads a single string (line) from input."""
    return input().strip()


# Selected Helper Functions

def read_str():
    """Read a line as a stripped string from standard input."""
    return input().strip()
# Selected because: We need to read the input string for the single‐pass DP routine.


# ==== NEW HELPER FUNCTIONS ====
def read_str():
    return input().strip()

def read_int():
    return int(read_str())

def trunc(s):
    return s if len(s) <= 10 else s[:5] + '...' + s[-2:]

def cnt(s):
    c = {}
    i = 0
    while i < len(s):
        j = i + 1
        while j < len(s) and s[j] == s[i]:
            j += 1
        c[s[i]] = max(c.get(s[i], 0), j - i)
        i = j
    return c

def nxt(c, t):
    MAX = 10**9
    nc = cnt(t)
    # carry over letters present before but not in t
    for ch, val in c.items():
        if val > 0 and ch not in nc:
            nc[ch] = 1
    # count prefix run
    f = 0
    while f < len(t) and t[f] == t[0]:
        f += 1
    # count suffix run
    r = 0
    while r < len(t) and t[-1 - r] == t[-1]:
        r += 1
    ch0, ch1 = t[0], t[-1]
    prev0 = c.get(ch0, 0)
    prev1 = c.get(ch1, 0)
    if ch0 == ch1:
        if f == len(t):
            nc[ch0] = min(MAX, max(nc.get(ch0, 0), prev0 + (prev0 + 1) * len(t)))
        elif prev0 > 0:
            nc[ch0] = min(MAX, max(nc.get(ch0, 0), f + 1 + r))
    else:
        # extend prefix char
        if prev0 > 0:
            nc[ch0] = min(MAX, max(nc.get(ch0, 0), f + 1))
        else:
            nc[ch0] = min(MAX, max(nc.get(ch0, 0), f))
        # extend suffix char
        if prev1 > 0:
            nc[ch1] = min(MAX, max(nc.get(ch1, 0), r + 1))
        else:
            nc[ch1] = min(MAX, max(nc.get(ch1, 0), r))
    return nc

def compute_ab_steps(s, mod):
    cnt_it = 0
    res = 0
    for ch in s:
        if ch == 'a':
            cnt_it = (cnt_it * 2 + 1) % mod
        elif ch == 'b':
            res = (res + cnt_it) % mod
    return res
