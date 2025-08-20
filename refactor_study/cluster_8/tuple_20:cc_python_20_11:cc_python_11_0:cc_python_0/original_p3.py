# Query for: node_20:cc_python_20
# =========================
"""
There is a grid with n rows and m columns. Every cell of the grid should be colored either blue or yellow.

A coloring of the grid is called stupid if every row has exactly one segment of blue cells and every column has exactly one segment of yellow cells.

In other words, every row must have at least one blue cell, and all blue cells in a row must be consecutive. Similarly, every column must have at least one yellow cell, and all yellow cells in a column must be consecutive.

<image> An example of a stupid coloring.  <image> Examples of clever colorings. The first coloring is missing a blue cell in the second row, and the second coloring has two yellow segments in the second column. 

How many stupid colorings of the grid are there? Two colorings are considered different if there is some cell that is colored differently.

Input

The only line contains two integers n, m (1≤ n, m≤ 2021).

Output

Output a single integer — the number of stupid colorings modulo 998244353.

Examples

Input


2 2


Output


2


Input


4 3


Output


294


Input


2020 2021


Output


50657649

Note

In the first test case, these are the only two stupid 2× 2 colorings.

<image>
"""

# Original Problem: node_20:cc_python_20
# =========================
M=998244353;N=4042
try:
    import __pypy__
    int_add=__pypy__.intop.int_add
    int_sub=__pypy__.intop.int_sub
    int_mul=__pypy__.intop.int_mul
    def make_mod_mul(mod=M):
        fmod_inv=1.0/mod
        def mod_mul(a,b,c=0):
            res=int_sub(
                int_add(int_mul(a,b),c),
                int_mul(mod,int(fmod_inv*a*b+fmod_inv*c)),
            )
            if res>=mod:return res-mod
            elif res<0:return res+mod
            else:return res
        return mod_mul
    mod_mul=make_mod_mul()
except:
    def mod_mul(a,b):return(a*b)%M
def mod_add(a,b):
    v=a+b
    if v>=M:v-=M
    if v<0:v+=M
    return v
def mod_sum(a):
    v=0
    for i in a:v=mod_add(v,i)
    return v
f1=[1]
for i in range(N):f1.append(mod_mul(f1[-1],i+1))
f2=[pow(f1[-1],M-2,M)]
for i in range(N):f2.append(mod_mul(f2[-1],N-i))
f2=f2[::-1]
C=lambda a,b:mod_mul(mod_mul(f1[a],f2[b]),f2[a-b])
A=lambda a,b,w:mod_mul(C(a+b,a),C(w+b-a-2,b-1))
def V(h,W,H):
    s=p=0
    for i in range(W-1):
        p=mod_add(p,A(i,H-h,W));s=mod_add(s,mod_mul(p,A(W-2-i,h,W)))
    return s
H,W=map(int,input().split())
Y=mod_sum(mod_mul(A(s,h,W),A(W-2-s,H-h,W))for s in range(W-1)for h in range(1,H))
X=mod_add(mod_sum(V(h,W,H)for h in range(1,H)),mod_sum(V(w,H,W)for w in range(1,W)))
print((X+X-Y-Y)%M)


# End of all problems.