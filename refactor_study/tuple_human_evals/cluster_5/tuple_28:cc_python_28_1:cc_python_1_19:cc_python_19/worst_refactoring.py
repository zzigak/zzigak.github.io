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

def format_answer(s):
    """Format string: if longer than 10, compress to first5 + '...' + last2."""
    return s if len(s) <= 10 else s[:5] + '...' + s[-2:]

def dp_compute_suffixes(s):
    """
    For each suffix s[i:], compute the lexicographically smallest string
    obtainable by removing non-overlapping equal adjacent pairs.
    Returns two lists: lengths and the (possibly formatted) strings.
    """
    n = len(s)
    best_str = [''] * n
    best_len = [0] * n
    # base cases
    best_str[n-1] = s[-1]
    best_len[n-1] = 1
    if n >= 2:
        if s[-2] != s[-1]:
            best_str[n-2] = s[-2] + s[-1]
            best_len[n-2] = 2
        else:
            best_str[n-2] = ''
            best_len[n-2] = 0
    # dp from right to left
    for i in range(n-3, -1, -1):
        c = s[i]
        # option 1: keep c
        s1 = c + best_str[i+1]
        l1 = best_len[i+1] + 1
        if l1 > 10:
            s1 = format_answer(s1)
        # option 2: remove pair if possible
        if c == s[i+1]:
            s2 = best_str[i+2]
            l2 = best_len[i+2]
        else:
            s2, l2 = s1, l1
        # choose lexicographically smaller
        if c == s[i+1] and s2 < s1:
            best_str[i], best_len[i] = s2, l2
        else:
            best_str[i], best_len[i] = s1, l1
    return best_len, best_str

def count_max_runs(s):
    """Return a dict mapping each lowercase letter to its max consecutive run in s."""
    counts = {ch: 0 for ch in 'abcdefghijklmnopqrstuvwxyz'}
    i, n = 0, len(s)
    while i < n:
        j = i + 1
        while j < n and s[j] == s[i]:
            j += 1
        counts[s[i]] = max(counts[s[i]], j - i)
        i = j
    return counts

def update_counts(prev_counts, t, MAX):
    """
    Given prev_counts (max runs before) and string t to multiply,
    compute the new max runs dictionary, capping at MAX.
    """
    counts = count_max_runs(t)
    # propagate presence of previous letters
    for ch, v in prev_counts.items():
        if v > 0 and counts.get(ch, 0) == 0:
            counts[ch] = 1
    # prefix run f and suffix run r in t
    f = 0
    while f < len(t) and t[f] == t[0]:
        f += 1
    r = 0
    while r < len(t) and t[-1 - r] == t[-1]:
        r += 1
    if t[0] == t[-1]:
        ch = t[0]
        if f == len(t):
            counts[ch] = max(counts[ch],
                              prev_counts[ch] + (prev_counts[ch] + 1) * len(t))
        elif prev_counts[ch] > 0:
            counts[ch] = max(counts[ch], f + 1 + r)
    else:
        if prev_counts[t[0]] > 0:
            counts[t[0]] = max(counts[t[0]], f + 1)
        if prev_counts[t[-1]] > 0:
            counts[t[-1]] = max(counts[t[-1]], r + 1)
    # cap at MAX
    for ch in counts:
        if counts[ch] > MAX:
            counts[ch] = MAX
    return counts

def count_steps_ab_to_bba(s, mod):
    """
    Count the minimum number of steps to eliminate all "ab" by replacing
    each occurrence with "bba", modulo mod.
    """
    res = 0
    a_count = 0
    for ch in s:
        if ch == 'a':
            a_count = (a_count * 2 + 1) % mod
        elif ch == 'b':
            res = (res + a_count) % mod
    return res


# ########################################
#
#  PROGRAM REFACTORINGS
#
# ########################################

# ########## PROGRAM: node_19:cc_python_19 ##########

from codebank import *

def main():
    s = read_str()
    MOD = 10**9 + 7
    print(count_steps_ab_to_bba(s, MOD))

if __name__ == "__main__":
    main()

# ########## PROGRAM: node_1:cc_python_1 ##########

from codebank import *

def main():
    n = read_int()
    MAX = 10 ** 9
    c = count_max_runs(read_str())
    for _ in range(n - 1):
        c = update_counts(c, read_str(), MAX)
    print(max(c.values()))

if __name__ == "__main__":
    main()

# ########## PROGRAM: node_28:cc_python_28 ##########

from codebank import *

def main():
    s = read_str()
    lengths, strs = dp_compute_suffixes(s)
    for l, st in zip(lengths, strs):
        print(l, st)

if __name__ == "__main__":
    main()
