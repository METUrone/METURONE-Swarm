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
        self.before_pos = [0,0,0]

        self.prev_speed = [0,0,0]

        self.before_time = datetime.datetime.now()

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

    def go(self,speed_constant , collision_constant):



        speed_x = ((self.dest[0] - self.info["X"]) ) * speed_constant 
        speed_y = ((self.dest[1] - self.info["Y"]) ) * speed_constant 
        speed_z = ((self.dest[2] - self.info["Z"]) ) * speed_constant 




        return [speed_x,speed_y,speed_z]

    def hover(self,speed_constant , collision_constant):
        secs = datetime.datetime.now() - self.before_time
        secs = secs.total_seconds() + 0.000001


        desired_pos_x = self.before_pos[0] + self.prev_speed[0] * secs
        desired_pos_y = self.before_pos[1] + self.prev_speed[1] * secs
        desired_pos_z = self.before_pos[2] + self.prev_speed[2] * secs

        error_speed_x = (self.info["X"] - desired_pos_x)/secs 
        error_speed_y = (self.info["Y"] - desired_pos_y)/secs 
        error_speed_z = (self.info["Z"] - desired_pos_z)/secs 


        speed_x = ((self.dest[0] - self.info["X"]) - error_speed_x) * speed_constant
        speed_y = ((self.dest[1] - self.info["Y"]) - error_speed_y) * speed_constant
        speed_z = ((self.dest[2] - self.info["Z"]) - error_speed_z) * speed_constant 

        


        speed_x = self.clip(-0.3,0.3,speed_x)
        speed_y = self.clip(-0.3,0.3,speed_y)
        speed_z = self.clip(-0.3,0.3,speed_z)

        return [speed_x,speed_y,speed_z]


    def distance_to_dest(self):
        return math.sqrt(pow(self.dest[0]-self.info["X"],2) + pow(self.dest[1]-self.info["Y"],2) + pow(self.dest[2]-self.info["Z"],2))


    def calculate_speed(self,speed_constant = 0.8,collision_constant = 0.6):
	#Düzeltilecek
        
        if self.distance_to_dest() > 0.4 :
            [speed_x,speed_y,speed_z] = self.go(speed_constant,collision_constant)

        else :
            [speed_x,speed_y,speed_z] = self.go(speed_constant,collision_constant)

        self.before_pos = [self.info["X"],self.info["Y"],self.info["Z"]]
        self.before_time = datetime.datetime.now()
        self.prev_speed = [speed_x,speed_y,speed_z]

        

        return [speed_x,speed_y,speed_z]




    def takeoff(self,height = 0.5):#Kalkış heighti
        self.dest.z = height

    def land(self,height = 0.05): # İniş Heighti
        self.dest.z = height
     
    def length2(self,drone2):

        return pow(self.info["X"]-drone2.info["X"],2) + pow(self.info["Y"]-drone2.info["Y"],2) + pow(self.info["Z"]-drone2.info["Z"],2)

for i in range(Max_Uav_Number):
    uavList.append(copy.deepcopy(Uav(i)))
for uav in uavList:
    uav.init_Swarm(uavList)

uavList[1].SetDest(0,-1,1)





