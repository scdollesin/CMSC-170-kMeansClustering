import math
import random
import matplotlib.pyplot as plt
from tkinter import *
import time
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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
    attributes = dataset.pop(0)  #separate the attributes from the actual data

    return attributes, dataset

inputcsv = open("08 Data Wine.csv")
if (inputcsv.readable()):
    #read input file
    attributes, dataset = getData(inputcsv)

    #set window properties
    window = Tk()
    window.geometry("680x452")
    window.config(bg = "white")

    frame1 = Frame(window, padx= 20, pady=20, height=452)
    frame1.grid(column=0, row=0, sticky="nswe")

    att1_label = Label(frame1, text = "Attribute 1", anchor="w", justify="left").grid(column=0, row=0)
    att1_str = StringVar(frame1)
    att1_str.set(attributes[0]) # default value
    att1 = 0
    att1_menu = OptionMenu(frame1, att1_str, *attributes)
    att1_menu.config(width=15)
    att1_menu.grid_propagate(0)
    att1_menu.grid(column=1, row=0)

    att2_label = Label(frame1, text = "Attribute 2", anchor="w", justify="left").grid(column=0, row=1)
    att2_str = StringVar(frame1)
    att2_str.set(attributes[1]) # default value
    att2 = 1
    att2_menu = OptionMenu(frame1, att2_str, *attributes)
    att2_menu.config(width=15)
    att2_menu.grid_propagate(0)
    att2_menu.grid(column=1, row=1)
    
    k_label = Label(frame1, text = "k Value", anchor="w", justify="left").grid(column=0, row=2)
    k_str = StringVar(frame1)
    k_str.set(1) # default value
    k = 1
    k_menu = OptionMenu(frame1, k_str, *[1,2,3,4,5,6,7,8,9,10])
    k_menu.config(width=15)
    k_menu.grid_propagate(0)
    k_menu.grid(column=1, row=2)

    frame2 = Frame(window, height=452, bg= "white")
    frame2.grid(column=1, row=0, sticky="nswe")
    
    #get values for 1st and 2nd attribute and k
    def run():
        global att1
        global att2
        global k
        att1 = attributes.index(att1_str.get())
        att2 = attributes.index(att2_str.get())
        k = int(k_str.get())

        #determine k centroids from the dataset
        centroids = []
        new_centroids = []
        clusters = []
        selected = []
        print("initial centroids: ")
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
            #print("EQUAL? ", centroids==new_centroids)

            #if the new centroids are not the same as the previous centroids, replace the old centroids with the newly computed ones
            if (centroids!=new_centroids):
                for i in range(k):
                    centroids[i] = new_centroids[i].copy()
                    new_centroids[i].clear()                #empty out new_centroids and clusters lists
                    clusters[i].clear()
            else: 
                break   #otherwise, stop iterating

        #create figure containing the plot
        fig = Figure(figsize = (4.5, 4.5), dpi = 100) 
        plot1 = fig.add_subplot(111) 

        #plot each cluster
        for c in clusters:
            plot1.scatter([point[0] for point in c],[point[1] for point in c])
        plot1.set_xlabel(attributes[att1])
        plot1.set_ylabel(attributes[att2])

        #embed the figure onto the window
        canvas = FigureCanvasTkAgg(fig, master = frame2)   
        canvas.draw()
        canvas.get_tk_widget().grid(column=0, row=0)

        #export to output file
        output = open("output.txt", "w")
        output_disp = ""
        for i in range(len(centroids)):
            output.write(f"Centroid {i}: {centroids[i]}\n")
            output_disp = output_disp + f"Centroid {i}: {centroids[i]}" + "\n"
            for j in range(len(clusters[i])):
                output.write(f"{clusters[i][j]}\n")
                output_disp = output_disp + f"{clusters[i][j]}\n"
            output.write("\n")
            output_disp = output_disp + "\n"

        output_label = Label(frame1, text=output_disp, anchor="w", justify="left")
        output_label.grid(column=0, row=5)

    button = Button(frame1, text="RUN", command=run)
    button.grid(column=0, row=4, columnspan=2)

    window.mainloop()