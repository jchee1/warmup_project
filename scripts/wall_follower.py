#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
import numpy as np


class WallFollower(object):

    def __init__(self):
        rospy.init_node('wall_follow')
        self.vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.scan_sub = rospy.Subscriber('/scan', LaserScan, self.callback)
        self.twist = Twist()
        

    def callback(self, data):

        distance = 0.3
        front_ranges = data.ranges[0:10] + data.ranges[350:360]
        left_ranges = data.ranges[80:110]
        fm = np.min(front_ranges[np.nonzero(front_ranges)]) #FIX to do nonzero
        lm = min(left_ranges[np.nonzero(left_ranges)])
        #turn 
        if data.ranges[0] <= distance+0.05 and data.ranges[0] >= distance-0.05 and data.ranges[0] > 0.0:
            print("something ahead, turning left")
            move = Twist()

            move.linear.x = 0
            move.angular.z = -0.2
            self.vel_pub.publish(move)
            return
        #follow along wall
        if data.ranges[90] <= distance+0.05 and data.ranges[90] >= distance-0.05 and data.ranges[90] > 0.0:
            print("something ahead, turning left")
            move = Twist()
            move.linear.x = 0.1
            move.angular.z = 0
            self.vel_pub.publish(move)
            return
        
        move = Twist()
        move.linear.x = 0.1
        
        #logic to get avg closest from scan
        sort_ranges = sorted(data.ranges)
        closest = []
        #find 3 smallest nonzero ranges
        for i in sort_ranges:
            if len(closest) >= 3:
                break
            if i > 0.0:
                closest.append(i)
        print("Closest:", closest)

        #to help control for noise, take avg distance and angles of 3 smallest ranges
        avg_closest = sum(closest) / len(closest)
        avg_ang = 0

        for dist in closest:
            angle = data.ranges.index(dist)
            avg_ang += angle
        avg_ang = avg_ang // len(closest)


        move.angular.z = -(90 - avg_ang) * 0.05
        print("linear x:", move.linear.x)
        print("angular z:", move.angular.z)

        self.vel_pub.publish(move)

    def run(self):
        rospy.spin()
        
            
if __name__ == '__main__':
    node = WallFollower()
    node.run()