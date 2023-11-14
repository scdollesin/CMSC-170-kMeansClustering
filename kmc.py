import random

def selectAttribute(attributes):
    for i in range(len(attributes)):
        print(f"[{i}] {attributes[i]}")
    choice = int(input("Select an attribute: "))
    return choice

def getData(file):
    dataset = file.read().split("\n")
    for i in range(len(dataset)):
        dataset[i] = dataset[i].split(",")
        for j in range(len(dataset[1])):
            if (i>0):
                dataset[i][j] = float(dataset[i][j])
        #print(dataset[i])
    attributes = dataset.pop(0)   #separate the attributes from the actual data
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
    k = int(input("Enter value of k: "))
    
    #determine centroids from the dataset randomly
    centroids = []
    for i in range(k):
        c = []
        print(len(dataset))
        r = random.randint(1, (len(dataset)-1))
        c.append(dataset[r][att1])
        c.append(dataset[r][att2])
        print(f"centroid {i}: {c[0]}, {c[1]} [{r}]")
        centroids.append(c)
    
    