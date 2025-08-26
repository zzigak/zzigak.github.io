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

