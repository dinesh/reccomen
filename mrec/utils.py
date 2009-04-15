import math

def getDistance(a, b):
    # Forbid measurements between Points in different spaces
    n = len(a)
    if len(a) != len(b): raise Exception("ILLEGAL: NON-COMPARABLE POINTS")
    # Euclidean distance between a and b is sqrt(sum((a[i]-b[i])^2) for all i)
    ret = 0.0
    for i in range(n):
        ret = ret+pow((a[i]-b[i]), 2)
    return math.sqrt(ret)
# -- Create a random Point in n-dimensional space

def makeRandomPoint(n, lower, upper):
    coords = []
    for i in range(n): coords.append(random.uniform(lower, upper))
    return Point(coords)

     
def exclude(list1,list2):
    final = []
    for l in list1:
        if l not in list2:
            final.append(l)
    return final

if __name__ == "__main__":
    print exclude([1,2,3,4,5,6],[1,2,3])