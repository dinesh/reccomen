

def Kmean(model,playlist,cutoff,rmax):
    k = 1
    while 1:
      cls = kmean(model,playlist,k,cutoff)
      print cls
      
      p = k
      for cl in cls: 
        if cl.radius >= rmax:
          k+=1
          kmean(playlist,k,cutoff)
      if p == k : break
        
           
def kmean(model,playlist,k,cutoff):
    
    initials = random.sample(playlist.files,k)
    clusters = []
    for p in initials: 
      clusters.append(model.Cluster(playlist.id,files=[p]))
      while True:
        lists = []
        for c in clusters: list.append([])
        for p in playlist.files:
          smallest_distance = getDistance(p.vector,clusters[0].centroid)
          index = 0
          for i in range(len(clusters[1:])):
            distance = getDistance(p.vector, clusters[i+1].centroid)
            if distance < smallest_distance:
                    smallest_distance = distance
                    index = i+1
            # Add this Point to that Cluster's corresponding list
            lists[index].append(p)
        # Update each Cluster with the corresponding list
        # Record the biggest centroid shift for any Cluster
        biggest_shift = 0.0
        for i in range(len(clusters)):
            shift = clusters[i].addfiles([lists[i]])
            biggest_shift = max(biggest_shift, shift)
        # If the biggest centroid shift is less than the cutoff, stop
        if biggest_shift < cutoff: break
    # Return the list of Clusters
    for cl in clusters:
        cl.calculateRadius()
        
    return clusters
# -- Get the Euclidean distance between two Points


def getDistance(a, b):
    # Forbid measurements between Points in different spaces
  
    if a.n != b.n: raise Exception("ILLEGAL: NON-COMPARABLE POINTS")
    # Euclidean distance between a and b is sqrt(sum((a[i]-b[i])^2) for all i)
    ret = 0.0
    for i in range(a.n):
        ret = ret+pow((a.coords[i]-b.coords[i]), 2)
    return math.sqrt(ret)
# -- Create a random Point in n-dimensional space

def makeRandomPoint(n, lower, upper):
    coords = []
    for i in range(n): coords.append(random.uniform(lower, upper))
    return Point(coords)

     
    