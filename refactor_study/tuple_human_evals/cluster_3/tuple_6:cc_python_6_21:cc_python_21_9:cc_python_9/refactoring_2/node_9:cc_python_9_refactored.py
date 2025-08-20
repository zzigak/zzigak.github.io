from codebank import *
from fractions import Fraction

def main():
    n = int(input())
    adj = read_tree(n)
    par, order = postorder(adj, 0)
    children = get_children(par)
    F = [0]*n
    H = [0]*n
    ratios = [[] for _ in range(n)]
    for u in order:
        F[u] = 1
        ratios[u] = []
        for v in children[u]:
            F[u] *= H[v]
            ratios[u].append(Fraction(F[v], H[v]))
        # compute H[u]
        rl = sorted(ratios[u], reverse=True)
        ans = F[u]
        pd = Fraction(1,1)
        s = 0
        for x in rl:
            pd *= x; s += 1
            ans = max(ans, int(pd * F[u]) * (s+1))
        for v in children[u]:
            rl2 = sorted(ratios[v], reverse=True)
            pd2 = Fraction(1,1)
            s2 = 0
            for x in rl2:
                pd2 *= x; s2 += 1
                val = (int(pd2 * F[u] * F[v]) // H[v]) * (s2+2)
                ans = max(ans, val)
        H[u] = ans
    print(H[0])

if __name__ == "__main__":
    main()