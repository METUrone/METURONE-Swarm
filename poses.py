import rospy
from geometry_msgs.msg import PoseStamped
from copy import deepcopy
import time
import os
import sys


def Store(data, args):
	out = "/"+str(args)+"/"+str(data.pose.position.x)+"/"+str(data.pose.position.y)+"/"+str(data.pose.position.z)+"/"+ str(data.pose.orientation.x)+"/"+ str(data.pose.orientation.y)+"/"+ str(data.pose.orientation.z)+"/"+ str(data.pose.orientation.w)

	print(out)
	time.sleep(0.0001)

if __name__ == "__main__":

	uav_num = sys.argv[1]

	rospy.init_node("poseStore{}".format(uav_num))

	rospy.Subscriber("/mocap_node/Robot_{}/pose".format(uav_num), PoseStamped, Store, (uav_num), queue_size=3)

	
	rospy.spin()
