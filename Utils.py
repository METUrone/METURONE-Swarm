import math
import numpy as np

M_PI = math.pi

class Pose:
	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z

def length2(a,b):
	return np.linalg.norm(np.array([a.x,a.y,a.z])-np.array([b.x,b.y,b.z]))

def rotate(curr, angle): # Angle in radians
	return Pose(curr.x*math.cos(angle) - curr.y*math.sin(angle),
				curr.x*math.sin(angle) + curr.y*math.cos(angle),
				curr.z)

# WTF IS THAT? TODO
def floor_angle(angle):

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
	print(length2(Pose(1,2,3),Pose(1,2,5)))
	print(rotate(Pose(1,2,3),M_PI).z)

""" NOT TO BE USED FOR SOME TIME
def NormalizeSpeed(speed, max_speed,count = 0):
	if count > 10:
		print("Normalize Speed cannot converge!", speed, max_speed)
		exit()
	x = speed[0]
	y = speed[1]
	z = speed[2]

	scalar = math.sqrt(pow(x,2) + pow(y,2) + pow(z,2))
	if scalar > max_speed:
		return NormalizeSpeed([x/scalar*max_speed, y/scalar*max_speed, z/scalar*max_speed],max_speed,count+1) # will be changed
	return speed
"""

