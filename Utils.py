import math
from threading import Lock
import numpy as np
class Vec3:
	def __init__(self,x,y,z):
		self.x = x
		self.y = y
		self.z = z
		
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



console_lock = Lock()
console_output = ""

def ConsoleOutput(text):
	global console_lock
	global console_output
	console_lock.acquire()
	console_output += text + "\n"
	print(console_output)
	console_lock.release()

def CheckUpdate():
	global console_lock
	global console_output
	console_lock.acquire()
	x = console_output
	console_output = ""
	console_lock.release()
	return x

def checkCollision(point_start,point_end, circle_center,radius):
	
	# Finding the distance of line
	# from center.
	x = circle_center[0]
	y = circle_center[1]

	a,b,c = lineFromPoints(point_start,point_end)
	print(a,b,c)
	
	dist = ((abs(a * x + b * y + c)) /
		math.sqrt(a * a + b * b))

	print(2/math.sqrt(17))
	print(dist)

	if radius >= dist:
		return True
	else:
		return False
    

def lineFromPoints(P, Q):

	a = Q[1] - P[1]
	b = P[0] - Q[0]
	c = a*(P[0]) + b*(P[1])

	return [a,b,-c]


def normalize(v):
	norm=np.linalg.norm(v, ord=2)
	if norm==0:
		return [0,0,0]
	return v/norm

print(normalize([-0.2,0.3,0]))