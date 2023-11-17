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
    while(1):
        #compute each data point's distance from the centroids
        for v in dataset:
            p = []
            p.append(v[att1])
            p.append(v[att2])
            #print(p)

            minDist = 999
            c = -1 #cluster number
            for i in range(len(centroids)):
                dist = math.sqrt((p[0]-centroids[i][0])**2 + (p[1]-centroids[i][1])**2)
                #print(dist)
                if (dist < minDist):
                    minDist = dist
                    c= i
            #print("cluster: " , c, "\n\n\n")
            clusters[c].append(p)

        for c in clusters:
            #print(c)
            #print()
            plt.scatter([point[0] for point in c],[point[1] for point in c])

        plt.xlabel(attributes[att1])
        plt.ylabel(attributes[att2])
        
        for i in range(len(new_centroids)):
            new_centroids[i].append((sum([point[0] for point in clusters[i]]))/len(clusters[i]))
            new_centroids[i].append((sum([point[1] for point in clusters[i]]))/len(clusters[i]))

        print("old: ", end='')
        print(centroids)
        print("new: ", end='')
        print(new_centroids)
        if (new_centroids == centroids):
            print("done.")
            break
        else:
            print("iterating again...")
            centroids = new_centroids.copy()

    plt.show()