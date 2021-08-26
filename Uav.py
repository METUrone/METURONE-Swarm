#Swarmdaki her bir uav Uav clasının bir objesi
from Utils import *
from enum import Enum

import datetime
import copy

uavList = []
MAX_SPEED = 0.15
Max_Uav_Number = 10 # change
#Max uav number : GUI için gerekli (table için)

class State(Enum):
	NOT_CONNECTED = 0
	CONNECTED = 1
	TAKEOFF = 2
	CIRCLE = 4
	TRAJECTORY = 8
	GO = 16
	HOVER = 32
	LOW_BATTERY = 64

	

class Uav():
	def __init__(self,DroneId , StartPos = [0,0,1]):
		self.states = {State.NOT_CONNECTED : "Bağlı Değil" , State.CONNECTED : "Hazır" , State.TAKEOFF : "TakeOff" , State.CIRCLE : "Daire" , State.TRAJECTORY:"Trajectory" , State.GO : "Go" , State.HOVER  : "Hover" , State.LOW_BATTERY : "Low"}

		self.state = State.NOT_CONNECTED
		self.info = {"Drone No" : DroneId , "Bağlı" : "Hayır", "Durum": self.states[self.state] , "X" : 0 , "Y" : 0 , "Z" : 0 ,"Batarya" : 0,"Grup" : 0} # GUI için gerekli
		self.dest = StartPos # Dronun ilk konumu  -- Utilsdeki Vec3 ile veriniz
		
		self.mode = "Hover"

		self.hover_circle = 0.3
		COMMON_SPEED_CONSTANT = 0.5
		self.speed_clip_takeoff = COMMON_SPEED_CONSTANT
		self.speed_constant_hover = 0.7
		self.speed_clip_land = 0.2
		self.speed_constant_circle = COMMON_SPEED_CONSTANT

		self.speed_clip_takeoff = 0.4
		self.speed_clip_go = 0.4

		self.circle_center = [0,0,0]
		self.circle_radious = 0
		self.circle_radian = 0

		self.trajectory_centers =[]
		self.trajectory_loop = False
		self.trajectory_speed = 0

	def CalculateTrajectory(self,centers,speed,loop):
		
		if len(centers) == 0:
			return 
		else :
			self.trajectory_centers = centers
			self.speed = speed
			self.loop = loop
			self.SetState(State.TRAJECTORY)


	def CalculateNewCenter(self,old_center,new_center):
		
		x_change = new_center[0] - old_center[0] 
		y_change = new_center[1] - old_center[1] 
		z_change = new_center[2] - old_center[2] 

		print("centers " ,old_center , new_center)

		pose = self.GetDest()

		print("old dest" ,self.GetDest())

		self.SetDest(pose[0] + x_change , pose[1] + y_change , pose[2] + z_change)
		print(self.GetDest())
		
		self.SetState(State.GO)


	def DistanceToCenter(self,center):
		return math.sqrt( pow(self.dest[0]-center[0],2) + pow(self.dest[1]-center[1],2) )

	def StartCircle(self,center):
		"""pose = self.GetPose()
		self.circle_radian = math.atan(  (pose[1] - center[1] ) / ( pose[0] - center[0] ) )
		self.circle_center = center
		self.circle_radious = max(self.DistanceToCenter(center),1)"""
		print("Start Circle")
		self.SetState(State.CIRCLE)

	def StopCircle(self):
		self.dest = self.GetPose()
		print("Stop Circle")
		self.SetState(State.HOVER)
		
	def GetDroneNo(self):
		return self.info["Drone No"]

	def GetDest(self):
		return self.dest

	
	def GetPose(self):
		return [self.info["X"] , self.info["Y"] , self.info["Z"]]

	def SetState(self, new_state):
		# check needed

		if new_state == State.TAKEOFF:
			pose = self.GetPose()
			self.dest = [pose[0],pose[1],1.0]

		if new_state == State.CONNECTED:
			pose = self.GetPose()
			self.dest = [pose[0],pose[1],0.0]
		self.state = new_state
		self.info["Durum"] = self.states[self.state]
		# adjustments needed
	
	def GetState(self):
		return self.state
		
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
			if uav == self or uav.info["Bağlı"] == "Hayır":
				continue
			elif self.length_to_uav(uav) < self.hover_circle:
				self.mode = "Hover"
				return

		self.mode = "Go"

	def CollisionSpeed(self,collisionconstant , uav):
		speed_x = 1/pow(self.info["X"] - uav.info["X"],3) * collisionconstant
		speed_y = 1/pow(self.info["Y"] - uav.info["Y"],3) * collisionconstant
		speed_z = 1/pow(self.info["Z"] - uav.info["Z"],3) * collisionconstant
		return [speed_x,speed_y,speed_z]

	def CalculateLandSpeed(self):
		pose = self.GetPose()
		if pose[2] < 0.4:
			return None
		else:
			speed_x = ((self.dest[0] - self.info["X"]) ) 
			speed_y = ((self.dest[1] - self.info["Y"]) ) 
			speed_z = ((self.dest[2] - self.info["Z"]) ) 
			
			speed_x = self.clip(-self.speed_clip_land,self.speed_clip_land,speed_x)
			speed_y = self.clip(-self.speed_clip_land,self.speed_clip_land,speed_y)
			speed_z = self.clip(-self.speed_clip_land,self.speed_clip_land,speed_z)

			return [speed_x,speed_y,speed_z]


	def CalculateCircleSpeed(self):

		self.SetState(State.HOVER)
	
		"""x_offset = self.circle_radious * math.cos(self.circle_radian)
		y_offset = self.circle_radious * math.sin(self.circle_radian)
		self.circle_radian += 0.003
		self.SetDest(self.circle_center[0] + x_offset , self.circle_center[1] + y_offset , self.circle_center[2])
		speed_x = ((self.dest[0] - self.info["X"]) )
		speed_y = ((self.dest[1] - self.info["Y"]) )
		speed_z = ((self.dest[2] - self.info["Z"]) )
		
		speed_x = self.clip(-0.2,0.2,speed_x)
		speed_y = self.clip(-0.2,0.2,speed_y)
		speed_z = self.clip(-0.2,0.2,speed_z)"""

		return [speed_x,speed_y,speed_z]

	def CalculateHoverSpeed(self):
		if self.distance_to_dest(self.dest) > self.hover_circle:
		
			self.SetState(State.GO)

		speed_x = ((self.dest[0] - self.info["X"]) ) * self.speed_constant_hover
		speed_y = ((self.dest[1] - self.info["Y"]) ) * self.speed_constant_hover
		speed_z = ((self.dest[2] - self.info["Z"]) ) * self.speed_constant_hover
		

		return [speed_x,speed_y,speed_z]

	def CalculateGoSpeed(self):
		if self.distance_to_dest(self.dest) < self.hover_circle:
		
			self.SetState(State.HOVER)

		speed_x = ((self.dest[0] - self.info["X"]) ) 
		speed_y = ((self.dest[1] - self.info["Y"]) ) 
		speed_z = ((self.dest[2] - self.info["Z"]) )
		
		speed_x = self.clip(-self.speed_clip_go,self.speed_clip_go,speed_x)
		speed_y = self.clip(-self.speed_clip_go,self.speed_clip_go,speed_y)
		speed_z = self.clip(-self.speed_clip_go,self.speed_clip_go,speed_z)

		return [speed_x,speed_y,speed_z]

	def CalculateTrajectorySpeed(self):
		print("Trajectory")
		self.SetState(State.HOVER)

	def CalculateTakeOffSpeed(self ):

		if self.distance_to_dest(self.dest) < self.hover_circle:
		
			self.SetState(State.HOVER)

		speed_x = ((self.dest[0] - self.info["X"]) ) 
		speed_y = ((self.dest[1] - self.info["Y"]) ) 
		speed_z = ((self.dest[2] - self.info["Z"]) )
		
		speed_x = self.clip(-self.speed_clip_takeoff,self.speed_clip_takeoff,speed_x)
		speed_y = self.clip(-self.speed_clip_takeoff,self.speed_clip_takeoff,speed_y)
		speed_z = self.clip(-self.speed_clip_takeoff,self.speed_clip_takeoff,speed_z)

		return [speed_x,speed_y,speed_z]


	def HoverCollision(self,collisionConstant):
		speed_x = 0
		speed_y = 0
		speed_z = 0

		for uav in uavList:
			if uav.info["Bağlı"] == "Hayır" or uav == self:
				continue

			distance = self.length_to_uav(uav)

			if distance < self.hover_circle:
				speed = self.CollisionSpeed(collisionConstant,uav)
				speed_x += speed[0]
				speed_y += speed[1]
				speed_z += speed[2]

		return [speed_x,speed_y,speed_z]
	def calculate_speed(self,speed_constant = 0.8,collision_constant = 0.3):
		if self.GetState() == State.CONNECTED or self.GetState() == State.LOW_BATTERY:
			return self.CalculateLandSpeed()
		
		elif self.GetState() == State.TAKEOFF:
			return self.CalculateTakeOffSpeed()


		elif self.GetState() == State.CIRCLE:
			return self.CalculateCircleSpeed()
		
		elif self.GetState() == State.HOVER:
			return self.CalculateHoverSpeed()
		
		elif self.GetState() == State.GO:
			return self.CalculateGoSpeed()
		
		elif self.GetState() == State.TRAJECTORY:
			return self.CalculateTrajectorySpeed()

		else :
			return [0,0,0]



	def length_to_uav(self,uav):

		return math.sqrt(pow(self.info["X"]-uav.info["X"],2) + pow(self.info["Y"]-uav.info["Y"],2) + pow(self.info["Z"]-uav.info["Z"],2))

for i in range(Max_Uav_Number):
    uavList.append(copy.deepcopy(Uav(i)))
for uav in uavList:
    uav.init_Swarm(uavList)






