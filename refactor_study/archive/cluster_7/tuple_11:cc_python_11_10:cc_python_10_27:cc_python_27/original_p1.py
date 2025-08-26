# Query for: node_10:cc_python_10
# =========================
"""
You are given an array a consisting of n non-negative integers. You have to choose a non-negative integer x and form a new array b of size n according to the following rule: for all i from 1 to n, b_i = a_i ⊕ x (⊕ denotes the operation [bitwise XOR](https://en.wikipedia.org/wiki/Bitwise_operation#XOR)).

An inversion in the b array is a pair of integers i and j such that 1 ≤ i < j ≤ n and b_i > b_j.

You should choose x in such a way that the number of inversions in b is minimized. If there are several options for x — output the smallest one.

Input

First line contains a single integer n (1 ≤ n ≤ 3 ⋅ 10^5) — the number of elements in a.

Second line contains n space-separated integers a_1, a_2, ..., a_n (0 ≤ a_i ≤ 10^9), where a_i is the i-th element of a.

Output

Output two integers: the minimum possible number of inversions in b, and the minimum possible value of x, which achieves those number of inversions.

Examples

Input


4
0 1 3 2


Output


1 0


Input


9
10 7 9 10 7 5 5 3 5


Output


4 14


Input


3
8 10 3


Output


0 8

Note

In the first sample it is optimal to leave the array as it is by choosing x = 0.

In the second sample the selection of x = 14 results in b: [4, 9, 7, 4, 9, 11, 11, 13, 11]. It has 4 inversions:

  * i = 2, j = 3; 
  * i = 2, j = 4; 
  * i = 3, j = 4; 
  * i = 8, j = 9. 



In the third sample the selection of x = 8 results in b: [0, 2, 11]. It has no inversions.
"""

# Original Problem: node_10:cc_python_10
# =========================
n=int(input())
l=input().split()
li=[int(i) for i in l]
xori=0
ans=0
mul=1
for i in range(32):
    hashi1=dict()
    hashi0=dict()
    inv1=0
    inv2=0
    for j in li:
        if(j//2 in hashi1 and j%2==0):
            inv1+=hashi1[j//2]
        if(j//2 in hashi0 and j%2==1):
            inv2+=hashi0[j//2]
        if(j%2):
            if j//2 not in hashi1:
                hashi1[j//2]=1
            else:
                hashi1[j//2]+=1
        else:
            if j//2 not in hashi0:
                hashi0[j//2]=1
            else:
                hashi0[j//2]+=1

    if(inv1<=inv2):
        ans+=inv1
    else:
        ans+=inv2
        xori=xori+mul
    mul*=2
    for j in range(n):
        li[j]=li[j]//2
print(ans,xori)

