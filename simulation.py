import sys
import matplotlib
matplotlib.use('Qt5Agg')

from PyQt5 import QtCore, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
import numpy as np
from PyQt5.QtWidgets import *





class MplCanvas(FigureCanvasQTAgg):

    def __init__(self,size , floor , dpi=100):

        self.colors = ["red" , "green" , "blue" ,"yellow"]
        fig = Figure(figsize=(size,size), dpi=dpi)
        self.axes = fig.add_subplot(111,projection = '3d')
        super(MplCanvas, self).__init__(fig)
        self.axes.set_zlim(0,5)
        self.axes.set_xlim(-floor,floor)
        self.axes.set_ylim(-floor,floor)
        
        self.vertices = []




    def ClearGraph(self):
        for i in self.vertices:
            try:
                i.remove()
            except :
                pass

    
        


    def CalculateAllLines(self,groups , aktif):


        
        self.ClearGraph() 
        if aktif == False or len(groups) == 0:
            return
           
        i = 0
        for group in groups:
            
            points = np.array(self.CalculateLine(group))
            vertices = []
            for i in range(len(points)):
                vertices.append([points[i],points[(i+1)%len(points)],points[i]])
            

            self.vertices.append(self.axes.scatter3D(points[:, 0], points[:, 1], points[:, 2]))

            
            self.vertices.append(self.axes.add_collection3d(Poly3DCollection(vertices, facecolors='red', linewidths=3, edgecolors=self.colors[i], alpha=0.5)))



            

    def CalculateLine(self,group):
        vertice = []
        point = group[0]
        first_point = point
        group.remove(point)
        while len(group) > 0 : 
            min_distance = self.distance(point,group[0])
            min_point = group[0]
            for i in group[1:]:
                if self.distance(point , i) < min_distance:
                    min_distance = self.distance(point , i)
                    min_point = i
            point = min_point
            group.remove(point)
            vertice.append(point)

        vertice.append(first_point)
        return vertice



    def distance(self,point1 , point2):
        return pow(point1[0] - point2[0] , 2)  +   pow(point1[1] - point2[1] , 2) + pow(point1[2] - point2[2] , 2)



class Simulation(QWidget):

    def __init__(self):
        super().__init__()

        # Create the maptlotlib FigureCanvas object,
        # which defines a single set of axes as self.axes.
        self.sc = MplCanvas( 5, 8, dpi=100)

        hbox = QHBoxLayout()
        hbox.addWidget(self.sc)
        #self.setCentralWidget(sc)
        self.setLayout(hbox)







