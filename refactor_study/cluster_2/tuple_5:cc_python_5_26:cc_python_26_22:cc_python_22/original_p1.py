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

# Original Problem: node_22:cc_python_22
# =========================
import sys
input = lambda: sys.stdin.readline().rstrip()

def scc(E):
    n = len(E)
    iE = [[] for _ in range(n)]
    for i, e in enumerate(E):
        for v in e:
            iE[v].append(i)
    T = []
    done = [0] * n # 0 -> 1 -> 2
    ct = 0
    for i0 in range(n):
        if done[i0]: continue
        Q = [~i0, i0]
        while Q:
            i = Q.pop()
            if i < 0:
                if done[~i] == 2: continue
                done[~i] = 2
                T.append(~i)
                ct += 1
                continue
            if i >= 0:
                if done[i]: continue
                done[i] = 1
            for j in E[i]:
                if done[j]: continue
                Q.append(~j)
                Q.append(j)
    
    done = [0] * n
    SCC = []
    ### ID ���K�v�ȂƂ�
    I = [0] * n
    ###
    for i0 in T[::-1]:
        if done[i0]: continue
        L = []
        Q = [~i0, i0]
        while Q:
            i = Q.pop()
            if i < 0:
                if done[~i] == 2: continue
                done[~i] = 2
                L.append(~i)
                ###
                I[~i] = len(SCC)
                ###
                continue
            if i >= 0:
                if done[i]: continue
                done[i] = 1
            for j in iE[i]:
                if done[j]: continue
                Q.append(~j)
                Q.append(j)
        SCC.append(L)
    # return SCC, I
    
    ### �� Edge ���K�v�ȂƂ� �i��� return �������j
    # nE = [set() for _ in range(len(SCC))]
    # iE = [set() for _ in range(len(SCC))]
    ciE = [1] * len(SCC)
    for i, e in enumerate(E):
        for j in e:
            if I[i] == I[j]: continue
            # print("i, j, I[i], I[j] =", i, j, I[i], I[j])
            # nE[I[i]].add(I[j])
            # iE[I[j]].add(I[i])
            ciE[I[j]] = 0
    # nE = [list(e) for e in nE]
    # iE = [list(e) for e in iE]
    return ciE
    # return SCC, I, nE, iE, ciE

N, M = map(int, input().split())
Z = [[1 if a == "#" else 0 for a in input()] for _ in range(N)]

su = sum([int(a) for a in input().split()])

I = []
ZZ = [[-1] * M for _ in range(N)]
for j in range(M):
    for i in range(N)[::-1]:
        if Z[i][j]:
            ZZ[i][j] = len(I)
            I.append((i << 20) ^ j)
        elif i < N - 1:
            ZZ[i][j] = ZZ[i+1][j]

mmm = (1 << 20) - 1
E = [[] for _ in range(su)]
for k in range(su):
    ij = I[k]
    i = ij >> 20
    j = ij & mmm
    if i < N - 1 and ZZ[i+1][j] >= 0:
        E[k].append(ZZ[i+1][j])
    if i and Z[i-1][j]:
        E[k].append(ZZ[i-1][j])
    if j and ZZ[i][j-1] >= 0:
        E[k].append(ZZ[i][j-1])
    if j < M - 1 and ZZ[i][j+1] >= 0:
        E[k].append(ZZ[i][j+1])

ciE = scc(E)

print(sum(ciE))

