# This file contains original problem queries and their corresponding Python code.

# Query for: node_14:cc_python_14
# =========================
"""
Maxim has opened his own restaurant! The restaurant has got a huge table, the table's length is p meters.

Maxim has got a dinner party tonight, n guests will come to him. Let's index the guests of Maxim's restaurant from 1 to n. Maxim knows the sizes of all guests that are going to come to him. The i-th guest's size (ai) represents the number of meters the guest is going to take up if he sits at the restaurant table.

Long before the dinner, the guests line up in a queue in front of the restaurant in some order. Then Maxim lets the guests in, one by one. Maxim stops letting the guests in when there is no place at the restaurant table for another guest in the queue. There is no place at the restaurant table for another guest in the queue, if the sum of sizes of all guests in the restaurant plus the size of this guest from the queue is larger than p. In this case, not to offend the guest who has no place at the table, Maxim doesn't let any other guest in the restaurant, even if one of the following guests in the queue would have fit in at the table.

Maxim is now wondering, what is the average number of visitors who have come to the restaurant for all possible n! orders of guests in the queue. Help Maxim, calculate this number.

Input

The first line contains integer n (1 ≤ n ≤ 50) — the number of guests in the restaurant. The next line contains integers a1, a2, ..., an (1 ≤ ai ≤ 50) — the guests' sizes in meters. The third line contains integer p (1 ≤ p ≤ 50) — the table's length in meters. 

The numbers in the lines are separated by single spaces.

Output

In a single line print a real number — the answer to the problem. The answer will be considered correct, if the absolute or relative error doesn't exceed 10 - 4.

Examples

Input

3
1 2 3
3


Output

1.3333333333

Note

In the first sample the people will come in the following orders: 

  * (1, 2, 3) — there will be two people in the restaurant; 
  * (1, 3, 2) — there will be one person in the restaurant; 
  * (2, 1, 3) — there will be two people in the restaurant; 
  * (2, 3, 1) — there will be one person in the restaurant; 
  * (3, 1, 2) — there will be one person in the restaurant; 
  * (3, 2, 1) — there will be one person in the restaurant. 



In total we get (2 + 1 + 2 + 1 + 1 + 1) / 6 = 8 / 6 = 1.(3).
"""

# Original Problem: node_14:cc_python_14
# =========================
import math

n = int(input())
a = [int(x) for x in input().split()]
p = int(input())

sum=0;
for x in range(n):
	sum+=a[x]
if(sum<=p):
	print(n)
else:
	ans=0
	for i in range(n):
		dp = [[[0 for z in range(55)] for y in range(55)] for x in range(55)]
		dp[-1][0][0]=1
		for j in range(n):
			if(j==i):

				for k in range(n):
					for z in range(p+1):
						dp[j][k][z]=dp[j-1][k][z]
				continue

			for k in range(n):

				for z in range(p+1):

					if(z+a[j]<=p):
						dp[j][k+1][z+a[j]]+=dp[j-1][k][z]
					dp[j][k][z]+=dp[j-1][k][z]


		for k in range(n):
			for z in range(p+1):
				if(z+a[i]>p):
					ans+=k*dp[n-1][k][z]*math.factorial(k)*math.factorial(n-k-1)

	print(ans/math.factorial(n))


# EoP (End of Problem details for node_14:cc_python_14)
# ######################################################################

# Query for: node_19:cc_python_19
# =========================
"""
Maxim has opened his own restaurant! The restaurant has got a huge table, the table's length is p meters.

Maxim has got a dinner party tonight, n guests will come to him. Let's index the guests of Maxim's restaurant from 1 to n. Maxim knows the sizes of all guests that are going to come to him. The i-th guest's size (ai) represents the number of meters the guest is going to take up if he sits at the restaurant table.

Long before the dinner, the guests line up in a queue in front of the restaurant in some order. Then Maxim lets the guests in, one by one. Maxim stops letting the guests in when there is no place at the restaurant table for another guest in the queue. There is no place at the restaurant table for another guest in the queue, if the sum of sizes of all guests in the restaurant plus the size of this guest from the queue is larger than p. In this case, not to offend the guest who has no place at the table, Maxim doesn't let any other guest in the restaurant, even if one of the following guests in the queue would have fit in at the table.

Maxim is now wondering, what is the average number of visitors who have come to the restaurant for all possible n! orders of guests in the queue. Help Maxim, calculate this number.

Input

The first line contains integer n (1 ≤ n ≤ 50) — the number of guests in the restaurant. The next line contains integers a1, a2, ..., an (1 ≤ ai ≤ 50) — the guests' sizes in meters. The third line contains integer p (1 ≤ p ≤ 50) — the table's length in meters. 

The numbers in the lines are separated by single spaces.

Output

In a single line print a real number — the answer to the problem. The answer will be considered correct, if the absolute or relative error doesn't exceed 10 - 4.

Examples

Input

3
1 2 3
3


Output

1.3333333333

Note

In the first sample the people will come in the following orders: 

  * (1, 2, 3) — there will be two people in the restaurant; 
  * (1, 3, 2) — there will be one person in the restaurant; 
  * (2, 1, 3) — there will be two people in the restaurant; 
  * (2, 3, 1) — there will be one person in the restaurant; 
  * (3, 1, 2) — there will be one person in the restaurant; 
  * (3, 2, 1) — there will be one person in the restaurant. 



In total we get (2 + 1 + 2 + 1 + 1 + 1) / 6 = 8 / 6 = 1.(3).
"""

# Original Problem: node_19:cc_python_19
# =========================
n=int(input())
arr=list(map(int,input().split()))
p=int(input())
dp=[[[0 for k in range(n+1)] for i in range(p+1)] for i in range(n+1)]
for j in range(p+1):
    for k in range(n+1):
        dp[0][j][k]=1
for i in range(1,n+1):
    for j in range(p+1):
        for k in range(1,n+1):
            if j>=arr[k-1]:
                dp[i][j][k]=dp[i][j][k-1]+i*dp[i-1][j-arr[k-1]][k-1]
            else:
                dp[i][j][k]=dp[i][j][k-1]
fact=n
ans=0
for i in range(1,n+1):
    ans+=dp[i][p][n]/fact
    fact*=(n-i)
print(ans)


# EoP (End of Problem details for node_19:cc_python_19)
# ######################################################################

# Query for: node_7:cc_python_7
# =========================
"""
Hyakugoku has just retired from being the resident deity of the South Black Snail Temple in order to pursue her dream of becoming a cartoonist. She spent six months in that temple just playing "Cat's Cradle" so now she wants to try a different game — "Snakes and Ladders". Unfortunately, she already killed all the snakes, so there are only ladders left now. 

The game is played on a 10 × 10 board as follows:

  * At the beginning of the game, the player is at the bottom left square. 
  * The objective of the game is for the player to reach the Goal (the top left square) by following the path and climbing vertical ladders. Once the player reaches the Goal, the game ends. 
  * The path is as follows: if a square is not the end of its row, it leads to the square next to it along the direction of its row; if a square is the end of its row, it leads to the square above it. The direction of a row is determined as follows: the direction of the bottom row is to the right; the direction of any other row is opposite the direction of the row below it. See Notes section for visualization of path. 
  * During each turn, the player rolls a standard six-sided dice. Suppose that the number shown on the dice is r. If the Goal is less than r squares away on the path, the player doesn't move (but the turn is performed). Otherwise, the player advances exactly r squares along the path and then stops. If the player stops on a square with the bottom of a ladder, the player chooses whether or not to climb up that ladder. If she chooses not to climb, then she stays in that square for the beginning of the next turn. 
  * Some squares have a ladder in them. Ladders are only placed vertically — each one leads to the same square of some of the upper rows. In order for the player to climb up a ladder, after rolling the dice, she must stop at the square containing the bottom of the ladder. After using the ladder, the player will end up in the square containing the top of the ladder. She cannot leave the ladder in the middle of climbing. And if the square containing the top of the ladder also contains the bottom of another ladder, she is not allowed to use that second ladder. 
  * The numbers on the faces of the dice are 1, 2, 3, 4, 5, and 6, with each number having the same probability of being shown. 



Please note that: 

  * it is possible for ladders to overlap, but the player cannot switch to the other ladder while in the middle of climbing the first one; 
  * it is possible for ladders to go straight to the top row, but not any higher; 
  * it is possible for two ladders to lead to the same tile; 
  * it is possible for a ladder to lead to a tile that also has a ladder, but the player will not be able to use that second ladder if she uses the first one; 
  * the player can only climb up ladders, not climb down. 



Hyakugoku wants to finish the game as soon as possible. Thus, on each turn she chooses whether to climb the ladder or not optimally. Help her to determine the minimum expected number of turns the game will take.

Input

Input will consist of ten lines. The i-th line will contain 10 non-negative integers h_{i1}, h_{i2}, ..., h_{i10}. If h_{ij} is 0, then the tile at the i-th row and j-th column has no ladder. Otherwise, the ladder at that tile will have a height of h_{ij}, i.e. climbing it will lead to the tile h_{ij} rows directly above. It is guaranteed that 0 ≤ h_{ij} < i. Also, the first number of the first line and the first number of the last line always contain 0, i.e. the Goal and the starting tile never have ladders.

Output

Print only one line containing a single floating-point number — the minimum expected number of turns Hyakugoku can take to finish the game. Your answer will be considered correct if its absolute or relative error does not exceed 10^{-6}.

Examples

Input


0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0


Output


33.0476190476


Input


0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0
0 0 3 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 9


Output


20.2591405923


Input


0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 6 6 6 6 6 6 0 0 0
1 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0


Output


15.9047592939

Note

A visualization of the path and the board from example 2 is as follows: <image>

The tile with an 'S' is the starting tile and the tile with an 'E' is the Goal.

For the first example, there are no ladders.

For the second example, the board looks like the one in the right part of the image (the ladders have been colored for clarity).

It is possible for ladders to overlap, as is the case with the red and yellow ladders and green and blue ladders. It is also possible for ladders to go straight to the top, as is the case with the black and blue ladders. However, it is not possible for ladders to go any higher (outside of the board). It is also possible that two ladders lead to the same tile, as is the case with the red and yellow ladders. Also, notice that the red and yellow ladders lead to the tile with the orange ladder. So if the player chooses to climb either of the red and yellow ladders, they will not be able to climb the orange ladder. Finally, notice that the green ladder passes through the starting tile of the blue ladder. The player cannot transfer from the green ladder to the blue ladder while in the middle of climbing the green ladder.
"""

# Original Problem: node_7:cc_python_7
# =========================
X = [[int(a) for a in input().split()] for _ in range(10)]
Y = [(i//10, 9-i%10 if (i//10)&1 else i%10) for i in range(100)]
Z = [[i * 10 + 9 - j if i & 1 else i * 10 + j for j in range(10)] for i in range(10)]
E = [0] * 100
F = [0] * 100
for i in range(1, 6):
    F[i] = E[i] = (sum(E[:i]) + 6) / i
for i in range(6, 100):
    F[i] = E[i] = sum(F[i-6:i])/6 + 1
    x, y = Y[i]
    if X[x][y]: F[i] = min(E[i], E[Z[x-X[x][y]][y]])

print(F[99])


# End of all problems.
