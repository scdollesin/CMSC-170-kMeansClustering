import math
import random
import matplotlib.pyplot as plt
from tkinter import *
import time

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

    #set window properties
    window = Tk()
    window.geometry("1080x720")
    att1_label = Label(window, text = "Attribute 1").pack()
    att1_str = StringVar(window)
    att1_str.set(attributes[0]) # default value
    att1 = 0
    att1_menu = OptionMenu(window, att1_str, *attributes)
    att1_menu.pack()

    att2_label = Label(window, text = "Attribute 2").pack()
    att2_str = StringVar(window)
    att2_str.set(attributes[1]) # default value
    att2 = 1
    att2_menu = OptionMenu(window, att2_str, *attributes)
    att2_menu.pack()
    
    k_label = Label(window, text = "k").pack()
    k_str = StringVar(window)
    k_str.set(1) # default value
    k = 1
    k_menu = OptionMenu(window, k_str, *[1,2,3,4,5,6,7,8,9,50])
    k_menu.pack()
    
    def run():
        global att1
        global att2
        global k
        att1 = attributes.index(att1_str.get())
        att2 = attributes.index(att2_str.get())
        k = int(k_str.get())
        print ("att1:", att1)
        print ("att2:", att2)
        print ("k:", k)


    button = Button(window, text="RUN", command=run)
    button.pack()

    window.mainloop()

    #ask for 1st and 2nd attribute and the value of k
    #att1 = selectAttribute(attributes)
    #att2 = selectAttribute(attributes)
    #k = getK()

    #determine k centroids from the dataset
    centroids = []
    new_centroids = []
    clusters = []
    selected = []
    for i in range(k):
        c = []
        
        #make sure no centroids are the same
        while 1:
            r = random.randint(1, (len(dataset) - 1))
            if (r not in selected):
                selected.append(r)
                break

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

        #print(">>>> CLUSTERS")
        #for x in clusters:
        #    print(x)
        #    print()
        
        #compute for the new centroids
        for i in range(len(new_centroids)):
            new_centroids[i].append((sum([point[0] for point in clusters[i]]))/len(clusters[i]))       #average of the x values
            new_centroids[i].append((sum([point[1] for point in clusters[i]]))/len(clusters[i]))       #average of the y values
        
        #print(">>>> OLD")
        #for x in centroids:
        #    print(x)
        #print(">>>> NEW")
        #for x in new_centroids:
        #    print(x)
        print("EQUAL? ", centroids==new_centroids)

        #if the new centroids are not the same as the previous centroids, replace the old centroids with the newly computed ones
        if (centroids!=new_centroids):
            for i in range(k):
                centroids[i] = new_centroids[i].copy()
                new_centroids[i].clear()                #empty out new_centroids and clusters lists
                clusters[i].clear()
        else: 
            break   #otherwise, stop iterating

    plt.show()