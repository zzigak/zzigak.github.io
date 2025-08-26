# This file contains original problem queries and their corresponding Python code.

# Query for: node_13:cc_python_13
# =========================
"""
You're given a tree with n vertices.

Your task is to determine the maximum possible number of edges that can be removed in such a way that all the remaining connected components will have even size.

Input

The first line contains an integer n (1 ≤ n ≤ 10^5) denoting the size of the tree. 

The next n - 1 lines contain two integers u, v (1 ≤ u, v ≤ n) each, describing the vertices connected by the i-th edge.

It's guaranteed that the given edges form a tree.

Output

Output a single integer k — the maximum number of edges that can be removed to leave all connected components with even size, or -1 if it is impossible to remove edges in order to satisfy this property.

Examples

Input

4
2 4
4 1
3 1


Output

1

Input

3
1 2
1 3


Output

-1

Input

10
7 1
8 4
8 10
4 7
6 5
9 3
3 5
2 10
2 5


Output

4

Input

2
1 2


Output

0

Note

In the first example you can remove the edge between vertices 1 and 4. The graph after that will have two connected components with two vertices in each.

In the second example you can't remove edges in such a way that all components have even number of vertices, so the answer is -1.
"""

# Original Problem: node_13:cc_python_13
# =========================
from collections import  defaultdict
import threading
from sys import stdin,setrecursionlimit
setrecursionlimit(300000)
input=stdin.readline

def dfs(node,g,par,sz):
	for i in g[node]:
		if i!=par:
			sz[node]+=dfs(i,g,node,sz)
	return sz[node]+1
def main():
	n=int(input())
	if n%2!=0:
		print(-1)
		exit(0)
	g=defaultdict(list)
	for i in range(n-1):
		x,y=map(int,input().strip().split())
		g[x-1].append(y-1)
		g[y-1].append(x-1)

	sz=[0]*(n)
	tt=[]
	dfs(0,g,-1,sz)
	res=0
	# print(sz)
	for i in range(1,n):
		if sz[i]%2!=0:
			res+=1
	print(res)

threading.stack_size(10 ** 8)
t = threading.Thread(target=main)
t.start()
t.join()


# EoP (End of Problem details for node_13:cc_python_13)
# ######################################################################

# Query for: node_19:cc_python_19
# =========================
"""
Consider a rooted tree. A rooted tree has one special vertex called the root. All edges are directed from the root. Vertex u is called a child of vertex v and vertex v is called a parent of vertex u if there exists a directed edge from v to u. A vertex is called a leaf if it doesn't have children and has a parent.

Let's call a rooted tree a spruce if its every non-leaf vertex has at least 3 leaf children. You are given a rooted tree, check whether it's a spruce.

The definition of a rooted tree can be found [here](https://goo.gl/1dqvzz).

Input

The first line contains one integer n — the number of vertices in the tree (3 ≤ n ≤ 1 000). Each of the next n - 1 lines contains one integer pi (1 ≤ i ≤ n - 1) — the index of the parent of the i + 1-th vertex (1 ≤ pi ≤ i).

Vertex 1 is the root. It's guaranteed that the root has at least 2 children.

Output

Print "Yes" if the tree is a spruce and "No" otherwise.

Examples

Input

4
1
1
1


Output

Yes


Input

7
1
1
1
2
2
2


Output

No


Input

8
1
1
1
1
3
3
3


Output

Yes

Note

The first example:

<image>

The second example:

<image>

It is not a spruce, because the non-leaf vertex 1 has only 2 leaf children.

The third example:

<image>
"""

# Original Problem: node_19:cc_python_19
# =========================
if __name__ == '__main__':
    n = int(input())
    nonleaf = [0 for i in range(1010)]
    child = [[] for i in range(1010)]
    leaf = [0 for i in range(1010)]

    def dfs(s):
        cnt = 0
        for chd in child[s]:
            cnt += dfs(chd)
        leaf[s] = cnt
        return 1 - nonleaf[s]

    for i in range(2, n + 1):
        node = int(input())
        child[node].append(i)
        nonleaf[node] = 1

    dfs(1)

    # print(nonleaf[1:n + 1])
    # print(child[1:n + 1])
    # print(leaf[1:n + 1])

    for i in range(1, n + 1):
        if nonleaf[i] and leaf[i] < 3:
            print("No")
            exit()

    print("Yes")


# EoP (End of Problem details for node_19:cc_python_19)
# ######################################################################

# Query for: node_29:cc_python_29
# =========================
"""
You are given an undirected tree of n vertices. 

Some vertices are colored blue, some are colored red and some are uncolored. It is guaranteed that the tree contains at least one red vertex and at least one blue vertex.

You choose an edge and remove it from the tree. Tree falls apart into two connected components. Let's call an edge nice if neither of the resulting components contain vertices of both red and blue colors.

How many nice edges are there in the given tree?

Input

The first line contains a single integer n (2 ≤ n ≤ 3 ⋅ 10^5) — the number of vertices in the tree.

The second line contains n integers a_1, a_2, ..., a_n (0 ≤ a_i ≤ 2) — the colors of the vertices. a_i = 1 means that vertex i is colored red, a_i = 2 means that vertex i is colored blue and a_i = 0 means that vertex i is uncolored.

The i-th of the next n - 1 lines contains two integers v_i and u_i (1 ≤ v_i, u_i ≤ n, v_i ≠ u_i) — the edges of the tree. It is guaranteed that the given edges form a tree. It is guaranteed that the tree contains at least one red vertex and at least one blue vertex.

Output

Print a single integer — the number of nice edges in the given tree.

Examples

Input


5
2 0 0 1 2
1 2
2 3
2 4
2 5


Output


1


Input


5
1 0 0 0 2
1 2
2 3
3 4
4 5


Output


4


Input


3
1 1 2
2 3
1 3


Output


0

Note

Here is the tree from the first example:

<image>

The only nice edge is edge (2, 4). Removing it makes the tree fall apart into components \{4\} and \{1, 2, 3, 5\}. The first component only includes a red vertex and the second component includes blue vertices and uncolored vertices.

Here is the tree from the second example:

<image>

Every edge is nice in it.

Here is the tree from the third example:

<image>

Edge (1, 3) splits the into components \{1\} and \{3, 2\}, the latter one includes both red and blue vertex, thus the edge isn't nice. Edge (2, 3) splits the into components \{1, 3\} and \{2\}, the former one includes both red and blue vertex, thus the edge also isn't nice. So the answer is 0.
"""

# Original Problem: node_29:cc_python_29
# =========================
import sys
input=sys.stdin.readline
n = int(input())
a = [int(t) for t in input().split(' ')]
mx = [[] for _ in range(n)]
for i in range(n-1):
    v1, v2 = map(int,input().split())
    mx[v1-1].append(v2-1)
    mx[v2-1].append(v1-1)
count = [[0, 0] for _ in range(n)]
total = [a.count(1), a.count(2)]
answer = 0
OBSERVE = 0
CHECK = 1
stack = [(OBSERVE, 0, -1)]
while len(stack):
    #print(stack,count)
    state, vertex, parent = stack.pop()
    if state == OBSERVE:
        stack.append((CHECK, vertex, parent))
        for child in mx[vertex]:
            #print(nv,v,from_)
            if child != parent:
                stack.append((OBSERVE, child, vertex))
    else:
        for child in mx[vertex]:
            if child != parent:
                #print(child,parent,count)
                if count[child][0] == total[0] and count[child][1] == 0 or count[child][1] == total[1] and count[child][0] == 0:
                    answer += 1
                count[vertex][0] += count[child][0]
                count[vertex][1] += count[child][1]
 
        if a[vertex] != 0:
            #print(count)
            count[vertex][a[vertex]-1] += 1
            #print(count)
 
print(answer)


# End of all problems.
