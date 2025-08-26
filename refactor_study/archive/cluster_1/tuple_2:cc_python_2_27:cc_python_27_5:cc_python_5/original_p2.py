# Query for: node_2:cc_python_2
# =========================
"""
Two little greedy bears have found two pieces of cheese in the forest of weight a and b grams, correspondingly. The bears are so greedy that they are ready to fight for the larger piece. That's where the fox comes in and starts the dialog: "Little bears, wait a little, I want to make your pieces equal" "Come off it fox, how are you going to do that?", the curious bears asked. "It's easy", said the fox. "If the mass of a certain piece is divisible by two, then I can eat exactly a half of the piece. If the mass of a certain piece is divisible by three, then I can eat exactly two-thirds, and if the mass is divisible by five, then I can eat four-fifths. I'll eat a little here and there and make the pieces equal". 

The little bears realize that the fox's proposal contains a catch. But at the same time they realize that they can not make the two pieces equal themselves. So they agreed to her proposal, but on one condition: the fox should make the pieces equal as quickly as possible. Find the minimum number of operations the fox needs to make pieces equal.

Input

The first line contains two space-separated integers a and b (1 ≤ a, b ≤ 109). 

Output

If the fox is lying to the little bears and it is impossible to make the pieces equal, print -1. Otherwise, print the required minimum number of operations. If the pieces of the cheese are initially equal, the required number is 0.

Examples

Input

15 20


Output

3


Input

14 8


Output

-1


Input

6 6


Output

0
"""

# Original Problem: node_2:cc_python_2
# =========================
from math import pow
def take_input(s):          #for integer inputs
    if s == 1:  return int(input())
    return map(int, input().split())

def factor(n,k):
    i = 0
    while(n%k==0):
        i += 1
        n //= k
    return i
        
a, b = take_input(2)
count = 0
if a == b:
    print(0)
    exit()

a_fac_2 = factor(a,2); a_fac_3 = factor(a,3); a_fac_5 = factor(a,5)
b_fac_2 = factor(b,2); b_fac_3 = factor(b,3); b_fac_5 = factor(b,5)
x = a
if a_fac_2>0:   x //= pow(2,a_fac_2)
if a_fac_3>0:   x //= pow(3,a_fac_3)
if a_fac_5>0:   x //= pow(5,a_fac_5)
y = b
if b_fac_2>0:   y //= pow(2,b_fac_2)
if b_fac_3>0:   y //= pow(3,b_fac_3)
if b_fac_5>0:   y //= pow(5,b_fac_5)


if x != y:
    print(-1)
else:
    print(abs(a_fac_2 - b_fac_2) + abs(a_fac_3 - b_fac_3) + abs(a_fac_5 - b_fac_5))