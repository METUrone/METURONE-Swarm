#Swarmdaki her bir Uav clasının bir objesi
from utils import *

import datetime
import copy

uav_list = [] # this list is initialized and its objects are created in the bottom of this file
MAX_SPEED = 0.15
MAX_UAV_NUMBER = 10 # used for GUI

class Uav():
	def __init__(self, DroneId ,StartPos = [0,0,1]):
		self.info = {"Drone No" : DroneId , "Aktif" : "Hayır" , "X" : 0 , "Y" : 0 , "Z" : 0 ,"Batarya" : 0,"Grup" : 0} # GUI için gerekli
		self.dest = StartPos # Dronun ilk konumu  -- Pose ile veriniz
		self.mode = "Hover"
		self.hover_circle = 0.4

	def init_Swarm(self,swarms): # Diğer Droneların Konumu için gerekli, azicik daha aciklama? TODO
		self.swarms = swarms

	def UpdatePose(self,x,y,z):
		self.info["X"] = x
		self.info["Y"] = y
		self.info["Z"] = z

	def GetPose(self):
		return np.array([PoseX,PoseY,PoseZ])

	def PoseX(self):
		return self.info["X"]
	
	def PoseY(self):
		return self.info["Y"]
	
	def PoseZ(self):
		return self.info["Z"]
	
	def SetDest(self,x,y,z):
		self.dest[0]= float(x)
		self.dest[1] = float(y)
		self.dest[2] = float(z)

	# NEEDS TO BE CHANGED TODO
	def clip(self,min,max,number):
		if number < min:
		    return min
		elif number > max:
		    return max
		else :
		    return number

	def distance_to_dest(self , dest ):
		return math.sqrt(pow(dest[0]-self.PoseX,2) + pow(dest[1]-self.PoseY,2) + pow(dest[2]-self.PoseZ,2))

	def SetMode(self):
		if self.distance_to_dest(self.dest) < self.hover_circle / 2:
			self.mode = "Hover"
			return 

		for uav in uav_list:
			if uav == self or uav.info["Aktif"] == "Hayır":
				continue
			elif self.length_to_uav(uav) < self.hover_circle:
				self.mode = "Hover"
				return

		self.mode = "Go"

	def CollisionSpeed(self,collisionconstant , uav):
		return 1/pow(self.GetPose()-uav.GetPose(),3)*collision_constant

	def HoverCollision(self,collisionConstant):
		vector = np.array([0,0,0])
		for uav in uav_list:
			if uav.info["Aktif"] == "Hayır" or uav == self:
				continue
			distance = self.length_to_uav(uav)
			if distance < self.hover_circle:
				vector += self.CollisionSpeed(collisionConstant,uav)

		return vector

	def calculate_speed(self,speed_constant = 0.8,collision_constant = 0.3):
		self.SetMode()
		#print(self.info["Drone No"] , self.mode)
		speed = np.array([self.dest[0],self.dest[1],self.dest[2]])
		speed = speed - self.GetPose * speed_constant
		
		if self.mode == "Hover":
			collision_speed = self.HoverCollision(collision_constant)
			speed += collision_speed

		if self.mode == "Hover":
			np.vectorize(clip)(speed)

		return speed

	def takeoff(self,height = 0.5):#Kalkış heighti
		self.dest.z = height

	def land(self,height = 0.05): # İniş Heighti
		self.dest.z = height

	def length_to_uav(self,uav):
		return np.linalg.norm(self.GetPose-uav.GetPose())
		
for i in range(MAX_UAV_NUMBER):
    uav_list.append(copy.deepcopy(Uav(i)))
for uav in uav_list:
    uav.init_Swarm(uav_list)






