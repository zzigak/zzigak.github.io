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
    """Reads a single line string from input."""
    return input().strip()

def read_int():
    """Reads a single integer from input."""
    return int(input())

def trim_str(s, max_len=10):
    """Trim s to first 5 + "..." + last 2 if it exceeds max_len."""
    if len(s) <= max_len:
        return s
    return s[:5] + "..." + s[-2:]

def cnt(s):
    """Count max consecutive runs for each char in s."""
    c = {}
    i, n = 0, len(s)
    while i < n:
        j = i + 1
        while j < n and s[j] == s[i]:
            j += 1
        c[s[i]] = max(c.get(s[i], 0), j - i)
        i = j
    return c

def nxt(c, t, alph, max_val):
    """Merge run counts c with string t according to string‐multiplication rules."""
    nc = cnt(t)
    for ch in alph:
        if c.get(ch, 0) and not nc.get(ch, 0):
            nc[ch] = 1
    n = len(t)
    f = 0
    while f < n and t[f] == t[0]:
        f += 1
    r = 0
    while r < n and t[-1 - r] == t[-1]:
        r += 1
    if t[0] == t[-1]:
        if f == n:
            v = c.get(t[0], 0)
            nc[t[0]] = min(max_val, max(nc.get(t[0], 0), v + (v + 1) * n))
        elif c.get(t[0], 0):
            nc[t[0]] = max(nc.get(t[0], 0), f + 1 + r)
    else:
        nc[t[0]] = max(nc.get(t[0], 0), f + (1 if c.get(t[0], 0) > 0 else 0))
        nc[t[-1]] = max(nc.get(t[-1], 0), r + (1 if c.get(t[-1], 0) > 0 else 0))
    return {ch: min(max_val, v) for ch, v in nc.items()}

def process_char(ch, cnt_a, res, mod):
    """Update counters for 'a'/'b' replacement process."""
    if ch == 'a':
        cnt_a = (cnt_a * 2 + 1) % mod
    elif ch == 'b':
        res = (res + cnt_a) % mod
    return cnt_a, res
