# Query for: node_1:cc_python_1
# =========================
"""
Roman and Denis are on the trip to the programming competition. Since the trip was long, they soon got bored, and hence decided to came up with something. Roman invented a pizza's recipe, while Denis invented a string multiplication. According to Denis, the result of multiplication (product) of strings s of length m and t is a string t + s_1 + t + s_2 + … + t + s_m + t, where s_i denotes the i-th symbol of the string s, and "+" denotes string concatenation. For example, the product of strings "abc" and "de" is a string "deadebdecde", while the product of the strings "ab" and "z" is a string "zazbz". Note, that unlike the numbers multiplication, the product of strings s and t is not necessarily equal to product of t and s.

Roman was jealous of Denis, since he invented such a cool operation, and hence decided to invent something string-related too. Since Roman is beauty-lover, he decided to define the beauty of the string as the length of the longest substring, consisting of only one letter. For example, the beauty of the string "xayyaaabca" is equal to 3, since there is a substring "aaa", while the beauty of the string "qwerqwer" is equal to 1, since all neighboring symbols in it are different.

In order to entertain Roman, Denis wrote down n strings p_1, p_2, p_3, …, p_n on the paper and asked him to calculate the beauty of the string ( … (((p_1 ⋅ p_2) ⋅ p_3) ⋅ … ) ⋅ p_n, where s ⋅ t denotes a multiplication of strings s and t. Roman hasn't fully realized how Denis's multiplication works, so he asked you for a help. Denis knows, that Roman is very impressionable, he guarantees, that the beauty of the resulting string is at most 10^9.

Input

The first line contains a single integer n (2 ≤ n ≤ 100 000) — the number of strings, wroted by Denis.

Next n lines contain non-empty strings p_1, p_2, …, p_n, consisting of lowercase english letters.

It's guaranteed, that the total length of the strings p_i is at most 100 000, and that's the beauty of the resulting product is at most 10^9.

Output

Print exactly one integer — the beauty of the product of the strings.

Examples

Input


3
a
b
a


Output


3


Input


2
bnn
a


Output


1

Note

In the first example, the product of strings is equal to "abaaaba".

In the second example, the product of strings is equal to "abanana".
"""

# Original Problem: node_1:cc_python_1
# =========================
ALPH = 'abcdefghijklmnopqrstuvwxyz'
MAX = 10 ** 9

def cnt(s):
    c = {ch : 0 for ch in ALPH}
    i = 0
    while i < len(s):
        j = i + 1
        while j < len(s) and s[i] == s[j]:
            j += 1
        c[s[i]] = max(c[s[i]], j - i)
        i = j
    return c

def nxt(c, t):
    nc = cnt(t)
    for ch in ALPH:
        if c[ch] and not nc[ch]:
            nc[ch] = 1
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
        nc[t[0]] = max(nc[t[0]], f + (c[t[0]] > 0))
        nc[t[-1]] = max(nc[t[-1]], r + (c[t[-1]] > 0))
    return {x : min(MAX, y) for x, y in nc.items()}

n = int(input())
c = cnt(input())
for i in range(n - 1):
    c = nxt(c, input())
print(max(c.values()))

