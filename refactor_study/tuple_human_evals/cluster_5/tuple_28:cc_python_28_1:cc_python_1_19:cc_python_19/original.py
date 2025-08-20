# This file contains original problem queries and their corresponding Python code.

# Query for: node_19:cc_python_19
# =========================
"""
We have a string of letters 'a' and 'b'. We want to perform some operations on it. On each step we choose one of substrings "ab" in the string and replace it with the string "bba". If we have no "ab" as a substring, our job is done. Print the minimum number of steps we should perform to make our job done modulo 109 + 7.

The string "ab" appears as a substring if there is a letter 'b' right after the letter 'a' somewhere in the string.

Input

The first line contains the initial string consisting of letters 'a' and 'b' only with length from 1 to 106.

Output

Print the minimum number of steps modulo 109 + 7.

Examples

Input

ab


Output

1


Input

aab


Output

3

Note

The first example: "ab"  →  "bba".

The second example: "aab"  →  "abba"  →  "bbaba"  →  "bbbbaa".
"""

# Original Problem: node_19:cc_python_19
# =========================
def mess():
    String=input()
    count_it=0
    Counter=0

    for i in String:
        if i=='a':
            count_it = (count_it * 2) % Modulo
            count_it+=1

        elif i=='b':
            Counter+=count_it
            #count_it =(count_it* 2)%Modulo
    return Counter

if __name__ == "__main__":
    Modulo = 1000000007
    print(mess()%Modulo)


# EoP (End of Problem details for node_19:cc_python_19)
# ######################################################################

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


# EoP (End of Problem details for node_1:cc_python_1)
# ######################################################################

# Query for: node_28:cc_python_28
# =========================
"""
Some time ago Lesha found an entertaining string s consisting of lowercase English letters. Lesha immediately developed an unique algorithm for this string and shared it with you. The algorithm is as follows.

Lesha chooses an arbitrary (possibly zero) number of pairs on positions (i, i + 1) in such a way that the following conditions are satisfied: 

  * for each pair (i, i + 1) the inequality 0 ≤ i < |s| - 1 holds; 
  * for each pair (i, i + 1) the equality s_i = s_{i + 1} holds; 
  * there is no index that is contained in more than one pair. 

After that Lesha removes all characters on indexes contained in these pairs and the algorithm is over. 

Lesha is interested in the lexicographically smallest strings he can obtain by applying the algorithm to the suffixes of the given string.

Input

The only line contains the string s (1 ≤ |s| ≤ 10^5) — the initial string consisting of lowercase English letters only.

Output

In |s| lines print the lengths of the answers and the answers themselves, starting with the answer for the longest suffix. The output can be large, so, when some answer is longer than 10 characters, instead print the first 5 characters, then "...", then the last 2 characters of the answer.

Examples

Input


abcdd


Output


3 abc
2 bc
1 c
0 
1 d


Input


abbcdddeaaffdfouurtytwoo


Output


18 abbcd...tw
17 bbcdd...tw
16 bcddd...tw
15 cddde...tw
14 dddea...tw
13 ddeaa...tw
12 deaad...tw
11 eaadf...tw
10 aadfortytw
9 adfortytw
8 dfortytw
9 fdfortytw
8 dfortytw
7 fortytw
6 ortytw
5 rtytw
6 urtytw
5 rtytw
4 tytw
3 ytw
2 tw
1 w
0 
1 o

Note

Consider the first example.

  * The longest suffix is the whole string "abcdd". Choosing one pair (4, 5), Lesha obtains "abc". 
  * The next longest suffix is "bcdd". Choosing one pair (3, 4), we obtain "bc". 
  * The next longest suffix is "cdd". Choosing one pair (2, 3), we obtain "c". 
  * The next longest suffix is "dd". Choosing one pair (1, 2), we obtain "" (an empty string). 
  * The last suffix is the string "d". No pair can be chosen, so the answer is "d". 



In the second example, for the longest suffix "abbcdddeaaffdfouurtytwoo" choose three pairs (11, 12), (16, 17), (23, 24) and we obtain "abbcdddeaadfortytw"
"""

# Original Problem: node_28:cc_python_28
# =========================
import sys
s = input().strip()
N = len(s)
if len(s) == 1:
    print(1, s[0])
    sys.exit()
X = [s[-1], s[-2]+s[-1] if s[-2]!=s[-1] else ""]
Y = [1, 2 if s[-2]!=s[-1] else 0]
for i in range(N-3, -1, -1):
    c = s[i]
    k1 = c+X[-1]
    ng = Y[-1]+1
    if ng > 10:
        k1 = k1[:5] + "..." + k1[-2:]
    if c == s[i+1] and k1 > X[-2]:
        k1 = X[-2]
        ng = Y[-2]
    X.append(k1)
    Y.append(ng)
for i in range(N-1, -1, -1):
    print(Y[i], X[i])


# End of all problems.
