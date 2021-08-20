import math as m
M_PI = m.pi

class pose:
	x, y, z = 0.0, 0.0, 0.0

	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z

def length2(thisDrone, notthisDrone):
    distance = pose(0,0,0);
    distance.x = thisDrone.x-notthisDrone.x;
    distance.y = thisDrone.y-notthisDrone.y;
    distance.z = thisDrone.z-notthisDrone.z;
    return distance.x*distance.x + distance.y * distance.y + distance.z * distance.z;

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
