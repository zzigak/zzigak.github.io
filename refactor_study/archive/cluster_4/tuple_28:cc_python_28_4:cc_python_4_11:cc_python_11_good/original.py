# This file contains original problem queries and their corresponding Python code.

# Query for: node_11:cc_python_11
# =========================
"""
The Olympic Games in Bercouver are in full swing now. Here everyone has their own objectives: sportsmen compete for medals, and sport commentators compete for more convenient positions to give a running commentary. Today the main sport events take place at three round stadiums, and the commentator's objective is to choose the best point of observation, that is to say the point from where all the three stadiums can be observed. As all the sport competitions are of the same importance, the stadiums should be observed at the same angle. If the number of points meeting the conditions is more than one, the point with the maximum angle of observation is prefered. 

Would you, please, help the famous Berland commentator G. Berniev to find the best point of observation. It should be noted, that the stadiums do not hide each other, the commentator can easily see one stadium through the other.

Input

The input data consists of three lines, each of them describes the position of one stadium. The lines have the format x, y, r, where (x, y) are the coordinates of the stadium's center ( - 103 ≤ x, y ≤ 103), and r (1 ≤ r ≤ 103) is its radius. All the numbers in the input data are integer, stadiums do not have common points, and their centers are not on the same line. 

Output

Print the coordinates of the required point with five digits after the decimal point. If there is no answer meeting the conditions, the program shouldn't print anything. The output data should be left blank.

Examples

Input

0 0 10
60 0 10
30 30 10


Output

30.00000 0.00000
"""

# Original Problem: node_11:cc_python_11
# =========================
import math

x1, y1, r1 = [int(_) for _ in input().split()]
x2, y2, r2 = [int(_) for _ in input().split()]
x3, y3, r3 = [int(_) for _ in input().split()]


def get_line(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    if x1 * y2 == x2 * y1:
        c = 0
        a = 1
        if y1 != 0:
            b = -x1 / y1
        elif y2 != 0:
            b = -x2 / y2
        else:
            a = 0
            b = 1
        return a, b, c
    else:
        c = 1
        a = (y1 - y2) / (x1 * y2 - x2 * y1)
        b = (x1 - x2) / (x2 * y1 - x1 * y2)
        return a, b, c


def comm(x1, y1, r1, x2, y2, r2):
    if r1 == r2:
        a, b, c = get_line((x1, y1), (x2, y2))
        return True, b, -a, a * (y1 + y2) / 2 - b * (x1 + x2) / 2
    else:
        c = r1 ** 2 / r2 ** 2
        x = (c * x2 - x1) / (c - 1)
        y = (c * y2 - y1) / (c - 1)
        r = math.sqrt((c * (x1 - x2) ** 2 + c * (y1 - y2) ** 2) / (c - 1) ** 2)
        return False, x, y, r


def get_angle(x, y, r, x0, y0):
    # print(x, y, r, x0, y0)
    dist = math.sqrt((x0 - x) ** 2 + (y0 - y) ** 2)
    # print("DIST: ", dist)
    # print("DIST: ", r / dist)
    return math.asin(r / dist)


def get_points(a, b, c, x, y, r):
    dist = abs(a * x + b * y + c) / math.sqrt(a ** 2 + b ** 2)
    if dist <= r:
        aa = (a ** 2 + b ** 2)
        bb = 2 * a * b * y + 2 * a * c - 2 * b ** 2 * x
        cc = b ** 2 * x ** 2 + (b * y + c) ** 2 - b ** 2 * r ** 2
        delta = math.sqrt(bb ** 2 - 4 * aa * cc)
        if delta == 0:
            xx = -bb / 2 / aa
            if b == 0:
                yy = math.sqrt(r ** 2 - (xx - x) ** 2) + y
            else:
                yy = (-c - a * xx) / b
            return 1, [(xx, yy)]
        else:
            xx1 = (-bb + delta) / 2 / aa
            if b == 0:
                tmp1 = math.sqrt(r ** 2 - (xx1 - x) ** 2) + y
                tmp2 = -math.sqrt(r ** 2 - (xx1 - x) ** 2) + y
                yy1 = 0
                if abs(a * xx1 + b * tmp1 + c) <= 0.001:
                    yy1 = tmp1
                if abs(a * xx1 + b * tmp2 + c) <= 0.001:
                    yy1 = tmp2
            else:
                yy1 = (-c - a * xx1) / b
            xx2 = (-bb - delta) / 2 / aa
            if b == 0:
                tmp1 = math.sqrt(r ** 2 - (xx2 - x) ** 2) + y
                tmp2 = -math.sqrt(r ** 2 - (xx2 - x) ** 2) + y
                yy2 = 0
                if abs(a * xx2 + b * tmp1 + c) <= 0.001:
                    yy2 = tmp1
                if abs(a * xx2 + b * tmp2 + c) <= 0.001:
                    yy2 = tmp2
            else:
                yy2 = (-c - a * xx2) / b
            return 2, [(xx1, yy1), (xx2, yy2)]
    return 0, []


items1 = comm(x1, y1, r1, x2, y2, r2)
items2 = comm(x1, y1, r1, x3, y3, r3)

# print(items1)
# print(items2)

if not items1[0]:
    items1, items2 = items2, items1

if items1[0] and items2[0]:
    a1, b1, c1 = items1[1:]
    a2, b2, c2 = items2[1:]
    if a1 * b2 != a2 * b1:
        print((b1 * c2 - b2 * c1) / (b2 * a1 - a2 * b1), (a1 * c2 - a2 * c1) / (a2 * b1 - a1 * b2))
elif items1[0] and not items2[0]:
    a, b, c = items1[1:]
    x, y, r = items2[1:]
    num, points = get_points(a, b, c, x, y, r)
    # print(num, points)
    if num == 1:
        print(points[0][0], points[0][1])
    elif num == 2:
        xx1, yy1 = points[0]
        xx2, yy2 = points[1]
        angle1 = get_angle(x1, y1, r1, xx1, yy1)
        angle2 = get_angle(x1, y1, r1, xx2, yy2)
        # print(angle1, angle2)
        if angle1 >= angle2:
            print(xx1, yy1)
        else:
            print(xx2, yy2)
else:
    xx1, yy1, rr1 = items1[1:]
    xx2, yy2, rr2 = items2[1:]
    a, b, c = 2 * (xx1 - xx2), 2 * (yy1 - yy2), (xx2 ** 2 + yy2 ** 2 - rr2 ** 2) - (xx1 ** 2 + yy1 ** 2 - rr1 ** 2)
    num, points = get_points(a, b, c, xx1, yy1, rr1)
    # print(num, points)
    if num == 1:
        print(points[0][0], points[0][1])
    elif num == 2:
        xxx1, yyy1 = points[0]
        xxx2, yyy2 = points[1]
        angle1 = get_angle(x1, y1, r1, xxx1, yyy1)
        angle2 = get_angle(x1, y1, r1, xxx2, yyy2)
        if angle1 >= angle2:
            print(xxx1, yyy1)
        else:
            print(xxx2, yyy2)


# EoP (End of Problem details for node_11:cc_python_11)
# ######################################################################

# Query for: node_28:cc_python_28
# =========================
"""
This problem is same as the previous one, but has larger constraints.

It was a Sunday morning when the three friends Selena, Shiro and Katie decided to have a trip to the nearby power station (do not try this at home). After arriving at the power station, the cats got impressed with a large power transmission system consisting of many chimneys, electric poles, and wires. Since they are cats, they found those things gigantic.

At the entrance of the station, there is a map describing the complicated wiring system. Selena is the best at math among three friends. He decided to draw the map on the Cartesian plane. Each pole is now a point at some coordinates (x_i, y_i). Since every pole is different, all of the points representing these poles are distinct. Also, every two poles are connected with each other by wires. A wire is a straight line on the plane infinite in both directions. If there are more than two poles lying on the same line, they are connected by a single common wire.

Selena thinks, that whenever two different electric wires intersect, they may interfere with each other and cause damage. So he wonders, how many pairs are intersecting? Could you help him with this problem?

Input

The first line contains a single integer n (2 ≤ n ≤ 1000) — the number of electric poles.

Each of the following n lines contains two integers x_i, y_i (-10^4 ≤ x_i, y_i ≤ 10^4) — the coordinates of the poles.

It is guaranteed that all of these n points are distinct.

Output

Print a single integer — the number of pairs of wires that are intersecting.

Examples

Input


4
0 0
1 1
0 3
1 2


Output


14


Input


4
0 0
0 2
0 4
2 0


Output


6


Input


3
-1 -1
1 0
3 1


Output


0

Note

In the first example:

<image>

In the second example:

<image>

Note that the three poles (0, 0), (0, 2) and (0, 4) are connected by a single wire.

In the third example:

<image>
"""

# Original Problem: node_28:cc_python_28
# =========================
from itertools import combinations

n = int(input())

points = []
for _ in range(n):
    x, y = map(int, input().split(' '))
    points.append((x, y))

directions = {}
for pair in combinations(points, 2):
    (x1, y1), (x2, y2) = pair
    if x1 == x2:
        dir = (0, 1)
        b = x1
    else:
        dir = (1, (y2 - y1) / (x2 - x1))
        b = (y2 * x1 - x2 * y1) / (x1 - x2)

    if dir in directions:
        directions[dir].add(b)
    else:
        directions[dir] = set([b])

total_lines = sum(len(value) for key, value in directions.items())

result = 0
for key, value in directions.items():
    current = len(value)
    result += (total_lines - current) * current

print(int(result / 2))


# EoP (End of Problem details for node_28:cc_python_28)
# ######################################################################

# Query for: node_4:cc_python_4
# =========================
"""
This problem is same as the next one, but has smaller constraints.

It was a Sunday morning when the three friends Selena, Shiro and Katie decided to have a trip to the nearby power station (do not try this at home). After arriving at the power station, the cats got impressed with a large power transmission system consisting of many chimneys, electric poles, and wires. Since they are cats, they found those things gigantic.

At the entrance of the station, there is a map describing the complicated wiring system. Selena is the best at math among three friends. He decided to draw the map on the Cartesian plane. Each pole is now a point at some coordinates (x_i, y_i). Since every pole is different, all of the points representing these poles are distinct. Also, every two poles are connected with each other by wires. A wire is a straight line on the plane infinite in both directions. If there are more than two poles lying on the same line, they are connected by a single common wire.

Selena thinks, that whenever two different electric wires intersect, they may interfere with each other and cause damage. So he wonders, how many pairs are intersecting? Could you help him with this problem?

Input

The first line contains a single integer n (2 ≤ n ≤ 50) — the number of electric poles.

Each of the following n lines contains two integers x_i, y_i (-10^4 ≤ x_i, y_i ≤ 10^4) — the coordinates of the poles.

It is guaranteed that all of these n points are distinct.

Output

Print a single integer — the number of pairs of wires that are intersecting.

Examples

Input


4
0 0
1 1
0 3
1 2


Output


14


Input


4
0 0
0 2
0 4
2 0


Output


6


Input


3
-1 -1
1 0
3 1


Output


0

Note

In the first example:

<image>

In the second example:

<image>

Note that the three poles (0, 0), (0, 2) and (0, 4) are connected by a single wire.

In the third example:

<image>
"""

# Original Problem: node_4:cc_python_4
# =========================
import sys
import collections
import math
import heapq
from operator import itemgetter

def getint():
    return int(input())

def getints():
    return [int(x) for x in input().split(' ')]

n = getint()
points = [tuple(getints()) for _ in range(n)]
result = 0

slopes = collections.defaultdict(set)
for i in range(n - 1):
    for j in range(i + 1, n):
        x1, y1, x2, y2 = points[i][0], points[i][1], points[j][0], points[j][1]
        a, b = y1 - y2, x1 - x2

        d = math.gcd(a, b)
        a, b = a // d, b // d
        if a < 0 or (a == 0 and b < 0):
            a, b = -a, -b
        
        c = a * x1 - b * y1
        slope = (a, b)
        slopes[slope].add(c)

slopeGroups = [(ab[0], ab[1], len(cs)) for ab, cs in slopes.items()]
m = len(slopeGroups)

for i in range(m - 1):
    intersects = 0
    for j in range(i + 1, m):
        intersects += slopeGroups[j][2]
    result += slopeGroups[i][2] * intersects

print(str(result))


# End of all problems.
