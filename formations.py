import pickle
import os

class Formations:
	def __init__(self):
	
		try : 
			tmp_file = open("config/formations.pkl", "rb")
			self.formations = pickle.load(tmp_file)
			tmp_file.close()
		except:
			self.formations = {"Üçgen" : 3, "Kare" : 4 , "Beşgen " : 5 , "Altıgen" : 6 , "Yedigen" : 7 , "Sekizgen" : 8, "Dokuzgen" : 9 , "Ongen" : 10}
		try : 
			tmp_file = open("config/trajectories.pkl", "rb")
			self.trajectories = pickle.load(tmp_file)
			tmp_file.close()
		except:
			self.trajectories = {}

		


	def AddFormation(self , name , dronePoses) :
		self.formations[name] = dronePoses
formations = Formations()

