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
def read_int():
    """Reads a single integer from input."""
    return int(input())

def read_str():
    """Reads a stripped line from input."""
    return input().strip()

def format_string(s: str, limit: int = 10) -> str:
    """Format string, abbreviating if longer than limit."""
    return s[:5] + "..." + s[-2:] if len(s) > limit else s

def compute_lex_min_suffix(s: str) -> list:
    """Compute for each suffix the lexicographically smallest result and its length."""
    n = len(s)
    if n == 1:
        return [(1, s)]
    X = [s[-1], s[-2] + s[-1] if s[-2] != s[-1] else ""]
    Y = [1, 2 if s[-2] != s[-1] else 0]
    for i in range(n-3, -1, -1):
        c = s[i]
        best_s = c + X[-1]
        best_l = Y[-1] + 1
        if best_l > 10:
            best_s = format_string(best_s)
        if c == s[i+1]:
            alt_s, alt_l = X[-2], Y[-2]
            if alt_s < best_s:
                best_s, best_l = alt_s, alt_l
        X.append(best_s)
        Y.append(best_l)
    res = []
    for i in range(n-1, -1, -1):
        res.append((Y[i], X[i]))
    return res

def count_max_runs(s: str) -> dict:
    """Count max consecutive runs per character in s."""
    c = {}
    i, n = 0, len(s)
    while i < n:
        j = i + 1
        while j < n and s[j] == s[i]:
            j += 1
        c[s[i]] = max(c.get(s[i], 0), j - i)
        i = j
    return c

def merge_beauty(prev: dict, t: str, max_val: int) -> dict:
    """Merge beauty counts for string multiplication with t."""
    nc = count_max_runs(t)
    # carry over chars present before but not in t
    for ch, cnt in prev.items():
        if cnt and nc.get(ch, 0) == 0:
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
            nc[t[0]] = max(nc[t[0]], prev.get(t[0], 0) + (prev.get(t[0], 0) + 1) * len(t))
        elif prev.get(t[0], 0):
            nc[t[0]] = max(nc[t[0]], f + 1 + r)
    else:
        nc[t[0]] = max(nc.get(t[0], 0), f + (1 if prev.get(t[0], 0) else 0))
        nc[t[-1]] = max(nc.get(t[-1], 0), r + (1 if prev.get(t[-1], 0) else 0))
    return {ch: min(max_val, cnt) for ch, cnt in nc.items()}

def compute_steps(s: str, mod: int) -> int:
    """Compute minimal steps to eliminate all 'ab' substrings."""
    cnt_a = 0
    ans = 0
    for ch in s:
        if ch == 'a':
            cnt_a = (cnt_a * 2 + 1) % mod
        else:  # 'b'
            ans = (ans + cnt_a) % mod
    return ans
