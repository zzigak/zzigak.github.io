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