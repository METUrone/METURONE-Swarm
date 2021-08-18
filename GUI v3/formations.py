class Formations:
	def __init__(self):
		self.formations = {"Üçgen" : 3, "Kare" : 4 , "Beşgen " : 5 , "Altıgen" : 6 , "Yedigen" : 7 , "Sekizgen" : 8, "Dokuzgen" : 9 , "Ongen" : 10}
		
	
	def AddFormation(self , name , dronePoses) :
		self.formations[name] = dronePoses
formations = Formations()

