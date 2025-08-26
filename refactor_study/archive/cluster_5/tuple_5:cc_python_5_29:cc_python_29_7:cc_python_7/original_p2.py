# Query for: node_5:cc_python_5
# =========================
"""
The Romans have attacked again. This time they are much more than the Persians but Shapur is ready to defeat them. He says: "A lion is never afraid of a hundred sheep". 

Nevertheless Shapur has to find weaknesses in the Roman army to defeat them. So he gives the army a weakness number.

In Shapur's opinion the weakness of an army is equal to the number of triplets i, j, k such that i < j < k and ai > aj > ak where ax is the power of man standing at position x. The Roman army has one special trait — powers of all the people in it are distinct.

Help Shapur find out how weak the Romans are.

Input

The first line of input contains a single number n (3 ≤ n ≤ 106) — the number of men in Roman army. Next line contains n different positive integers ai (1 ≤ i ≤ n, 1 ≤ ai ≤ 109) — powers of men in the Roman army. 

Output

A single integer number, the weakness of the Roman army. 

Please, do not use %lld specificator to read or write 64-bit integers in C++. It is preffered to use cout (also you may use %I64d).

Examples

Input

3
3 2 1


Output

1


Input

3
2 3 1


Output

0


Input

4
10 8 3 1


Output

4


Input

4
1 5 4 3


Output

1
"""

# Original Problem: node_5:cc_python_5
# =========================
from sys import stdin


class order_tree:
    def __init__(self, n):
        self.tree, self.n = [[0, 0] for _ in range(n << 1)], n

    # get interval[l,r)
    def query(self, r, col):
        res = 0
        l = self.n
        r += self.n

        while l < r:
            if l & 1:
                res += self.tree[l][col]
                l += 1

            if r & 1:
                r -= 1
                res += self.tree[r][col]

            l >>= 1
            r >>= 1

        return res

    def update(self, ix, val, col):
        ix += self.n

        # set new value
        self.tree[ix][col] += val

        # move up
        while ix > 1:
            self.tree[ix >> 1][col] = self.tree[ix][col] + self.tree[ix ^ 1][col]
            ix >>= 1


def fast3():
    import os, sys, atexit
    from io import BytesIO
    sys.stdout = BytesIO()
    _write = sys.stdout.write
    sys.stdout.write = lambda s: _write(s.encode())
    atexit.register(lambda: os.write(1, sys.stdout.getvalue()))
    return BytesIO(os.read(0, os.fstat(0).st_size)).readline


input = fast3()
n, a = int(input()), [int(x) for x in input().split()]
tree, ans = order_tree(n), 0
mem = {i: j for j, i in enumerate(sorted(a))}

for i in range(n - 1, -1, -1):
    cur = mem[a[i]]
    ans += tree.query(cur, 1)
    tree.update(cur, 1, 0)
    tree.update(cur, tree.query(cur, 0), 1)

print(ans)

