# This file contains original problem queries and their corresponding Python code.

# Query for: node_22:cc_python_22
# =========================
"""
This is the easy version of the problem. The difference between the versions is the constraints on a_i. You can make hacks only if all versions of the problem are solved.

Little Dormi has recently received a puzzle from his friend and needs your help to solve it. 

The puzzle consists of an upright board with n rows and m columns of cells, some empty and some filled with blocks of sand, and m non-negative integers a_1,a_2,…,a_m (0 ≤ a_i ≤ n). In this version of the problem, a_i will be equal to the number of blocks of sand in column i.

When a cell filled with a block of sand is disturbed, the block of sand will fall from its cell to the sand counter at the bottom of the column (each column has a sand counter). While a block of sand is falling, other blocks of sand that are adjacent at any point to the falling block of sand will also be disturbed and start to fall. Specifically, a block of sand disturbed at a cell (i,j) will pass through all cells below and including the cell (i,j) within the column, disturbing all adjacent cells along the way. Here, the cells adjacent to a cell (i,j) are defined as (i-1,j), (i,j-1), (i+1,j), and (i,j+1) (if they are within the grid). Note that the newly falling blocks can disturb other blocks.

In one operation you are able to disturb any piece of sand. The puzzle is solved when there are at least a_i blocks of sand counted in the i-th sand counter for each column from 1 to m.

You are now tasked with finding the minimum amount of operations in order to solve the puzzle. Note that Little Dormi will never give you a puzzle that is impossible to solve.

Input

The first line consists of two space-separated positive integers n and m (1 ≤ n ⋅ m ≤ 400 000).

Each of the next n lines contains m characters, describing each row of the board. If a character on a line is '.', the corresponding cell is empty. If it is '#', the cell contains a block of sand.

The final line contains m non-negative integers a_1,a_2,…,a_m (0 ≤ a_i ≤ n) — the minimum amount of blocks of sand that needs to fall below the board in each column. In this version of the problem, a_i will be equal to the number of blocks of sand in column i.

Output

Print one non-negative integer, the minimum amount of operations needed to solve the puzzle.

Examples

Input


5 7
#....#.
.#.#...
#....#.
#....##
#.#....
4 1 1 1 0 3 1


Output


3


Input


3 3
#.#
#..
##.
3 1 1


Output


1

Note

For example 1, by disturbing both blocks of sand on the first row from the top at the first and sixth columns from the left, and the block of sand on the second row from the top and the fourth column from the left, it is possible to have all the required amounts of sand fall in each column. It can be proved that this is not possible with fewer than 3 operations, and as such the answer is 3. Here is the puzzle from the first example.

<image>

For example 2, by disturbing the cell on the top row and rightmost column, one can cause all of the blocks of sand in the board to fall into the counters at the bottom. Thus, the answer is 1. Here is the puzzle from the second example.

<image>
"""

# Query for: node_26:cc_python_26
# =========================
"""
Nastia has an unweighted tree with n vertices and wants to play with it!

The girl will perform the following operation with her tree, as long as she needs:

  1. Remove any existing edge. 
  2. Add an edge between any pair of vertices. 



What is the minimum number of operations Nastia needs to get a bamboo from a tree? A bamboo is a tree in which no node has a degree greater than 2.

Input

The first line contains a single integer t (1 ≤ t ≤ 10 000) — the number of test cases.

The first line of each test case contains a single integer n (2 ≤ n ≤ 10^5) — the number of vertices in the tree.

Next n - 1 lines of each test cases describe the edges of the tree in form a_i, b_i (1 ≤ a_i, b_i ≤ n, a_i ≠ b_i).

It's guaranteed the given graph is a tree and the sum of n in one test doesn't exceed 2 ⋅ 10^5.

Output

For each test case in the first line print a single integer k — the minimum number of operations required to obtain a bamboo from the initial tree.

In the next k lines print 4 integers x_1, y_1, x_2, y_2 (1 ≤ x_1, y_1, x_2, y_{2} ≤ n, x_1 ≠ y_1, x_2 ≠ y_2) — this way you remove the edge (x_1, y_1) and add an undirected edge (x_2, y_2).

Note that the edge (x_1, y_1) must be present in the graph at the moment of removing.

Example

Input


2
7
1 2
1 3
2 4
2 5
3 6
3 7
4
1 2
1 3
3 4


Output


2
2 5 6 7
3 6 4 5
0

Note

Note the graph can be unconnected after a certain operation.

Consider the first test case of the example: 

<image> The red edges are removed, and the green ones are added.
"""

# Query for: node_5:cc_python_5
# =========================
"""
Mr. Kitayuta has just bought an undirected graph consisting of n vertices and m edges. The vertices of the graph are numbered from 1 to n. Each edge, namely edge i, has a color ci, connecting vertex ai and bi.

Mr. Kitayuta wants you to process the following q queries.

In the i-th query, he gives you two integers — ui and vi.

Find the number of the colors that satisfy the following condition: the edges of that color connect vertex ui and vertex vi directly or indirectly.

Input

The first line of the input contains space-separated two integers — n and m (2 ≤ n ≤ 100, 1 ≤ m ≤ 100), denoting the number of the vertices and the number of the edges, respectively.

The next m lines contain space-separated three integers — ai, bi (1 ≤ ai < bi ≤ n) and ci (1 ≤ ci ≤ m). Note that there can be multiple edges between two vertices. However, there are no multiple edges of the same color between two vertices, that is, if i ≠ j, (ai, bi, ci) ≠ (aj, bj, cj).

The next line contains a integer — q (1 ≤ q ≤ 100), denoting the number of the queries.

Then follows q lines, containing space-separated two integers — ui and vi (1 ≤ ui, vi ≤ n). It is guaranteed that ui ≠ vi.

Output

For each query, print the answer in a separate line.

Examples

Input

4 5
1 2 1
1 2 2
2 3 1
2 3 3
2 4 3
3
1 2
3 4
1 4


Output

2
1
0


Input

5 7
1 5 1
2 5 1
3 5 1
4 5 1
1 2 2
2 3 2
3 4 2
5
1 5
5 1
2 5
1 5
1 4


Output

1
1
1
1
2

Note

Let's consider the first sample. 

<image> The figure above shows the first sample. 

  * Vertex 1 and vertex 2 are connected by color 1 and 2. 
  * Vertex 3 and vertex 4 are connected by color 3. 
  * Vertex 1 and vertex 4 are not connected by any single color.
"""