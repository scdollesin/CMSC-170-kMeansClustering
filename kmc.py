import math
import random
import matplotlib.pyplot as plt

def selectAttribute(attributes):
    no_of_attribs = len(attributes)
    for i in range(no_of_attribs):
        print(f"[{i}] {attributes[i]}")
    choice = 1

    while (1):
        choice = int(input("Select an attribute: "))
        if (choice > (no_of_attribs - 1)) or (choice < 0):
            print("Please enter a a valid attribute")
        else:
            break

    return choice

def getK():
    k = 1
    while (1):
        k = int(input("Enter value of k: "))
        if (k > 10):
            print("10 maximum centroids allowed")
        elif (k < 1):
            print("Please enter a value greater than 0")
        else:
            break
    return k


def getData(file):
    dataset = file.read().split("\n")
    for i in range(len(dataset)):
        dataset[i] = dataset[i].split(",")
        for j in range(len(dataset[1])):
            if (i > 0):
                dataset[i][j] = float(dataset[i][j])
        #print(dataset[i])
    attributes = dataset.pop(0)  #separate the attributes from the actual data
    #print(attributes)
    #print("No. of points: ", len(dataset))

    return attributes, dataset


inputcsv = open("08 Data Wine.csv")
if (inputcsv.readable()):
    #read input file
    attributes, dataset = getData(inputcsv)
    #ask for 1st and 2nd attribute and the value of k
    att1 = selectAttribute(attributes)
    att2 = selectAttribute(attributes)
    k = getK()

    #determine k centroids from the dataset
    centroids = []
    new_centroids = []
    clusters = []
    for i in range(k):
        c = []
        r = random.randint(1, (len(dataset) - 1))
        c.append(dataset[r][att1])
        c.append(dataset[r][att2])
        print(f"centroid {i}: {c[0]}, {c[1]} [{r}]")
        centroids.append(c)
        new_centroids.append([])
        clusters.append([])

    while (1):
        #compute each data point's distance from the centroids
        for v in dataset:
            p = []
            p.append(v[att1])
            p.append(v[att2])

            #determine the cluster by searching for the smallest distance
            minDist = 999
            c = -1 #cluster number
            for i in range(len(centroids)):
                dist = math.sqrt((p[0]-centroids[i][0])**2 + (p[1]-centroids[i][1])**2)
                if (dist < minDist):
                    minDist = dist
                    c= i
            #append the point to the list of the cluster to which it belongs
            clusters[c].append(p)

        #plot each cluster
        for c in clusters:
            plt.scatter([point[0] for point in c],[point[1] for point in c])
        plt.xlabel(attributes[att1])
        plt.ylabel(attributes[att2])
        
        #compute for the new centroids
        for i in range(len(new_centroids)):
            new_centroids[i].append((sum([point[0] for point in clusters[i]]))/len(clusters[i]))       #average of the x values
            new_centroids[i].append((sum([point[1] for point in clusters[i]]))/len(clusters[i]))       #average of the y values
        
        print(">>>> OLD")
        for x in centroids:
            print(x)
        print(">>>> NEW")
        for x in new_centroids:
            print(x)
        print("EQUAL? ", centroids==new_centroids)
        print(">>>> CLUSTERS")
        for x in clusters:
            print(x)
            print()

        #if the new centroids are not the same as the previous centroids, replace the old centroids with the newly computed ones
        if (centroids!=new_centroids):
            for i in range(k):
                centroids[i] = new_centroids[i].copy()
                new_centroids[i].clear()                #empty out new_centroids and clusters lists
                clusters[i].clear()
        else: 
            break   #otherwise, stop iterating
            
    plt.show()