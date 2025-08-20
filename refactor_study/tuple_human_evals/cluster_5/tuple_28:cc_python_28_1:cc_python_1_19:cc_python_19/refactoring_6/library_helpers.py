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
    """Read a full line string from input."""
    return input().strip()

def read_int():
    """Reads a single integer from input."""
    return int(input())

def truncate_str(s, max_len=10):
    """If s longer than max_len, return s[:5]+'...'+s[-2:], else s."""
    return s if len(s) <= max_len else s[:5] + "..." + s[-2:]

def get_run_max(s):
    """Return dict mapping chars to their max consecutive run in s."""
    d = {}
    i = 0
    n = len(s)
    while i < n:
        j = i + 1
        while j < n and s[j] == s[i]:
            j += 1
        d[s[i]] = max(d.get(s[i], 0), j - i)
        i = j
    return d

def merge_counts(prev, t, max_cap):
    """
    Merge run-max counts prev with string t under cap max_cap,
    following the custom string 'multiplication' beauty update.
    """
    curr = get_run_max(t)
    # any char in prev but not in t gets at least 1
    for ch, cnt in prev.items():
        if cnt > 0 and ch not in curr:
            curr[ch] = 1
    # prefix run length of t[0], suffix run of t[-1]
    f = 0
    while f < len(t) and t[f] == t[0]:
        f += 1
    r = 0
    while r < len(t) and t[-1 - r] == t[-1]:
        r += 1
    first, last = t[0], t[-1]
    if first == last:
        if f == len(t):
            # all same char
            extended = prev.get(first, 0) + (prev.get(first, 0) + 1) * len(t)
            curr[first] = min(max(curr.get(first, 0), extended), max_cap)
        elif prev.get(first, 0) > 0:
            # join prefix and suffix across prev
            curr[first] = max(curr.get(first, 0), f + 1 + r)
    else:
        if prev.get(first, 0) > 0:
            curr[first] = max(curr.get(first, 0), f + 1)
        curr[last] = max(curr.get(last, 0), r + (1 if prev.get(last, 0) > 0 else 0))
    # cap all
    for ch in curr:
        curr[ch] = min(curr[ch], max_cap)
    return curr
