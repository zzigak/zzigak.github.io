# This file contains original problem queries and their corresponding Python code.

# Query for: node_3:cc_python_3
# =========================
"""
Peter had a cube with non-zero length of a side. He put the cube into three-dimensional space in such a way that its vertices lay at integer points (it is possible that the cube's sides are not parallel to the coordinate axes). Then he took a piece of paper and wrote down eight lines, each containing three integers — coordinates of cube's vertex (a single line contains coordinates of a single vertex, each vertex is written exactly once), put the paper on the table and left. While Peter was away, his little brother Nick decided to play with the numbers on the paper. In one operation Nick could swap some numbers inside a single line (Nick didn't swap numbers from distinct lines). Nick could have performed any number of such operations.

When Peter returned and found out about Nick's mischief, he started recollecting the original coordinates. Help Peter restore the original position of the points or else state that this is impossible and the numbers were initially recorded incorrectly.

Input

Each of the eight lines contains three space-separated integers — the numbers written on the piece of paper after Nick's mischief. All numbers do not exceed 106 in their absolute value.

Output

If there is a way to restore the cube, then print in the first line "YES". In each of the next eight lines print three integers — the restored coordinates of the points. The numbers in the i-th output line must be a permutation of the numbers in i-th input line. The numbers should represent the vertices of a cube with non-zero length of a side. If there are multiple possible ways, print any of them.

If there is no valid way, print "NO" (without the quotes) in the first line. Do not print anything else.

Examples

Input

0 0 0
0 0 1
0 0 1
0 0 1
0 1 1
0 1 1
0 1 1
1 1 1


Output

YES
0 0 0
0 0 1
0 1 0
1 0 0
0 1 1
1 0 1
1 1 0
1 1 1


Input

0 0 0
0 0 0
0 0 0
0 0 0
1 1 1
1 1 1
1 1 1
1 1 1


Output

NO
"""

# Original Problem: node_3:cc_python_3
# =========================
from itertools import permutations as p

d = lambda a, b: sum((i - j) ** 2 for i, j in zip(a, b))
f = lambda a, b: [i + j - k for i, j, k in zip(a, b, q)]
g = lambda t: sorted(sorted(q) for q in t)

v = [sorted(map(int, input().split())) for i in range(8)]
q = v.pop()

u = g(v)
for a, b, c in p(v, 3):
    for x in p(a):
        s = 2 * d(q, x)
        if not s: continue
        for y in p(b):
            if not 2 * d(q, y) == d(x, y) == s: continue
            for z in p(c):
                if not 2 * d(q, z) == d(x, z) == d(y, z) == s: continue
                t = [x, y, z] + [f(x, y), f(x, z), f(y, z), f(f(x, y), z)]
                if g(t) == u:
                    print('YES')
                    d = [str(sorted(i)) for i in t]
                    for j in v:
                        i = d.index(str(j))
                        k = t.pop(i)
                        print(*k)
                        d.pop(i)
                    print(*q)
                    exit()

print('NO')


# EoP (End of Problem details for node_3:cc_python_3)
# ######################################################################

# Query for: node_8:cc_python_8
# =========================
"""
Cat Noku has obtained a map of the night sky. On this map, he found a constellation with n stars numbered from 1 to n. For each i, the i-th star is located at coordinates (xi, yi). No two stars are located at the same position.

In the evening Noku is going to take a look at the night sky. He would like to find three distinct stars and form a triangle. The triangle must have positive area. In addition, all other stars must lie strictly outside of this triangle. He is having trouble finding the answer and would like your help. Your job is to find the indices of three stars that would form a triangle that satisfies all the conditions. 

It is guaranteed that there is no line such that all stars lie on that line. It can be proven that if the previous condition is satisfied, there exists a solution to this problem.

Input

The first line of the input contains a single integer n (3 ≤ n ≤ 100 000).

Each of the next n lines contains two integers xi and yi ( - 109 ≤ xi, yi ≤ 109).

It is guaranteed that no two stars lie at the same point, and there does not exist a line such that all stars lie on that line.

Output

Print three distinct integers on a single line — the indices of the three points that form a triangle that satisfies the conditions stated in the problem.

If there are multiple possible answers, you may print any of them.

Examples

Input

3
0 1
1 0
1 1


Output

1 2 3


Input

5
0 0
0 2
2 0
2 2
1 1


Output

1 3 5

Note

In the first sample, we can print the three indices in any order.

In the second sample, we have the following picture. 

<image>

Note that the triangle formed by starts 1, 4 and 3 doesn't satisfy the conditions stated in the problem, as point 5 is not strictly outside of this triangle (it lies on it's border).
"""

# Original Problem: node_8:cc_python_8
# =========================
f = lambda: list(map(int, input().split()))
d = lambda x, y: (x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2
r = lambda x, y, z: (x[0] - y[0]) * (x[1] - z[1]) == (x[1] - y[1]) * (x[0] - z[0])

n = int(input())
t = [f() for i in range(n)]

j = k = -1
b = c = 0

x = t.pop()
for i in range(n - 1):
    a = d(x, t[i])
    if j < 0 or a < b: j, b = i, a

y = t.pop(j)
for i in range(n - 2):
    if r(x, y, t[i]): continue
    a = d(x, t[i])
    if k < 0 or a < c: k, c = i, a

print(n, j + 1, k + 2 - (j > k))


# EoP (End of Problem details for node_8:cc_python_8)
# ######################################################################

# Query for: node_9:cc_python_9
# =========================
"""
You are given set of n points in 5-dimensional space. The points are labeled from 1 to n. No two points coincide.

We will call point a bad if there are different points b and c, not equal to a, from the given set such that angle between vectors <image> and <image> is acute (i.e. strictly less than <image>). Otherwise, the point is called good.

The angle between vectors <image> and <image> in 5-dimensional space is defined as <image>, where <image> is the scalar product and <image> is length of <image>.

Given the list of points, print the indices of the good points in ascending order.

Input

The first line of input contains a single integer n (1 ≤ n ≤ 103) — the number of points.

The next n lines of input contain five integers ai, bi, ci, di, ei (|ai|, |bi|, |ci|, |di|, |ei| ≤ 103) — the coordinates of the i-th point. All points are distinct.

Output

First, print a single integer k — the number of good points.

Then, print k integers, each on their own line — the indices of the good points in ascending order.

Examples

Input

6
0 0 0 0 0
1 0 0 0 0
0 1 0 0 0
0 0 1 0 0
0 0 0 1 0
0 0 0 0 1


Output

1
1


Input

3
0 0 1 2 0
0 0 9 2 0
0 0 5 9 0


Output

0

Note

In the first sample, the first point forms exactly a <image> angle with all other pairs of points, so it is good.

In the second sample, along the cd plane, we can see the points look as follows:

<image>

We can see that all angles here are acute, so no points are good.
"""

# Original Problem: node_9:cc_python_9
# =========================
n=int(input())
A=[]
js=0
B=[]
for i in range(n):
    A.append(list(map(int,input().split())))

def product(a,b,c):
    pr=0
    for m in range(5):
        pr=pr+(A[b][m]-A[a][m])*(A[c][m]-A[a][m])
    return (pr)

if(n>11):
    print(0)
else:
    for j in range(n):
        k=0
        l=0
        flag=0
        while(k<n):
            l=k+1
            while(l<n):
                pro=product(j,k,l)
                if(l!=j and k!=j and pro>0):
                    flag=1
                    break
                else:
                    l=l+1
            if(flag==1):
                break
            else:
                k=k+1
        if(k==n):
            js=js+1
            B.append(j+1)
    print(js)
    for f in range(js):
        print(B[f])


# End of all problems.
