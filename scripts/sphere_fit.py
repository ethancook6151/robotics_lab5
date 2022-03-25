#!/usr/bin/env python3
import rospy
import numpy as np
import cv2
import math
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from robot_vision_lectures.msg import XYZarray 
from robot_vision_lectures.msg import SphereParams

data_done = False
xyz_data = XYZarray
sphere_data = SphereParams

# get the image message
def get_data(data):
	solve_A_B(data.points)
	
	
def solve_A_B(points):
	A = []
	B = []
	for i in range(len(points)):
		At = []
		x, y, z = points[i].x, points[i].y, points[i].z
		At.append(2*x)
		At.append(2*y)
		At.append(2*z) 
		At.append(1)
		A.append(At)
		B.append(x**2 + y**2 + z**2)
	
	get_sphere_data(A,B)
	
	
def get_sphere_data(A,B):
	p = np.linalg.lstsq(A, B, rcond=None)[0]
	xc, yc, zc, p3 = p[0], p[1], p[2], p[3]
	r = math.sqrt(p3 + xc**2 + yc**2 + zc**2)
	sphere_data.xc = xc
	sphere_data.yc = yc
	sphere_data.zc = zc 
	sphere_data.radius = r
	data_done = True

if __name__ == '__main__':
	# define the node and subcribers and publishers
	rospy.init_node('sphere_fit', anonymous = True)
	# define a subscriber to ream images
	img_sub = rospy.Subscriber("/xyz_cropped_ball", XYZarray, get_data) 
	# define a publisher to publish images
	sphere_pub = rospy.Publisher('/sphere_params', SphereParams, queue_size = 1)
	
	# set the loop frequency
	rate = rospy.Rate(10)

	while not rospy.is_shutdown():
		if data_done: 
			sphere_pub.publish(sphere_data)
		rate.sleep()

