from codebank import *

def main():
    n = int(input())
    a = read_ints()
    # build reversed graph: for each move i->j, add edge j->i
    neighbors = [[] for _ in range(n)]
    for i, val in enumerate(a):
        for j in (i - val, i + val):
            if 0 <= j < n:
                neighbors[j].append(i)
    # BFS from all even and all odd positions separately
    even_sources = [i for i, val in enumerate(a) if val % 2 == 0]
    odd_sources  = [i for i, val in enumerate(a) if val % 2 == 1]
    dist_even = multi_source_bfs(neighbors, even_sources)
    dist_odd  = multi_source_bfs(neighbors, odd_sources)
    # for odd a[i], answer is dist to nearest even => dist_even; else dist_odd
    ans = [dist_even[i] if a[i] % 2 == 1 else dist_odd[i] for i in range(n)]
    print(*ans)

if __name__ == "__main__":
    main()