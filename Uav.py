#Swarmdaki her bir uav Uav clasının bir objesi
from Utils import *


import datetime
import copy

uavList = []
MAX_SPEED = 0.15
Max_Uav_Number = 10 # change
#Max uav number : GUI için gerekli (table için)

class Uav():
	def __init__(self,DroneId , StartPos = [0,0,1]):
		self.info = {"Drone No" : DroneId , "Aktif" : "Hayır" , "X" : 0 , "Y" : 0 , "Z" : 0 ,"Batarya" : 0,"Grup" : 0} # GUI için gerekli
		self.dest = StartPos # Dronun ilk konumu  -- Utilsdeki Vec3 ile veriniz

		self.mode = "Hover"

		self.hover_circle = 0.4

	def init_Swarm(self,swarms): # Diğer Droneların Konumu için gerekli
		self.swarms = swarms

	def Update(self,x,y,z):
		self.info["X"] = x
		self.info["Y"] = y
		self.info["Z"] = z


	def SetDest(self,x,y,z):
		self.dest[0]= float(x)
		self.dest[1] = float(y)
		self.dest[2] = float(z)

	def clip(self,min,max,number):
		if number < min:
		    return min
		elif number > max:
		    return max
		else :
		    return number

	def distance_to_dest(self , dest ):
		return math.sqrt(pow(dest[0]-self.info["X"],2) + pow(dest[1]-self.info["Y"],2) + pow(dest[2]-self.info["Z"],2))

	def SetMode(self):
		if self.distance_to_dest(self.dest) < self.hover_circle / 2:
			self.mode = "Hover"
			return 

		for uav in uavList:
			if uav == self or uav.info["Aktif"] == "Hayır":
				continue
			elif self.length_to_uav(uav) < self.hover_circle:
				self.mode = "Hover"
				return

		self.mode = "Go"

	def CollisionSpeed(self,collisionconstant , uav):
		speed_x = 1/pow(self.info["X"] - uav.info["X"],3) * collisionconstant;
		speed_y = 1/pow(self.info["Y"] - uav.info["Y"],3) * collisionconstant;
		speed_z = 1/pow(self.info["Z"] - uav.info["Z"],3) * collisionconstant;
		return [speed_x,speed_y,speed_z]

	def HoverCollision(self,collisionConstant):
		speed_x = 0
		speed_y = 0
		speed_z = 0

		for uav in uavList:
			if uav.info["Aktif"] == "Hayır" or uav == self:
				continue

			distance = self.length_to_uav(uav)

			if distance < self.hover_circle:
				speed = self.CollisionSpeed(collisionConstant,uav)
				speed_x += speed[0]
				speed_y += speed[1]
				speed_z += speed[2]

		return [speed_x,speed_y,speed_z]
	def calculate_speed(self,speed_constant = 0.8,collision_constant = 0.3):


		self.SetMode()
		#print(self.info["Drone No"] , self.mode)

		speed_x = ((self.dest[0] - self.info["X"]) ) * speed_constant 
		speed_y = ((self.dest[1] - self.info["Y"]) ) * speed_constant 
		speed_z = ((self.dest[2] - self.info["Z"]) ) * speed_constant 

		#print(self.mode)

		if self.mode == "Hover":
			collision_speed = self.HoverCollision(collision_constant)
			speed_x += collision_speed[0]
			speed_y += collision_speed[1]
			speed_z += collision_speed[2]

			speed_x = self.clip(-0.2,0.2,speed_x)
			speed_y = self.clip(-0.2,0.2,speed_y)
			speed_z = self.clip(-0.1,0.1,speed_z)

		speed_x = self.clip(-0.4,0.4,speed_x)
		speed_y = self.clip(-0.4,0.4,speed_y)
		speed_z = self.clip(-0.4,0.4,speed_z)

		return [speed_x,speed_y,speed_z]




	def takeoff(self,height = 0.5):#Kalkış heighti
		self.dest.z = height

	def land(self,height = 0.05): # İniş Heighti
		self.dest.z = height

	def length_to_uav(self,uav):

		return math.sqrt(pow(self.info["X"]-uav.info["X"],2) + pow(self.info["Y"]-uav.info["Y"],2) + pow(self.info["Z"]-uav.info["Z"],2))

for i in range(Max_Uav_Number):
    uavList.append(copy.deepcopy(Uav(i)))
for uav in uavList:
    uav.init_Swarm(uavList)






