import math
import numpy as np

M_PI = math.pi

class Pose:
	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z

def Length(a,b):
	return np.linalg.norm(np.array([a.x,a.y,a.z])-np.array([b.x,b.y,b.z]))

def Rotate(curr, angle): # Angle in radians
	return Pose(curr.x*math.cos(angle) - curr.y*math.sin(angle),
				curr.x*math.sin(angle) + curr.y*math.cos(angle),
				curr.z)

# From 540 -> 180, makes the degree between (0,360)
""" this version may be used for performance, but the real performance impact should be done in rotation function
def FloorAngle2(angle):
    while angle > 360:
        angle-=360
    return angle
"""
def FloorAngle(angle):
	return 

	angle = angle*180/M_PI;
	after_point = angle - (int(angle));
	remainder = (int(angle))%360;
	
	return (remainder+after_point)*M_PI/180;

# TODO CHANGE THIS!
class Formations:
	def __init__(self):
		self.formations = {"Üçgen" : 3, "Kare" : 4 , "Beşgen " : 5 , "Altıgen" : 6 , "Yedigen" : 7 , "Sekizgen" : 8, "Dokuzgen" : 9 , "Ongen" : 10}
		
	def AddFormation(self , name , dronePoses) :
		self.formations[name] = dronePoses

formations = Formations()

if __name__ == "__main__":
	print(Length(Pose(1,2,3),Pose(1,2,5)))
	print(Rotate(Pose(1,2,3),M_PI).z)