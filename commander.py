import datetime
import time
import logging
from typing import Dict
import collections
import threading

import cflib.crtp
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.swarm import CachedCfFactory
from swarm import Swarm
from cflib.crazyflie.syncLogger import SyncLogger

from uav import *
from groups import *

import math
import traceback
import subprocess, sys

# Change uris and sequences according to your setup
logging.basicConfig(level=logging.ERROR)

deques = [collections.deque(maxlen=1)] * 3
logs = [""]*MAX_UAV_NUMBER

def Pos_thread(sequence):
	append = sequence[0]
	process = sequence[1]
	error_count = 0
	while 1:
		x = datetime.datetime.now()
		for line in iter(process.stdout.readline, ""):
			lst = line.split("/")[1:]
			uav_list[int(lst[0])-1].UpdatePose(	float(lst[1]),
												float(lst[2]),
												float(lst[3]))

		print("ERROR: Cannot read UAV Pose. Trying again.")
		error_count+=1
		# If the error continues, shut down the thread
		if error_count > 10000:
			break
	print("ERROR: UAV Pose cannot be read, closing thread.")

class Commander:
	def InitSwarm(self,uris):
		self.seq_args = {}
		
		self.pose_args = {}
		cflib.crtp.init_drivers(enable_debug_driver=False)
		for uri in range(len(uris)):
			self.seq_args[uris[uri]] = [[uri]]
			p = subprocess.Popen("stdbuf -o0 python poses.py" + " {}".format(uri+1), shell=True, stdout=subprocess.PIPE, universal_newlines=True) 
			self.pose_args[uris[uri]] = [[deques[uri],p]]
			t = threading.Thread(target = Pos_thread,args = ([uri,p],))
			t.start()

		factory = CachedCfFactory(rw_cache='./cache')


		with Swarm(uris, factory=factory) as swarm:

			swarm.parallel(wait_for_param_download)

			#swarm.parallel(Pos_thread,args_dict = self.pose_args)

			swarm.parallel(run_sequence , args_dict = self.seq_args )


	
def land(cf,DroneID ,height = 0.1,time1 = 0.5):
	landTime = time.time() + time1
	uav_list[DroneID].SetDest(uav_list[DroneID].PoseX(),uav_list[DroneID].PoseY() , height)
	while uav_list[DroneID].PoseZ() > 0.2 :
		speed = uav_list[DroneID].calculate_speed()
		cf.commander.send_velocity_world_setpoint(speed[0], speed[1], speed[2], 0)


def wait_for_param_download(scf):
	while not scf.cf.param.is_updated:
		time.sleep(1.0)
	print('Parameters downloaded for', scf.cf.link_uri)

def run_sequence(scf,sequence):
	
	try:	
		cf = scf.cf
		
		while cf.is_connected() == False:
			time.sleep(0.01)

		### LOG INFOS (Konum ve Batarya çek)
		lg_stab = LogConfig(name='log', period_in_ms=10)
		lg_stab.add_variable('stateEstimate.x', 'float')
		lg_stab.add_variable('stateEstimate.y', 'float')
		lg_stab.add_variable('stateEstimate.z', 'float')
		lg_stab.add_variable('pm.vbat' , 'float')

		logger = SyncLogger(scf, lg_stab)
		logger.connect()
		info = logger._queue.get()[1]
		### LOG INFOS

		DroneID = sequence[0]

	
		uav_list[DroneID].info["Aktif"] = "Evet"

		uav_list[DroneID].SetDest(uav_list[DroneID].PoseX() , uav_list[DroneID].PoseY(),1.0)
		#print(uav_list[DroneID].dest)
		charging_problem = 0
		while uav_list[DroneID].info["Aktif"] == "Evet":
			info = logger._queue.get()[1]
			#uav_list[DroneID].UpdatePose(info["stateEstimate.x"],info["stateEstimate.y"],info["stateEstimate.z"],info["pm.vbat"])
			uav_list[DroneID].info["Batarya"] = info["pm.vbat"]

			charge_percent = (info["pm.vbat"] - 3.0) / (4.23 - 3.0) # https://forum.bitcraze.io/viewtopic.php?t=732
			if charge_percent < 15:
				charging_problem+=1
				if charging_problem > 1e6:
					print("Crazyflie {} has {}%% battery left, landing.".format(DroneID,charge_percent))
					uav_list[DroneID].info["Aktif"] = "Hayır"
					land(cf,DroneID)
			
			speed = uav_list[DroneID].calculate_speed()
			logs[DroneID] += str(uav_list[DroneID].PoseX()) + "," + str(uav_list[DroneID].PoseY()) + "," + str(uav_list[DroneID].PoseZ()) + "," + str(speed[0]) + "," + str(speed[1]) + "," + str(speed[2]) + "\n"
			#print(DroneID,[ "pos = " ,uav_list[DroneID].PoseX() ,uav_list[DroneID].info["Y"],uav_list[DroneID].info["Z"]] ,speed)
			cf.commander.send_velocity_world_setpoint(speed[0], speed[1], speed[2], 0)

		

		land(cf , DroneID)

			

		

		#self.Land(cf,DroneID)
	except Exception as e:
		print(e)
		traceback.print_exc()		
	



commander = Commander()
