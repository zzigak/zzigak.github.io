from codebank import *
from fractions import Fraction

def main():
    n = int(input())
    adj = read_tree(n)
    par, order = parorder(adj, 0)
    children = get_children(par)
    H = [0]*n
    F = [0]*n
    FoH = [None]*n
    for u in reversed(order):
        ch = children[u]
        F_u = 1
        ratios = []
        for v in ch:
            F_u *= H[v]
            ratios.append(Fraction(F[v], H[v]))
        ans = F_u
        ratios.sort(reverse=True)
        pd = 1
        for i, r in enumerate(ratios, 1):
            pd *= r
            ans = max(ans, int(pd * F_u) * (i+1))
        for v in ch:
            pd = 1
            for i, r in enumerate(FoH[v], 1):
                pd *= r
                comp = F_u * F[v] // H[v]
                ans = max(ans, int(pd * comp) * (i+2))
        F[u] = F_u
        FoH[u] = ratios
        H[u] = ans
    print(H[0])

if __name__ == "__main__":
    main()