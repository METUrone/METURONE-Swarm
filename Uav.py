#Swarmdaki her bir uav Uav clasının bir objesi
from Utils import *
from enum import Enum

import numpy as np

import datetime
import copy

#from mathutils.geometry import intersect_point_line
from threading import Lock

uavList = []
MAX_SPEED = 0.15
Max_Uav_Number = 10 # change
#Max uav number : GUI için gerekli (table için)

g_start_time = None
prev_dest_trajectory = None
time_lock = Lock()

def SetStartTime(time, prev):
	time_lock.acquire()
	global g_start_time
	global prev_dest_trajectory
	if prev != prev_dest_trajectory:
		g_start_time = time
		prev_dest_trajectory = prev
	time_lock.release()

def ReadStartTime():
	time_lock.acquire()
	global g_start_time
	result = g_start_time
	time_lock.release()
	return result


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



		self.collision_circle = 0.3
		self.hover_circle = 0.4
		COMMON_SPEED_CONSTANT = 0.5
		self.speed_clip_takeoff = COMMON_SPEED_CONSTANT
		self.speed_constant_hover = 0.8
		self.speed_constant_trajectory = 0.7
		self.speed_clip_land = 0.2
		self.speed_constant_circle = COMMON_SPEED_CONSTANT

		self.speed_clip_takeoff = 0.4
		self.speed_clip_go = 0.3

		self.collision_constant_go = 1.8
		self.collision_constant_hover = 1.3

		self.circle_center = None
		self.circle_radius = None
		self.circle_radian = None
		self.circle_timer = None

		self.trajectory_centers =[]
		self.trajectory_loop = False
		self.trajectory_speed = 0
		self.trajectory_first = None
		self.trajectory_start_time = None
		self.trajectory_start_pose = None
		self.trajectory_end_pose = None
		self.trajectory_correction_constant = 0.4

		self.distance_to_center = 0

	#eğer formasyon yoksa no trajectory
	def CalculateTrajectory(self,centers,speed,loop):
		
		if len(centers) == 0:
			return 
		else :
			self.trajectory_centers = copy.deepcopy(centers)
			self.trajectory_first = centers[0]
			self.trajectory_speed = speed
			self.trajectory_loop = loop
			self.SetState(State.TRAJECTORY)

	def SetDistanceToCenter(self,center,curr_pose):
		self.distance_to_center = np.array(curr_pose) - np.array(center)

	def CalculateNewCenter(self,old_center,new_center):
		
		x_change = new_center[0] - old_center[0] 
		y_change = new_center[1] - old_center[1] 
		z_change = new_center[2] - old_center[2] 


		pose = self.GetDest()

		self.SetDest(pose[0] + x_change , pose[1] + y_change , pose[2] + z_change)

		self.SetState(State.GO)


	def DistanceToCenter(self,center):
		return math.sqrt( pow(self.dest[0]-center[0],2) + pow(self.dest[1]-center[1],2) )

	def StartCircle(self,center):

		self.circle_center = center
		pose = self.GetDest()
		self.circle_radius = np.linalg.norm( np.array(pose) - np.array(self.circle_center) )
		self.circle_radian = math.atan2(pose[0] - self.circle_center[0] , pose[1] - self.circle_center[1])

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
		elif new_state == State.CONNECTED:
			pose = self.GetPose()
			self.dest = [pose[0],pose[1],0.0]
		elif new_state == State.TRAJECTORY:
			self.trajectory_start_time = datetime.datetime.now()
			self.trajectory_end_pose = np.array(self.trajectory_centers[0]) + self.distance_to_center
			self.trajectory_start_pose = np.array(self.GetPose())
		elif new_state == State.NOT_CONNECTED:
			self.info["Bağlı"] = "Hayır"

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
	
	def clip(self,border,number):
		border = abs(border)
		if number < -border:
		    return -border
		elif number > border:
		    return border
		else :
		    return number



	def distance_to_dest(self , dest = None ):
		if dest is None:
			dest = self.dest
		return math.sqrt(pow(dest[0]-self.info["X"],2) + pow(dest[1]-self.info["Y"],2) + pow(dest[2]-self.info["Z"],2))


	def CollisionSpeedHover(self, uav  ):
		x_diff = -(self.info["X"] - uav.info["X"])
		y_diff = -(self.info["Y"] - uav.info["Y"])

		if x_diff > 0 :
			x_diff -= self.collision_circle 
		else :
			x_diff += self.collision_circle

		if y_diff > 0 :
			y_diff -= self.collision_circle
		else :
			y_diff += self.collision_circle


		speed_x = x_diff * self.collision_constant_hover
		speed_y = y_diff * self.collision_constant_hover
		return [speed_x,speed_y,0]

	def CalculateLandSpeed(self, clip_speed = None):
		if clip_speed is None:
			clip_speed = self.speed_clip_land
		pose = self.GetPose()
		if pose[2] < 0.4:
			return None
		else:
			speed_x = ((self.dest[0] - self.info["X"]) ) 
			speed_y = ((self.dest[1] - self.info["Y"]) ) 
			speed_z = ((self.dest[2] - self.info["Z"]) ) 
			
			speed_x = self.clip(clip_speed,speed_x)
			speed_y = self.clip(clip_speed,speed_y)
			speed_z = self.clip(clip_speed,speed_z)

			return [speed_x,speed_y,speed_z]


	def CalculateCircleSpeed(self):


		x = self.circle_center[0] + self.circle_radius * math.sin(self.circle_radian)
		y = self.circle_center[1] + self.circle_radius * math.cos(self.circle_radian)
		self.circle_radian += 0.005

		speed_x = ((x - self.info["X"]) ) 
		speed_y = ((y - self.info["Y"]) ) 
		speed_z = ((self.circle_center[2] - self.info["Z"]) ) 


		
		return [speed_x,speed_y,speed_z]

	# Be careful! No clip
	def CalculateHoverSpeed(self):
		if self.distance_to_dest() > self.hover_circle:
		
			self.SetState(State.GO)

		elif self.distance_to_dest() < 0.05:
			return [0,0,0]

		else:
			speed_x = ((self.dest[0] - self.info["X"]) ) 
			speed_y = ((self.dest[1] - self.info["Y"]) ) 
			speed_z = ((self.dest[2] - self.info["Z"]) ) 
			
		

			speed_x *= self.speed_constant_hover
			speed_y *= self.speed_constant_hover
			speed_z *= self.speed_constant_hover

			return [speed_x,speed_y,speed_z]

	def CalculateGoSpeedCircle(self , uav):
		
		self.circle_center = uav.GetPose()
		pose = self.GetDest()
		self.circle_radius = self.hover_circle
		self.circle_radian = math.atan2(pose[0] - self.circle_center[0] , pose[1] - self.circle_center[1]) + 0.02
		speed = self.CalculateCircleSpeed()[:2]

		speed = normalize(speed)

		speed[0] *= 0.1
		speed[1] *= 0.1

		print("circle " , speed)
		return [speed[0],speed[1],0.0]

	

	def CalculateGoSpeed(self, clip_speed = None):


		if clip_speed is None:
			clip_speed = self.speed_clip_go
		
		for uav in uavList:
			if uav == self:
				continue
			if uav.GetState() == State.HOVER:
				distance = self.length_to_uav(uav)
				start_point = self.GetPose()
				end_point = self.GetDest()
				circle_center = uav.GetDest()

				if distance < self.hover_circle:
					if checkCollision( start_point , end_point , circle_center, self.collision_circle):
						return self.CalculateGoSpeedCircle(uav)

			

		

		if self.distance_to_dest() < self.hover_circle:
		
			self.SetState(State.HOVER)

		speed_x = ((self.dest[0] - self.info["X"]) ) 
		speed_y = ((self.dest[1] - self.info["Y"]) ) 
		speed_z = ((self.dest[2] - self.info["Z"]) )
		
		speed = normalize([speed_x,speed_y,speed_z])
	
		speed[0]*= self.speed_clip_go
		speed[1]*= self.speed_clip_go
		speed[2]*= self.speed_clip_go

		print("normal",speed)


		return speed

	def EndTrajectory(self , grup):
		center = self.trajectory_centers[-1]
		
		for uav in uavList:

			if uav.info["Grup"] == grup and uav.GetState() == State.TRAJECTORY:
				pose = np.array(center) + uav.distance_to_center
				uav.SetDest(pose[0] , pose[1] ,center[2])
				uav.SetState(State.HOVER)
				print(uav.GetDest())


	def CalculateTrajectorySpeed(self):


		curr_pose = np.array(self.GetPose())
		destinated_pose = np.array(self.trajectory_centers[0]) + self.distance_to_center

		result = None


		if np.linalg.norm(curr_pose-destinated_pose) > 0.2:
			distance_between_centers = np.array(self.trajectory_centers[0]) - np.array(self.GetPose()) + self.distance_to_center
			length = np.linalg.norm(distance_between_centers)
			result = [self.trajectory_speed * distance_between_centers[0] / length, self.trajectory_speed * distance_between_centers[1] / length, (self.dest[2] - self.info["Z"]) * self.speed_constant_trajectory]
		else:
			self.trajectory_start_pose = destinated_pose

			
			SetStartTime(datetime.datetime.now(), self.trajectory_centers[0])
			
			self.trajectory_start_time = ReadStartTime()
			c = self.trajectory_centers.pop(0)
			if self.trajectory_centers[0] == self.trajectory_first and self.trajectory_loop == False:
				self.EndTrajectory(self.info["Grup"])
			self.trajectory_centers.append(c)
			self.trajectory_end_pose = np.array(self.trajectory_centers[0]) + self.distance_to_center
			return self.CalculateTrajectorySpeed()


		#distance_to_trajectory_line = np.cross(self.trajectory_end_pose-self.trajectory_start_pose,curr_pose-self.trajectory_start_pose)/np.linalg.norm(self.trajectory_end_pose-self.trajectory_start_pose)
		#distance_to_trajectory_line *= self.trajectory_correction_constant
		
		#closest_point = np.array(intersect_point_line(curr_pose,self.trajectory_start_pose,self.trajectory_end_pose)[0])
		closest_point = np.array(self.trajectory_start_pose) + np.array(result) * (datetime.datetime.now() - self.trajectory_start_time).total_seconds()
		print(closest_point, curr_pose,(datetime.datetime.now() - self.trajectory_start_time).total_seconds())
		closest_vector = closest_point - curr_pose
		closest_vector *= self.trajectory_correction_constant
		return np.array(result) + np.array([closest_vector[0],closest_vector[1],0])


	def CalculateTakeOffSpeed(self, clip_speed = None ):
		if clip_speed is None:
			clip_speed = self.speed_clip_takeoff

		if self.distance_to_dest(self.dest) < self.hover_circle:
		
			self.SetState(State.HOVER)

		speed_x = ((self.dest[0] - self.info["X"]) ) 
		speed_y = ((self.dest[1] - self.info["Y"]) ) 
		speed_z = ((self.dest[2] - self.info["Z"]) )
		
		speed_x = self.clip(clip_speed,speed_x)
		speed_y = self.clip(clip_speed,speed_y)
		speed_z = self.clip(clip_speed,speed_z)

		return [speed_x,speed_y,speed_z]

	def CalculateCollisionSpeed(self):
		return self.HoverCollision()
		

	def GoCollision(self):
		return [0,0,0]

	def HoverCollision(self):
		speed_x = 0
		speed_y = 0
		speed_z = 0

		for uav in uavList:
			if uav == self or uav.GetState() == State.NOT_CONNECTED or uav.GetState() == State.CONNECTED:
				continue

			distance = self.length_to_uav(uav)

			if distance < self.collision_circle :
				speed = self.CollisionSpeedHover(uav )
				speed_x += speed[0]
				speed_y += speed[1]

		speed = normalize([speed_x,speed_y])

		speed[0] *= 0.4
		speed[1] *= 0.4


		return [speed_x,speed_y,0]


	def calculate_speed(self):
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

		else:
			return None



	def length_to_uav(self,uav):

		return math.sqrt(pow(self.info["X"]-uav.info["X"],2) + pow(self.info["Y"]-uav.info["Y"],2) + pow(self.info["Z"]-uav.info["Z"],2))

for i in range(Max_Uav_Number):
    uavList.append(copy.deepcopy(Uav(i)))
for uav in uavList:
    uav.init_Swarm(uavList)







