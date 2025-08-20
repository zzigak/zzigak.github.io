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

def truncate_string(s):
    """If string longer than 10, return first 5 + '...' + last 2, else original."""
    return s if len(s) <= 10 else s[:5] + "..." + s[-2:]

def max_run_lengths(s):
    """Return dict mapping each character in s to its maximum consecutive run length."""
    d = {}
    i, n = 0, len(s)
    while i < n:
        j = i + 1
        while j < n and s[j] == s[i]:
            j += 1
        d[s[i]] = max(d.get(s[i], 0), j - i)
        i = j
    return d

def merge_counts(prev_counts, t, alph, max_limit):
    """
    Merge prev_counts with string t according to the string‐multiplication beauty rule,
    returning a new dict of max runs per character, capped at max_limit.
    """
    # start with runs in t
    nc = max_run_lengths(t)
    # any char seen before but not in t gets run 1
    for ch in alph:
        if prev_counts.get(ch, 0) > 0 and nc.get(ch, 0) == 0:
            nc[ch] = 1
    # compute prefix and suffix runs in t
    f = 0
    while f < len(t) and t[f] == t[0]:
        f += 1
    r = 0
    while r < len(t) and t[-1 - r] == t[-1]:
        r += 1
    first, last = t[0], t[-1]
    if first == last:
        if f == len(t):
            # entire t is the same char
            prev = prev_counts.get(first, 0)
            nc[first] = max(nc.get(first, 0),
                            prev + (prev + 1) * len(t))
        elif prev_counts.get(first, 0) > 0:
            nc[first] = max(nc.get(first, 0), f + 1 + r)
    else:
        if prev_counts.get(first, 0) > 0:
            nc[first] = max(nc.get(first, 0), f + 1)
        if prev_counts.get(last, 0) > 0:
            nc[last] = max(nc.get(last, 0), r + 1)
    # cap at max_limit
    return {ch: min(run, max_limit) for ch, run in nc.items()}
