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