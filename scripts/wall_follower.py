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
        

    def callback(self, data):

        distance = 0.4

        #TODO: figure out what robot should do to find wall

        #turn on inward corner
        if data.ranges[0] <= distance + 0.05 and data.ranges[0] >= distance - 0.05 and data.ranges[0] > 0.0:
            print("something ahead, turning right")
            move = Twist()
            move.linear.x = 0
            move.angular.z = -0.6
            self.vel_pub.publish(move)
            return
        #follow along wall that's on left side
        if data.ranges[90] <= distance + 0.05 and data.ranges[90] >= distance - 0.05 and data.ranges[90] > 0.0:
            print("following wall")
            move = Twist()
            move.linear.x = 0.1
            move.angular.z = 0
            self.vel_pub.publish(move)
            return
        
        move = Twist()
        
        
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
        avg_ang = avg_ang / len(closest)

        move.linear.x = 0.15
        if avg_ang > 90 and avg_ang < 180:
            print("cond: in corner turns")
            move.linear.x = 0.1
            #move.angular.z = 0.6
        
        #proportional control
        move.angular.z = -(90 - avg_ang) * 0.08
        
        #print("linear x:", move.linear.x)
        print("avg_ang:", avg_ang)
        print("angular z:", move.angular.z)

        self.vel_pub.publish(move)

    def run(self):
        rospy.spin()
        
            
if __name__ == '__main__':
    node = WallFollower()
    node.run()