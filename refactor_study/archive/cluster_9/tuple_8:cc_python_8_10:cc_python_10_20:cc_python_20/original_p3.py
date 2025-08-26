# Query for: node_8:cc_python_8
# =========================
"""
Logical quantifiers are very useful tools for expressing claims about a set. For this problem, let's focus on the set of real numbers specifically. The set of real numbers includes zero and negatives. There are two kinds of quantifiers: universal (∀) and existential (∃). You can read more about them here.

The universal quantifier is used to make a claim that a statement holds for all real numbers. For example:

  * ∀ x,x<100 is read as: for all real numbers x, x is less than 100. This statement is false. 
  * ∀ x,x>x-1 is read as: for all real numbers x, x is greater than x-1. This statement is true. 



The existential quantifier is used to make a claim that there exists some real number for which the statement holds. For example:

  * ∃ x,x<100 is read as: there exists a real number x such that x is less than 100. This statement is true. 
  * ∃ x,x>x-1 is read as: there exists a real number x such that x is greater than x-1. This statement is true. 



Moreover, these quantifiers can be nested. For example:

  * ∀ x,∃ y,x<y is read as: for all real numbers x, there exists a real number y such that x is less than y. This statement is true since for every x, there exists y=x+1. 
  * ∃ y,∀ x,x<y is read as: there exists a real number y such that for all real numbers x, x is less than y. This statement is false because it claims that there is a maximum real number: a number y larger than every x. 



Note that the order of variables and quantifiers is important for the meaning and veracity of a statement.

There are n variables x_1,x_2,…,x_n, and you are given some formula of the form $$$ f(x_1,...,x_n):=(x_{j_1}<x_{k_1})∧ (x_{j_2}<x_{k_2})∧ ⋅⋅⋅∧ (x_{j_m}<x_{k_m}), $$$

where ∧ denotes logical AND. That is, f(x_1,…, x_n) is true if every inequality x_{j_i}<x_{k_i} holds. Otherwise, if at least one inequality does not hold, then f(x_1,…,x_n) is false.

Your task is to assign quantifiers Q_1,…,Q_n to either universal (∀) or existential (∃) so that the statement $$$ Q_1 x_1, Q_2 x_2, …, Q_n x_n, f(x_1,…, x_n) $$$

is true, and the number of universal quantifiers is maximized, or determine that the statement is false for every possible assignment of quantifiers.

Note that the order the variables appear in the statement is fixed. For example, if f(x_1,x_2):=(x_1<x_2) then you are not allowed to make x_2 appear first and use the statement ∀ x_2,∃ x_1, x_1<x_2. If you assign Q_1=∃ and Q_2=∀, it will only be interpreted as ∃ x_1,∀ x_2,x_1<x_2.

Input

The first line contains two integers n and m (2≤ n≤ 2⋅ 10^5; 1≤ m≤ 2⋅ 10^5) — the number of variables and the number of inequalities in the formula, respectively.

The next m lines describe the formula. The i-th of these lines contains two integers j_i,k_i (1≤ j_i,k_i≤ n, j_i≠ k_i).

Output

If there is no assignment of quantifiers for which the statement is true, output a single integer -1.

Otherwise, on the first line output an integer, the maximum possible number of universal quantifiers.

On the next line, output a string of length n, where the i-th character is "A" if Q_i should be a universal quantifier (∀), or "E" if Q_i should be an existential quantifier (∃). All letters should be upper-case. If there are multiple solutions where the number of universal quantifiers is maximum, print any.

Examples

Input


2 1
1 2


Output


1
AE


Input


4 3
1 2
2 3
3 1


Output


-1


Input


3 2
1 3
2 3


Output


2
AAE

Note

For the first test, the statement ∀ x_1, ∃ x_2, x_1<x_2 is true. Answers of "EA" and "AA" give false statements. The answer "EE" gives a true statement, but the number of universal quantifiers in this string is less than in our answer.

For the second test, we can show that no assignment of quantifiers, for which the statement is true exists.

For the third test, the statement ∀ x_1, ∀ x_2, ∃ x_3, (x_1<x_3)∧ (x_2<x_3) is true: We can set x_3=max\\{x_1,x_2\}+1.
"""

# Original Problem: node_8:cc_python_8
# =========================
import sys
input = sys.stdin.readline

############ ---- Input Functions ---- ############
def inp():
    return(int(input()))
def inlt():
    return(list(map(int,input().split())))
def insr():
    s = input().strip()
    return(list(s[:len(s)]))
def invr():
    return(map(int,input().split()))



def from_file(f):
    return f.readline


def build_graph(n, A, reversed=False):
    edges = [[] for _ in range(n)]
    for i, j in A:
        i -= 1
        j -= 1
        if reversed:
            j, i = i, j
        edges[i].append(j)
    return edges


def fill_min(s, edges, visited_dfs, visited, container):
    visited[s] = True
    visited_dfs.add(s)

    for c in edges[s]:
        if c in visited_dfs:
            # cycle
            return -1
        if not visited[c]:
            res = fill_min(c, edges, visited_dfs, visited, container)
            if res == -1:
                return -1
        container[s] = min(container[s], container[c])
    visited_dfs.remove(s)
    return 0


def dfs(s, edges,  visited, container):

    stack = [s]

    colors = {s: 0}

    while stack:
        v = stack.pop()
        if colors[v] == 0:
            colors[v] = 1
            stack.append(v)
        else:
            # all children are visited
            tmp = [container[c] for c in edges[v]]
            if tmp:
                container[v] = min(min(tmp), container[v])
            colors[v] = 2 # finished
            visited[v] = True

        for c in edges[v]:
            if visited[c]:
                continue
            if c not in colors:
                colors[c] = 0 # white
                stack.append(c)
            elif colors[c] == 1:
                # grey
                return -1
    return 0





def iterate_topologically(n, edges, container):
    visited = [False] * n

    for s in range(n):
        if not visited[s]:
            # visited_dfs = set()
            # res = fill_min(s, edges, visited_dfs, visited, container)
            res = dfs(s, edges, visited, container)
            if res == -1:
                return -1
    return 0


def solve(n, A):
    edges = build_graph(n, A, False)
    container_forward = list(range(n))
    container_backward = list(range(n))

    res = iterate_topologically(n, edges, container_forward)
    if res == -1:
        return None

    edges = build_graph(n, A, True)

    iterate_topologically(n, edges, container_backward)
    container = [min(i,j) for i,j in zip(container_forward, container_backward)]

    res = sum((1 if container[i] == i else 0 for i in range(n)))

    s = "".join(["A" if container[i] == i else "E" for i in range(n)])

    return res, s



# with open('5.txt') as f:
#     input = from_file(f)
n, m = invr()
A = []
for _ in range(m):
    i, j = invr()
    A.append((i, j))

result = solve(n, A)
if not result:
    print (-1)
else:
    print(f"{result[0]}")
    print(f"{result[1]}")


# End of all problems.