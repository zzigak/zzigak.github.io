# This file contains original problem queries and their corresponding Python code.

# Query for: node_11:cc_python_11
# =========================
"""
Vasya plays one very well-known and extremely popular MMORPG game. His game character has k skill; currently the i-th of them equals to ai. Also this game has a common rating table in which the participants are ranked according to the product of all the skills of a hero in the descending order.

Vasya decided to 'upgrade' his character via the game store. This store offers n possible ways to improve the hero's skills; Each of these ways belongs to one of three types:

  1. assign the i-th skill to b; 
  2. add b to the i-th skill; 
  3. multiply the i-th skill by b. 



Unfortunately, a) every improvement can only be used once; b) the money on Vasya's card is enough only to purchase not more than m of the n improvements. Help Vasya to reach the highest ranking in the game. To do this tell Vasya which of improvements he has to purchase and in what order he should use them to make his rating become as high as possible. If there are several ways to achieve it, print any of them.

Input

The first line contains three numbers — k, n, m (1 ≤ k ≤ 105, 0 ≤ m ≤ n ≤ 105) — the number of skills, the number of improvements on sale and the number of them Vasya can afford.

The second line contains k space-separated numbers ai (1 ≤ ai ≤ 106), the initial values of skills.

Next n lines contain 3 space-separated numbers tj, ij, bj (1 ≤ tj ≤ 3, 1 ≤ ij ≤ k, 1 ≤ bj ≤ 106) — the type of the j-th improvement (1 for assigning, 2 for adding, 3 for multiplying), the skill to which it can be applied and the value of b for this improvement.

Output

The first line should contain a number l (0 ≤ l ≤ m) — the number of improvements you should use.

The second line should contain l distinct space-separated numbers vi (1 ≤ vi ≤ n) — the indices of improvements in the order in which they should be applied. The improvements are numbered starting from 1, in the order in which they appear in the input. 

Examples

Input

2 4 3
13 20
1 1 14
1 2 30
2 1 6
3 2 2


Output

3
2 3 4
"""

# Original Problem: node_11:cc_python_11
# =========================
def euclid(a, b):
	if b == 0:
		return (1, 0, a)
	else:
		(x, y, g) = euclid(b, a%b)
		return (y, x - a//b*y, g)

def modDivide(a, b, p):
	(x, y, g) = euclid(b, p)
	return a // g * (x + p) % p

def comb(n, k):
	return modDivide(fac[n], fac[k] * fac[n-k] % P, P)

k, n, m = list(map(int, input().split()))
a = list(map(int, input().split()))
skill = []
l = [[[], [], []] for i in range(k)]
for j in range(n):
	t = list(map(int, input().split()))
	skill.append(t)
	(t, i, b) = t
	l[i-1][t-1].append((b, j+1))
for i in range(k):
	for j in range(3):
		l[i][j].sort(reverse=True)
op = []
for i in range(k):
	t = l[i][1][:]
	if len(l[i][0]) != 0 and l[i][0][0][0] > a[i]:
		t.append((l[i][0][0][0] - a[i], l[i][0][0][1]))
		t.sort(reverse=True)
	s = a[i]
	for (add, index) in t:
		op.append(((s+add)/s, index))
		s += add
	for (mul, index) in l[i][2]:
		op.append((mul, index))
op.sort(reverse=True)
st = set(map(lambda t : t[1], op[:m]))
print(len(st))
for i in range(k):
	for j in range(3):
		for (mul, index) in l[i][j]:
			if index in st:
				print(index, end=' ')


# EoP (End of Problem details for node_11:cc_python_11)
# ######################################################################

# Query for: node_12:cc_python_12
# =========================
"""
The dragon and the princess are arguing about what to do on the New Year's Eve. The dragon suggests flying to the mountains to watch fairies dancing in the moonlight, while the princess thinks they should just go to bed early. They are desperate to come to an amicable agreement, so they decide to leave this up to chance.

They take turns drawing a mouse from a bag which initially contains w white and b black mice. The person who is the first to draw a white mouse wins. After each mouse drawn by the dragon the rest of mice in the bag panic, and one of them jumps out of the bag itself (the princess draws her mice carefully and doesn't scare other mice). Princess draws first. What is the probability of the princess winning?

If there are no more mice in the bag and nobody has drawn a white mouse, the dragon wins. Mice which jump out of the bag themselves are not considered to be drawn (do not define the winner). Once a mouse has left the bag, it never returns to it. Every mouse is drawn from the bag with the same probability as every other one, and every mouse jumps out of the bag with the same probability as every other one.

Input

The only line of input data contains two integers w and b (0 ≤ w, b ≤ 1000).

Output

Output the probability of the princess winning. The answer is considered to be correct if its absolute or relative error does not exceed 10 - 9.

Examples

Input

1 3


Output

0.500000000


Input

5 5


Output

0.658730159

Note

Let's go through the first sample. The probability of the princess drawing a white mouse on her first turn and winning right away is 1/4. The probability of the dragon drawing a black mouse and not winning on his first turn is 3/4 * 2/3 = 1/2. After this there are two mice left in the bag — one black and one white; one of them jumps out, and the other is drawn by the princess on her second turn. If the princess' mouse is white, she wins (probability is 1/2 * 1/2 = 1/4), otherwise nobody gets the white mouse, so according to the rule the dragon wins.
"""

# Original Problem: node_12:cc_python_12
# =========================
w,b = list( map(int, input().split()) )
p = []
for i in range(w+1): p.append([0]*(b+1))
for i in range(1,w+1): p[i][0] = 1

for i in range(1,w+1):
    for j in range(1,b+1):
        p[i][j] = i/(i+j)
        if j>=3:
            p[i][j] += (j/(i+j)) * ((j-1)/(i+j-1)) * ((j-2)/(i+j-2)) * p[i][j-3]
        if j>=2:
            p[i][j] += (j/(i+j)) * ((j-1)/(i+j-1)) * ((i)/(i+j-2)) * p[i-1][j-2]

print("%.9f" % p[w][b])


# EoP (End of Problem details for node_12:cc_python_12)
# ######################################################################

# Query for: node_2:cc_python_2
# =========================
"""
Yakko, Wakko and Dot, world-famous animaniacs, decided to rest from acting in cartoons, and take a leave to travel a bit. Yakko dreamt to go to Pennsylvania, his Motherland and the Motherland of his ancestors. Wakko thought about Tasmania, its beaches, sun and sea. Dot chose Transylvania as the most mysterious and unpredictable place.

But to their great regret, the leave turned to be very short, so it will be enough to visit one of the three above named places. That's why Yakko, as the cleverest, came up with a truly genius idea: let each of the three roll an ordinary six-sided die, and the one with the highest amount of points will be the winner, and will take the other two to the place of his/her dreams.

Yakko thrown a die and got Y points, Wakko — W points. It was Dot's turn. But she didn't hurry. Dot wanted to know for sure what were her chances to visit Transylvania.

It is known that Yakko and Wakko are true gentlemen, that's why if they have the same amount of points with Dot, they will let Dot win.

Input

The only line of the input file contains two natural numbers Y and W — the results of Yakko's and Wakko's die rolls.

Output

Output the required probability in the form of irreducible fraction in format «A/B», where A — the numerator, and B — the denominator. If the required probability equals to zero, output «0/1». If the required probability equals to 1, output «1/1». 

Examples

Input

4 2


Output

1/2

Note

Dot will go to Transylvania, if she is lucky to roll 4, 5 or 6 points.
"""

# Original Problem: node_2:cc_python_2
# =========================
x, y = input().split()
x = int(x)
y = int(y)
z = 7 - max(x, y)
ans = z/6
if ans == (1/6):
    print("1/6")
elif ans == (2/6):
    print("1/3")
elif ans == (3/6):
    print("1/2")
elif ans == (4/6):
    print("2/3")
elif ans == (5/6):
    print("5/6")
else:
    print("1/1")


# End of all problems.
