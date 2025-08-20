# This file contains original problem queries and their corresponding Python code.

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


# EoP (End of Problem details for node_10:cc_python_10)
# ######################################################################

# Query for: node_11:cc_python_11
# =========================
"""
As you might remember from the previous round, Vova is currently playing a strategic game known as Rage of Empires.

Vova managed to build a large army, but forgot about the main person in the army - the commander. So he tries to hire a commander, and he wants to choose the person who will be respected by warriors.

Each warrior is represented by his personality — an integer number pi. Each commander has two characteristics — his personality pj and leadership lj (both are integer numbers). Warrior i respects commander j only if <image> (<image> is the bitwise excluding OR of x and y).

Initially Vova's army is empty. There are three different types of events that can happen with the army:

  * 1 pi — one warrior with personality pi joins Vova's army; 
  * 2 pi — one warrior with personality pi leaves Vova's army; 
  * 3 pi li — Vova tries to hire a commander with personality pi and leadership li. 



For each event of the third type Vova wants to know how many warriors (counting only those who joined the army and haven't left yet) respect the commander he tries to hire.

Input

The first line contains one integer q (1 ≤ q ≤ 100000) — the number of events.

Then q lines follow. Each line describes the event:

  * 1 pi (1 ≤ pi ≤ 108) — one warrior with personality pi joins Vova's army; 
  * 2 pi (1 ≤ pi ≤ 108) — one warrior with personality pi leaves Vova's army (it is guaranteed that there is at least one such warrior in Vova's army by this moment); 
  * 3 pi li (1 ≤ pi, li ≤ 108) — Vova tries to hire a commander with personality pi and leadership li. There is at least one event of this type. 

Output

For each event of the third type print one integer — the number of warriors who respect the commander Vova tries to hire in the event.

Example

Input

5
1 3
1 4
3 6 3
2 4
3 6 3


Output

1
0

Note

In the example the army consists of two warriors with personalities 3 and 4 after first two events. Then Vova tries to hire a commander with personality 6 and leadership 3, and only one warrior respects him (<image>, and 2 < 3, but <image>, and 5 ≥ 3). Then warrior with personality 4 leaves, and when Vova tries to hire that commander again, there are no warriors who respect him.
"""

# Original Problem: node_11:cc_python_11
# =========================
import sys
from collections import defaultdict

class Node:
	def __init__(self, val):
		self.val = val
		self.left = None
		self.right = None

q = int(sys.stdin.readline())
root = Node(0)
# def search(node, bit, )

for _ in range(q):
	l = list(map(int, sys.stdin.readline().split()))
	if l[0] == 1:
		# add
		bit = 28
		cur = root
		num = l[1]
		# print(num,'num')
		while bit >= 0:
			if ((1<<bit)&num) == (1<<bit):
				if cur.right is None:
					cur.right = Node(1)
					# print(bit,'bit right')
				else:
					cur.right.val += 1
					# print(bit,'bit add right')
				cur = cur.right
			else:
				if cur.left is None:
					cur.left = Node(1)
					# print(bit,'bit  left', cur.left.val)
				else:
					cur.left.val += 1
					# print(bit,'bit add left', cur.left.val)
				cur = cur.left
			bit -= 1
	if l[0] == 2:
		num = l[1]
		bit, cur = 28, root
		# print(num,'num')
		while bit >= 0:
			if((1<<bit)&num) == (1<<bit):
				cur.right.val -= 1
				cur = cur.right
			else:
				cur.left.val -= 1
				cur = cur.left
			bit -= 1
		# remove
	if l[0] == 3:
		# print
		res, cur, bit = 0, root, 28
		# print(res, cur, bit)
		while bit >= 0:
			num = (1<<bit)
			# print(bit,'bit')
			if (num&l[2]) and (num&l[1]):
				# print("A")
				if cur.right is not None:
					res += cur.right.val
				if cur.left is None:
					break
				cur = cur.left
				bit -= 1
				continue
			if (num&l[2]) and not (num&l[1]):
				# print("B")
				if cur.left is not None:
					res += cur.left.val
				if cur.right is None:
					break
				cur = cur.right
				bit -= 1
				continue
			if not (num&l[2]) and (num&l[1]):
				# print("C")
				if cur.right is None:
					break
				cur = cur.right
				bit -= 1
				continue
			if not (num&l[2]) and not (num&l[1]):
				# print("D")
				if cur.left is None:
					break
				cur = cur.left
				bit -= 1
				continue
		print(res)


# EoP (End of Problem details for node_11:cc_python_11)
# ######################################################################

# Query for: node_27:cc_python_27
# =========================
"""
You are given an array a of length n that consists of zeros and ones.

You can perform the following operation multiple times. The operation consists of two steps: 

  1. Choose three integers 1 ≤ x < y < z ≤ n, that form an arithmetic progression (y - x = z - y). 
  2. Flip the values a_x, a_y, a_z (i.e. change 1 to 0, change 0 to 1). 



Determine if it is possible to make all elements of the array equal to zero. If yes, print the operations that lead the the all-zero state. Your solution should not contain more than (⌊ n/3 ⌋ + 12) operations. Here ⌊ q ⌋ denotes the number q rounded down. We can show that it is possible to make all elements equal to zero in no more than this number of operations whenever it is possible to do so at all.

Input

The first line contains a single integer n (3 ≤ n ≤ 10^5) — the length of the array.

The second line contains n integers a_1, a_2, …, a_n (0 ≤ a_i ≤ 1) — the elements of the array.

Output

Print "YES" (without quotes) if the answer exists, otherwise print "NO" (without quotes). You can print each letter in any case (upper or lower).

If there is an answer, in the second line print an integer m (0 ≤ m ≤ (⌊ n/3 ⌋ + 12)) — the number of operations in your answer.

After that in (i + 2)-th line print the i-th operations — the integers x_i, y_i, z_i. You can print them in arbitrary order.

Examples

Input

5
1 1 0 1 1


Output

YES
2
1 3 5
2 3 4


Input

3
0 1 0


Output

NO

Note

In the first sample the shown output corresponds to the following solution: 

  * 1 1 0 1 1 (initial state); 
  * 0 1 1 1 0 (the flipped positions are the first, the third and the fifth elements); 
  * 0 0 0 0 0 (the flipped positions are the second, the third and the fourth elements). 



Other answers are also possible. In this test the number of operations should not exceed ⌊ 5/3 ⌋ + 12 = 1 + 12 = 13.

In the second sample the only available operation is to flip all the elements. This way it is only possible to obtain the arrays 0 1 0 and 1 0 1, but it is impossible to make all elements equal to zero.
"""

# Original Problem: node_27:cc_python_27
# =========================
def solve(a):
    l = len(a)
    d = sum(a[i] * 2 ** i for i in range(l))
    if d == 0:
        return []
    usable = []
    if l >= 3:
        for i in range(l - 2):
            usable.append(0b111 << i)
    if l >= 5:
        for i in range(l - 4):
            usable.append(0b10101 << i)
    if l >= 7:
        for i in range(l - 6):
            usable.append(0b1001001 << i)
    ul = len(usable)
    best_answer = None
    for mask in range(1 << ul):
        start = 0
        clone = mask
        cnt = 0
        while clone:
            if clone % 2 == 1:
                start ^= usable[cnt]
            clone //= 2
            cnt += 1
        if start == d:
            answer = []
            clone = mask
            cnt = 0
            while clone:
                if clone % 2 == 1:
                    answer.append([])
                    used = usable[cnt]
                    cnt2 = 1
                    while used:
                        if used % 2 == 1:
                            answer[-1].append(cnt2)
                        cnt2 += 1
                        used //= 2
                clone //= 2
                cnt += 1
            if best_answer is None or len(best_answer) > len(answer):
                best_answer = answer
    return best_answer


if __name__ == '__main__':
    n = int(input())
    a = list(map(int, input().split()))
    if len(a) <= 10:
        sol = solve(a)
        if sol is None:
            print("NO")
            exit(0)
        print("YES")
        print(len(sol))
        for t in sol:
            print(' '.join(map(str, t)))
        exit(0)
    operations = []
    while len(a) > 10:
        l = len(a)
        last = a[-3:]
        if last == [1, 1, 1]:
            operations.append([l - 2, l - 1, l])
        elif last == [1, 1, 0]:
            operations.append([l - 3, l - 2, l - 1])
            a[-4] ^= 1
        elif last == [1, 0, 1]:
            operations.append([l - 4, l - 2, l])
            a[-5] ^= 1
        elif last == [0, 1, 1]:
            nxt = a[-6:-3]
            if nxt == [1, 1, 1]:
                operations.append([l - 8, l - 4, l])
                operations.append([l - 5, l - 3, l - 1])
                a[-9] ^= 1
            elif nxt == [1, 1, 0]:
                operations.append([l - 8, l - 4, l])
                operations.append([l - 9, l - 5, l - 1])
                a[-9] ^= 1
                a[-10] ^= 1
            elif nxt == [1, 0, 1]:
                operations.append([l - 6, l - 3, l])
                operations.append([l - 9, l - 5, l - 1])
                a[-7] ^= 1
                a[-10] ^= 1
            elif nxt == [0, 1, 1]:
                operations.append([l - 6, l - 3, l])
                operations.append([l - 7, l - 4, l - 1])
                a[-7] ^= 1
                a[-8] ^= 1
            elif nxt == [1, 0, 0]:
                operations.append([l - 2, l - 1, l])
                operations.append([l - 8, l - 5, l - 2])
                a[-9] ^= 1
            elif nxt == [0, 1, 0]:
                operations.append([l - 2, l - 1, l])
                operations.append([l - 6, l - 4, l - 2])
                a[-7] ^= 1
            elif nxt == [0, 0, 1]:
                operations.append([l - 10, l - 5, l])
                operations.append([l - 5, l - 3, l - 1])
                a[-11] ^= 1
            elif nxt == [0, 0, 0]:
                operations.append([l - 8, l - 4, l])
                operations.append([l - 7, l - 4, l - 1])
                a[-9] ^= 1
                a[-8] ^= 1
            a.pop()
            a.pop()
            a.pop()
        elif last == [1, 0, 0]:
            operations.append([l - 4, l - 3, l - 2])
            a[-5] ^= 1
            a[-4] ^= 1
        elif last == [0, 1, 0]:
            operations.append([l - 5, l - 3, l - 1])
            a[-6] ^= 1
            a[-4] ^= 1
        elif last == [0, 0, 1]:
            operations.append([l - 6, l - 3, l])
            a[-7] ^= 1
            a[-4] ^= 1
        a.pop()
        a.pop()
        a.pop()
    while len(a) < 8:
        a.append(0)
    sol = solve(a)
    print("YES")
    sol = operations + sol
    print(len(sol))
    for t in sol:
        print(' '.join(map(str, t)))


# End of all problems.
