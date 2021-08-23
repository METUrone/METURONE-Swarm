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

        self.colors = ["red" , "green" , "blue" ,"yellow","brown","black","purple"]
        fig = Figure(figsize=(size,size), dpi=dpi)
        self.axes = fig.add_subplot(111,projection = '3d')
        super(MplCanvas, self).__init__(fig)
        
        self.floor = floor



    def ClearGraph(self):
        self.axes.clear()


        self.axes.set_zlim(0,self.floor)
        self.axes.set_xlim(-self.floor,self.floor)
        self.axes.set_ylim(-self.floor,self.floor)
    
        


    def CalculateAllLines(self,groups_s , aktif):


        
        self.ClearGraph() 
        if aktif == False or len(groups_s) == 0:
            return
           
        i = 0
        for group in groups_s:
            points = np.array(self.CalculateLine(group))
            vertices = []
            for j in range(len(points)):
                vertices.append([points[j],points[(j+1)%len(points)],points[j]])
            
    
            self.axes.scatter3D(points[:, 0], points[:, 1], points[:, 2])

            
            self.axes.add_collection3d(Poly3DCollection(vertices,  linewidths=3, edgecolors=self.colors[i], alpha=0.5))

            i+=1



            

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

        self.sc = MplCanvas( 5, 3, dpi=100)

        hbox = QHBoxLayout()
        hbox.addWidget(self.sc)

        buttonIdle = "QPushButton{background-color: lightblue;border-style: outset;border-width: 2px;border-radius: 10px;border-color: beige;font: bold 14px;min-width: 10em;padding: 6px;} "
        buttonPressed = "QPushButton::pressed{background-color : black;color : white}"
        buttonHover = "QPushButton::hover{background-color : yellow}"

        self.simulation_aktif = True
        self.simulation_button = QPushButton("Simülasyonu Başlat/Durdur")
        self.simulation_button.clicked.connect(self.SimMode)
        self.simulation_button.setStyleSheet(buttonIdle + buttonPressed + buttonHover)


        self.simulation_layout = QVBoxLayout()
        self.simulation_layout.addWidget(self.simulation_button)
        self.simulation_layout.addWidget(self.sc)



    def SimMode(self):
        if self.simulation_aktif:
            self.simulation_aktif = False
        else :
            self.simulation_aktif = True







