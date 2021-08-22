import time as t
import math as m
from munkres import Munkres

from utils import *

M_PI = m.pi


class Formation:

	# formation elements
	center = Pose(0.0, 0.0, 0.0)
	sides = []
	ihaArasiUzaklik = 0.0
	ihaSayisi = 0
	isFormed = False
	formationConstant = 0.0

	# individual and parametric elements
	droneID = 0
	height = 0.0
	angle = 0.0
	initialAngle = 0.0
	initialPosition = Pose(0.0, 0.0, 0.0)

	# constructor
	def __init__(self):
		self.height
		self.initialPosition = Pose(0,0,0)

	# some getters used throughout the code
	def GetSides(self):
		sides = []
		for side in self.sides:
			sides.append([side.x,side.y,self.height])

		return sides


	def getCurrentAngle(self):
		return self.angle

	def getInitialAngle(self):
		return self.initialAngle

	# some setters used widely through the code
	def setUAVnum(self, num):
		self.ihaSayisi = num
		##{ ihaSayisi = num; };

	def setCurrentAngle(self, angle):
		self.angle = angle

	
	# Used to partially create a polygon
	# Takes three integer arguments, number of sides, distance between UAVs and number of UAVs in the polygon
	# Returns a list of points fot the UAVs to go
	def PartialCokgen(self, kenar, ihaArasiUzaklik, ihaSayisi, center, angle=0):
		sides = []
		if (ihaSayisi <= 0):
			return sides

		addition = Pose(
				ihaArasiUzaklik*m.cos(2*M_PI/kenar+self.angle),
				ihaArasiUzaklik*m.sin(2*M_PI/kenar+self.angle),
				0.0)
		curr = self.initialPosition
		for i in range(0,ihaSayisi):
				curr_append = Pose(curr.x, curr.y, curr.z)
				sides.append(curr_append)
				curr.x += addition.x
				curr.y += addition.y
				curr.z += addition.z

				if ((i+1) % (ihaSayisi/kenar) == 0):
					addition = Rotate(addition, 2*M_PI/kenar)
		return sides

	# Creates polygon formation with arbitary number of sides
	# Takes an integer argument, the number of sides
	def Cokgen(self, ihaSayisi, ihaArasiUzaklik,kenar, center=0, angle=0):
		self.ihaSayisi = ihaSayisi
		self.ihaArasiUzaklik = ihaArasiUzaklik
		self.height = center.z
		print("Cokgen kenar: ", kenar);
		# self.initialPosition
		if (self.sides != []):
			self.sides = []
		
		k = self.ihaSayisi//kenar;
		
		insiderAngle = (kenar-2)*m.pi/(kenar*2)
		self.initialPosition.x = center.x + self.ihaArasiUzaklik*k/2
		self.initialPosition.y = (center.y - m.tan(insiderAngle)*self.ihaArasiUzaklik*k/2)
		
		if (self.ihaSayisi%kenar == 0):
			self.sides = self.PartialCokgen(kenar, self.ihaArasiUzaklik, self.ihaSayisi, center);
			self.isFormed = True;
			return;

		# TODO: Check integer division
		denseCount = 2*(self.ihaSayisi%kenar)*(self.ihaSayisi//kenar);
		denseLength = self.ihaArasiUzaklik*k/(k+1);

		print("İHA mesafe: ", self.ihaArasiUzaklik, " Dense length: ", denseLength);

		dense = self.PartialCokgen(kenar, denseLength, (self.ihaSayisi//kenar+1)*kenar, center);
		sparse = self.PartialCokgen(kenar, self.ihaArasiUzaklik, self.ihaSayisi-self.ihaSayisi%kenar, center);

		print(dense)
		print(sparse)

		"""
		for i in range(min(denseCount,self.ihaSayisi)):
			self.sides.append(dense[i]);
		for i in range(self.ihaSayisi-self.ihaSayisi%kenar-1, len(self.sides),-1):
			print(i)
			self.sides.append(sparse[i]);"""
		# TODO: Test this
		self.sides = dense[:min(denseCount,self.ihaSayisi)]+sparse[self.ihaSayisi-self.ihaSayisi%kenar-1:len(self.sides):-1]

		print(self.sides)
		self.isFormed = True;

	# Creates a pentagon with 5 UAVs to be used in Yildiz function
	# Will not be used in any other function
	def YildizHelper(self, isBigPentagon):
		kenar = 5;
		ihaSayisi = 5;
		sides = [];

		addition = Pose(
				self.ihaArasiUzaklik*m.cos(2*M_PI/kenar+self.angle),
				self.ihaArasiUzaklik*m.sin(2*M_PI/kenar+self.angle),
				0.0);

		curr = self.initialPosition

		if (isBigPentagon):
			addition.x = -self.ihaArasiUzaklik*((3+m.sqrt(5))/2);
			addition.y = 0.0;
			addition.z = 0.0;

			curr.x = self.initialPosition.x + self.ihaArasiUzaklik*((1+m.sqrt(5))/4);
			curr.y = self.initialPosition.y + self.ihaArasiUzaklik*(m.sqrt((50+22*m.sqrt(5))/16));
			curr.z = self.initialPosition.z;

			curr = Rotate(curr, self.angle);
			addition = Rotate(addition, self.angle);
		
		for i in range(ihaSayisi):
			curr_append = Pose(curr.x, curr.y, curr.z)
			sides.append(curr_append);

			curr.x += addition.x;
			curr.y += addition.y;
			curr.z += addition.z;

			if ((i+1)%(ihaSayisi/kenar) == 0):
				addition = Rotate(addition, 2*M_PI/kenar);
		return sides;

	# Creates star formation with 10 UAVs
	def Yildiz(self):
		if (self.sides != []):
			self.sides = [];

		kucukBesgen = self.YildizHelper(False);
		buyukBesgen = self.YildizHelper(True);

		for i in range(self.ihaSayisi//2):
			self.sides.append(kucukBesgen[i]);

		for i in range(self.ihaSayisi//2, self.ihaSayisi):
			self.sides.append(buyukBesgen[i-self.ihaSayisi//2]);

		self.isFormed = True;
	
	# Creates V formation
	def V(self):
		if (self.sides != []):
			self.sides = []

		addition = Pose(
				self.ihaArasiUzaklik*m.cos(2*M_PI/3+self.angle),
				self.ihaArasiUzaklik*m.sin(2*M_PI/3+self.angle),
				0.0)

		curr = self.initialPosition;

		for i in range(self.ihaSayisi):
			curr_append = Pose(curr.x, curr.y, curr.z)
			self.sides.append(curr_append);

			curr.x += addition.x;
			curr.y += addition.y;
			curr.z += addition.z;

			if (i == self.ihaSayisi/2-1):
				addition = Rotate(addition, 2*M_PI/3);

		self.isFormed = True;

	# Creates V formation
	def Hilal(self):
		if (self.sides != []):
			self.sides = []

		sekizgen = self.PartialCokgen(8, self.ihaArasiUzaklik, (self.ihaSayisi/8+1)*8);

		for i in range(self.ihaSayisi):
			self.sides.append(sekizgen[i]);

		self.isFormed = True;

	# Creates arbitary formation from given points
	# Takes a list of points and the height of the formation
	def Miscellaneous(self, poses, height):
		for i in range(self.ihaSayisi+1): # ihaSayisi+1 ???
			self.sides[i].x = poses[i].x;
			self.sides[i].y = poses[i].y;

			if (height == 0):
				self.sides[i].z = poses[i].z;
			else:
				self.sides[i].z = height;

	def moveFormationReg(self, destX, destY, destZ):
		incX = destX-self.sides[0].x
		incY = destY-self.sides[0].y
		incZ = destZ-self.sides[0].z

		for i in range(self.ihaSayisi):
			self.sides[i].x += incX
			self.sides[i].y += incY
			self.sides[i].z += incZ

		self.initialPosition = self.sides[0]

	# move formation to a point with appropriate increment and rate
	def moveFormationRate(self, destX, destY, destZ, increment, rate):
		angle = m.atan((destY-self.initialPosition.y) / (destX - self.initialPosition.x))
		incX = increment*m.cos(angle)
		incY = increment*m.sin(angle)

		if (destX+incX >= self.initialPosition.x and self.initialPosition.x >= destX-incX and destY+incY >= self.initialPosition.y and self.initialPosition.y >= destY-incY):
			self.initialPosition.x = destX
			self.initialPosition.y = destY
			return

		for i in range(self.ihaSayisi):
			self.sides[i].x += incX
			self.sides[i].y += incY
		
		self.initialPosition = self.sides[0]
		t.sleep(rate)

	# Increments positively for CCW, negative for CW
	# Dönüş hızı increment ve rate değerleriyle ayarlanabilir.
	# Will be removed for rotation to commander
	def turnFormationAroundPoint(self, center, increment, rate, angle=0):
		print("Current angle: ", FloorAngle(self.angle)*180/M_PI);
		print("Destination angle: [", FloorAngle(angle-increment)*180/M_PI, ",", FloorAngle(angle+increment)*180/M_PI, "]");

		if (angle and (FloorAngle(angle+increment) >= FloorAngle(self.angle) and FloorAngle(self.angle) >= FloorAngle(angle-increment))):
			self.angle = angle
			self.initialAngle = angle
			return
		
		axis = Pose(self.initialPosition.x-center.x, self.initialPosition.y-center.y, self.initialPosition.z-center.z)

		for i in range(self.ihaSayisi):
			axis.x = self.sides[i].x - center.x
			axis.y = self.sides[i].y - center.y
			axis.z = self.sides[i].z - center.z
		
			axis = Rotate(axis, increment)

			self.sides[i].x = axis.x + center.x;
			self.sides[i].y = axis.y + center.y;
			self.sides[i].z = axis.z + center.z;
		
		self.angle += increment
		t.sleep(rate)

	def assignDrones(self, currentPoses):
		initial_cost = [[Length(dest, drone) for drone in currentPoses] for dest in self.sides]
		hungarian = Munkres()
		
		# Returns a list of tuples that is of the form
		# (index of drone in currentPoses, index of position in self.sides)
		indexes = hungarian.compute(initial_cost)

		return indexes

	def UAVRepulsion(self):
		rep = pose(0,0,0)
		# TODO
