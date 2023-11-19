# EXERCISE #8 K-MEANS CLUSTERING
# AUTHOR: Samantha Shane C. Dollesin
# STUDENT NO.: 2020-01893
# SECTION: WX-1L
# PROGRAM DESCRIPTION: This program takes a csv file containing data points and performs k-means clustering
#                      given two attributes and a k value (from the user via the GUI) and displays a scatter plot

import math
import random
import matplotlib.pyplot
from tkinter import *
import tkinter as tk
import tkinter.scrolledtext as st 
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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
    window.geometry("750x452")
    window.config(bg = "white")
    window.title("KMeans Clustering")

    frame1 = Frame(window, padx= 20, pady=20, height=452)
    frame1.grid(column=0, row=0, sticky="nswe")

    #attribute 1
    att1_label = Label(frame1, text = "Attribute 1", anchor="w", justify="left").grid(column=0, row=0, sticky="w")
    att1_str = StringVar(frame1)
    att1_str.set(attributes[0]) # default value
    att1 = 0
    att1_menu = OptionMenu(frame1, att1_str, *attributes)
    att1_menu.config(width=15)
    att1_menu.grid_propagate(0)
    att1_menu.grid(column=1, row=0)
    #attribute 2
    att2_label = Label(frame1, text = "Attribute 2", anchor="w", justify="left").grid(column=0, row=1, sticky="w")
    att2_str = StringVar(frame1)
    att2_str.set(attributes[1]) # default value
    att2 = 1
    att2_menu = OptionMenu(frame1, att2_str, *attributes)
    att2_menu.config(width=15)
    att2_menu.grid_propagate(0)
    att2_menu.grid(column=1, row=1)
    #value for k
    k_label = Label(frame1, text = "k Value", anchor="w", justify="left").grid(column=0, row=2, sticky="w")
    k_str = StringVar(frame1)
    k_str.set(3) # default value
    k = 1
    k_menu = OptionMenu(frame1, k_str, *[1,2,3,4,5,6,7,8,9,10])
    k_menu.config(width=15)
    k_menu.grid_propagate(0)
    k_menu.grid(column=1, row=2)

    frame2 = Frame(window, height=452, bg= "white")
    frame2.grid(column=1, row=0, sticky="nswe")

    #get values for 1st and 2nd attribute and k when run button is pressed then proceed to computation
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
        output = open("output.csv", "w")
        output_disp = ""
        for i in range(len(centroids)):
            output.write(f"Centroid {i}: {centroids[i]}\n")
            output_disp = output_disp + f"Centroid {i}: {centroids[i]}" + "\n"
            for j in range(len(clusters[i])):
                output.write(f"{clusters[i][j]}\n")
                output_disp = output_disp + f"{clusters[i][j]}\n"
            output.write("\n")
            output_disp = output_disp + "\n"

        #display in text area
        text_area.delete('1.0', END)
        text_area.insert(tk.INSERT, output_disp) 

    #create run button
    button = Button(frame1, text="RUN", command=run, width=10)
    button.grid(column=0, row=3, sticky="w")

    #set text area properties
    txtarea_label = Label(frame1, text = "Centoids & Clusters          ", anchor="e", justify="right").grid(column=1, row=4, sticky="e")
    text_area = st.ScrolledText(frame1, width = 32, height = 17, font = ("Consolas", 10))
    text_area.grid(column = 0, pady = 10, padx = 10, columnspan=2)

    window.mainloop()