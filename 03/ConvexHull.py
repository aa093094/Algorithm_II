import math
import timeit
import random


# Given a list of points (x, y)
#   find the convex hull using Graham's Scan
# Return a list of points in the convex hull in ccw order
def grahamScan(points):
    results = sorted(points, key = lambda p:(p[1], p[0]))
    for i in range(len(results) - 1):
        if (results[i][1] == results[i + 1][1] and results[i][0] < results[i + 1][0]):
            continue
        else:
            start = results[i]
            break

    angleOrder = []
    for j, point in enumerate(points):
        if point == start:
            startPoint = j
        else:
            angle = math.atan2(point[1] - start[1], point[0] - start[0])
            angleOrder.append((j, angle))
    angleOrder.sort(key = lambda p:(p[1], p[0]))
    
    def angleTest(i, j, k):
        if ((j[0] - i[0]) * (k[1] - i[1]) - (j[1] - i[1]) * (k[0] - i[0]) > 0):
            return True        
        else:
            return False
    
    stack = []
    stack.append(points[startPoint])
    p = stack[0]
    test = True
    for k, value in enumerate(angleOrder):
        if k == 0:
            stack.append(points[value[0]])
            q = stack[1]
        else:
            r = points[value[0]]
            test = angleTest(p, q, r)
            if (test == True):
                stack.append(r)
                p, q = q, r
            else:
                while (test == False):
                    stack.pop()
                    q = p
                    p = stack[len(stack) - 2]
                    test = angleTest(p, q, r)
                stack.append(r)
                p, q = q, r


    r = stack[0]
    test = angleTest(p, q, r)
    while (test == False):
        stack.pop()
        q = p
        p = stack[len(stack) - 2]
        test = angleTest(p, q, r)

    return stack


def correctnessTest(input, expected_output, correct):
    output = grahamScan(input)
    print(f"grahamScan({input})\n{output}")
    if output == expected_output: print("Pass")
    else:        
        print(f"Fail - expected output: {expected_output}")
        correct = False
    print()    

    return correct


def simulateNSquare(points):    
    points = sorted(points, key = lambda p: (p[1], -p[0])) 
    result = []
    for i in range(len(points)):
        points_with_angle = []
        for j in range(i+1, len(points)):
            x, y = points[j]
            points_with_angle.append((x, y, math.atan2(y - points[i][1], x - points[i][0])))
        points_with_angle = sorted(points_with_angle, key = lambda p: p[2])


'''
Unit Test
'''
if __name__ == "__main__":
    '''# ccw turns
    print(ccw((0,0), (-1,1), (-2, -1)))
    print(ccw((-1,1), (-2, -1), (0,0)))
    print(ccw((-2, -1), (0,0), (-1,1)))

    # non-ccw turns
    print(ccw((0,0), (-2, -1), (-1,1)))
    print(ccw((-2, -1), (-1,1), (0,0)))
    print(ccw((-1,1), (0,0), (-2, -1)))
    print(ccw((0,0), (-1, 1), (-2, 2))) # Straight line'''

    print("Correctness test for grahamScan()")
    print("For each test case, if your answer does not appear within 5 seconds, then consider that you failed the case")
    print()
    correct = True
    
    input = [(3, -1), (2, -2), (4, -1)]
    expected_output = [(2, -2), (4, -1), (3, -1)]
    correct = correctnessTest(input, expected_output, correct)

    input = [(0, 0), (-2, -1), (-1, 1), (1, -1), (3, -1), (-3, -1)]
    expected_output = [(3, -1), (-1, 1), (-3, -1)]
    correct = correctnessTest(input, expected_output, correct)

    input = [(4, 2), (3, -1), (2, -2), (1, 0), (0, 2), (0, -2), (-1, 1), (-2, -1), (-2, -3), (-3, 3), (-4, 0), (-4, -2), (-4, -4)]
    expected_output = [(-4, -4), (2, -2), (3, -1), (4, 2), (-3, 3), (-4, 0)]
    correct = correctnessTest(input, expected_output, correct)

    input = [(2, 0), (2, 2), (1, -1), (0, 2), (-1, 1), (-2, -2)]
    expected_output = [(-2, -2), (1, -1), (2, 0), (2, 2), (0, 2), (-1, 1)]
    correct = correctnessTest(input, expected_output, correct)

    input = [(2, 0), (2, 2), (1, -1), (0, 2), (-1, 1), (-2, -2), (-2, 2), (4, -4)]
    expected_output = [(4, -4), (2, 2), (-2, 2), (-2, -2)]
    correct = correctnessTest(input, expected_output, correct)

    # "342235" is a 6-digit number and is greater than the other 5-digit numbers
    input = [(342235, -23412), (-74545, 72345), (25812, -45689), (-45676, 24578), (45689, 0), (-74545, 0), (0, 45689), (0, -45689)]
    expected_output = [(25812, -45689), (342235, -23412), (-74545, 72345), (-74545, 0), (0, -45689)]
    correct = correctnessTest(input, expected_output, correct)
    
    print()
    print("Speed test for grahamScan()")
    if not correct: print("Fail (since the algorithm is not correct)")
    else:
        repeat = 10
        inputLength = 100
        minC, maxC = -1000000, 1000000
        points = [(random.randint(minC, maxC), random.randint(minC, maxC)) for _ in range(inputLength)]
        tCodeToCompare = timeit.timeit(lambda: simulateNSquare(points), number=repeat) / repeat
        tSubmittedCode = timeit.timeit(lambda: grahamScan(points), number=repeat) / repeat        
        print(f"Average running time of grahamScan() and simulateNSquare() with {inputLength} points: {tSubmittedCode:.10f} and {tCodeToCompare:.10f}")                
        if tSubmittedCode < tCodeToCompare * 0.1: print("Pass")
        else:
            print("Fail")
        print()