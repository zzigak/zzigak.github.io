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
    """Reads a stripped line from input."""
    return input().strip()

def read_int():
    """Reads a single integer from input."""
    return int(input())

def truncate(s):
    """Truncate string s if longer than 10: first5...last2."""
    return s if len(s) <= 10 else s[:5] + '...' + s[-2:]

def cnt(s):
    """Count max runs of each lowercase letter in s."""
    ALPH = 'abcdefghijklmnopqrstuvwxyz'
    c = {ch: 0 for ch in ALPH}
    i = 0
    while i < len(s):
        j = i + 1
        while j < len(s) and s[i] == s[j]:
            j += 1
        c[s[i]] = max(c[s[i]], j - i)
        i = j
    return c

def nxt(c, t):
    """Compute new counts after multiplying current product by t."""
    ALPH = 'abcdefghijklmnopqrstuvwxyz'
    MAX = 10**9
    nc = cnt(t)
    # carry over any letter present before but absent now
    for ch in ALPH:
        if c.get(ch, 0) and not nc[ch]:
            nc[ch] = 1
    # prefix and suffix runs in t
    f = 0
    while f < len(t) and t[f] == t[0]:
        f += 1
    r = 0
    while r < len(t) and t[-1 - r] == t[-1]:
        r += 1
    if t[0] == t[-1]:
        if f == len(t):
            nc[t[0]] = max(nc[t[0]], c[t[0]] + (c[t[0]] + 1) * len(t))
        elif c[t[0]]:
            nc[t[0]] = max(nc[t[0]], f + 1 + r)
    else:
        nc[t[0]] = max(nc[t[0]], f + (1 if c[t[0]] else 0))
        nc[t[-1]] = max(nc[t[-1]], r + (1 if c[t[-1]] else 0))
    # cap by MAX
    for x, y in nc.items():
        nc[x] = min(MAX, y)
    return nc
