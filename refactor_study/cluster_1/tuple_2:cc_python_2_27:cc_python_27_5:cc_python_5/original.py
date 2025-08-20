# This file contains original problem queries and their corresponding Python code.

# Query for: node_27:cc_python_27
# =========================
"""
Let's call a non-empty sequence of positive integers a1, a2... ak coprime if the greatest common divisor of all elements of this sequence is equal to 1.

Given an array a consisting of n positive integers, find the number of its coprime subsequences. Since the answer may be very large, print it modulo 109 + 7.

Note that two subsequences are considered different if chosen indices are different. For example, in the array [1, 1] there are 3 different subsequences: [1], [1] and [1, 1].

Input

The first line contains one integer number n (1 ≤ n ≤ 100000).

The second line contains n integer numbers a1, a2... an (1 ≤ ai ≤ 100000).

Output

Print the number of coprime subsequences of a modulo 109 + 7.

Examples

Input

3
1 2 3


Output

5


Input

4
1 1 1 1


Output

15


Input

7
1 3 5 15 3 105 35


Output

100

Note

In the first example coprime subsequences are: 

  1. 1
  2. 1, 2
  3. 1, 3
  4. 1, 2, 3
  5. 2, 3



In the second example all subsequences are coprime.
"""

# Original Problem: node_27:cc_python_27
# =========================
# 803F
import math
import collections
def do():
    n = int(input())
    nums = map(int, input().split(" "))
    count = collections.defaultdict(int)
    for num in nums:
        for i in range(1, int(math.sqrt(num))+1):
            cp = num // i
            if num % i == 0:
                count[i] += 1
            if cp != i and num % cp == 0:
                count[cp] += 1
    maxk = max(count.keys())
    freq = {k: (1 << count[k]) - 1 for k in count}
    for k in sorted(count.keys(), reverse=True):
        for kk in range(k << 1, maxk+1, k):
            freq[k] -= freq[kk] if kk in freq else 0
    return freq[1] % (10**9 + 7)

print(do())


# EoP (End of Problem details for node_27:cc_python_27)
# ######################################################################

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


# EoP (End of Problem details for node_2:cc_python_2)
# ######################################################################

# Query for: node_5:cc_python_5
# =========================
"""
Johnny has recently found an ancient, broken computer. The machine has only one register, which allows one to put in there one variable. Then in one operation, you can shift its bits left or right by at most three positions. The right shift is forbidden if it cuts off some ones. So, in fact, in one operation, you can multiply or divide your number by 2, 4 or 8, and division is only allowed if the number is divisible by the chosen divisor. 

Formally, if the register contains a positive integer x, in one operation it can be replaced by one of the following: 

  * x ⋅ 2 
  * x ⋅ 4 
  * x ⋅ 8 
  * x / 2, if x is divisible by 2 
  * x / 4, if x is divisible by 4 
  * x / 8, if x is divisible by 8 



For example, if x = 6, in one operation it can be replaced by 12, 24, 48 or 3. Value 6 isn't divisible by 4 or 8, so there're only four variants of replacement.

Now Johnny wonders how many operations he needs to perform if he puts a in the register and wants to get b at the end.

Input

The input consists of multiple test cases. The first line contains an integer t (1 ≤ t ≤ 1000) — the number of test cases. The following t lines contain a description of test cases.

The first and only line in each test case contains integers a and b (1 ≤ a, b ≤ 10^{18}) — the initial and target value of the variable, respectively.

Output

Output t lines, each line should contain one integer denoting the minimum number of operations Johnny needs to perform. If Johnny cannot get b at the end, then write -1.

Example

Input


10
10 5
11 44
17 21
1 1
96 3
2 128
1001 1100611139403776
1000000000000000000 1000000000000000000
7 1
10 8


Output


1
1
-1
0
2
2
14
0
-1
-1

Note

In the first test case, Johnny can reach 5 from 10 by using the shift to the right by one (i.e. divide by 2).

In the second test case, Johnny can reach 44 from 11 by using the shift to the left by two (i.e. multiply by 4).

In the third test case, it is impossible for Johnny to reach 21 from 17.

In the fourth test case, initial and target values are equal, so Johnny has to do 0 operations.

In the fifth test case, Johnny can reach 3 from 96 by using two shifts to the right: one by 2, and another by 3 (i.e. divide by 4 and by 8).
"""

# Original Problem: node_5:cc_python_5
# =========================
# from debug import debug
import math
t = int(input())

for ii in range(t):
	a, b = map(int, input().split())
	if a == b:
		print(0)
	else:
		b, a = min(a,b), max(a,b)
		if a%b:
			print(-1)
		else:
			aa = int(math.log2(a//b))
			if pow(2, aa) == a//b:
				c = 0
				c += aa//3
				aa = aa%3

				c += aa//2
				aa = aa%2

				c += aa//1
				aa = aa%1
				print(c)
			else:
				print(-1)


# End of all problems.
