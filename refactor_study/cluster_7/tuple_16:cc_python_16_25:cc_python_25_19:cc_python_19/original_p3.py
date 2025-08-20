# Query for: node_25:cc_python_25
# =========================
"""
Given 2 integers u and v, find the shortest array such that [bitwise-xor](https://en.wikipedia.org/wiki/Bitwise_operation#XOR) of its elements is u, and the sum of its elements is v.

Input

The only line contains 2 integers u and v (0 ≤ u,v ≤ 10^{18}).

Output

If there's no array that satisfies the condition, print "-1". Otherwise:

The first line should contain one integer, n, representing the length of the desired array. The next line should contain n positive integers, the array itself. If there are multiple possible answers, print any.

Examples

Input


2 4


Output


2
3 1

Input


1 3


Output


3
1 1 1

Input


8 5


Output


-1

Input


0 0


Output


0

Note

In the first sample, 3⊕ 1 = 2 and 3 + 1 = 4. There is no valid array of smaller length.

Notice that in the fourth sample the array is empty.
"""

# Original Problem: node_25:cc_python_25
# =========================
u, v = list(map(int, input().split()))
if u > v:
    print(-1)
elif u == 0 and v == 0:
    print(0)
elif u == v:
    print(1)
    print(u)
else:
    a, b, c = u, (v - u) // 2, (v - u) // 2
    d, e = (v - u) // 2 + u, (v - u) // 2
    if d + e == v and d ^ e == u:
        print(2)
        print(d, e)
    elif a+b+c == v and a ^ b ^ c == u:
        print(3)
        print(a, b, c)
    else:
        print(-1)


# End of all problems.