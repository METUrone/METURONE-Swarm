from utils import Pose

class SetFormation:
    def __init__(self,x,y,z , formationSide , distance , group):
        self.Center = Pose(x,y,z)
        self.formationSide = formationSide
        self.distance = distance
        self.group = group

class SetHareket:
    def __init__(self,x,y,z,group):
        self.Hedef = Pose(x,y,z)
        self.group = group

class Groups:
 
    def __init__(self,swarms):
        self.swarms = swarms

    def init_group(self,swarm_count):
        self.swarm_count = swarm_count
        self.group = []
        self.groups = []
        for i in range(self.swarm_count):
            self.group.append(i)
        
        self.groups.append(self.group)
    def SplitGroup(self,first,swarms):

        if len(swarms) == 0 :
            return

        if len(self.groups[first])==1:
            return
        new_group = []
        for i in swarms:
            self.groups[first].remove(i)
            new_group.append(i)
            self.swarms[i].getInfo()["Grup"] = len(self.groups)
            
        self.groups.append(new_group)
        

    def AppendGroups(self,first,second):

        if first == second :
            return

        new_group = self.groups[second]

        for i in new_group:
            self.groups[first].append(i)
            self.swarms[i].getInfo()["Grup"] = first

        self.groups[first].sort()

        new_group = self.groups.pop(second)
        
import math as m
M_PI = m.pi

class pose:
	x, y, z = 0, 0, 0

	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z



def rotate(curr, angle): # Angle in radians
    fn = pose(0,0,0);
    
    fn.x = curr.x*m.cos(angle) - curr.y*m.sin(angle);
    fn.y = curr.x*m.sin(angle) + curr.y*m.cos(angle);
    fn.z = curr.z;
    
    return fn;

def floor_angle(angle):

    angle = angle*180/M_PI;
    after_point = angle - (int(angle));
    remainder = (int(angle))%360;
    
    return (remainder+after_point)*M_PI/180;

        
