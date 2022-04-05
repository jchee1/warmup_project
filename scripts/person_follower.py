#!/usr/bin/env python3

from soupsieve import closest
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan


class PersonFollower(object):

    def __init__(self):
        rospy.init_node('person_follow')
        self.vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.scan_sub = rospy.Subscriber('/scan', LaserScan, self.process_point)
        self.twist = Twist()

    def process_point(self, data):

        #check to stop robot if close enough
        if data.ranges[0] <= 0.4 and data.ranges[0] > 0.0:  
            print("stop")    
            self.twist.linear.x = 0.0
            self.twist.angular.z = 0
            self.vel_pub.publish(self.twist)
            return
        
        #check to see if straight ahead, if it is, then just go forward
        if data.ranges[0] <= 2.0 and data.ranges[0] > 0.0:  
            print("moving forward")    
            self.twist.linear.x = 0.3
            self.twist.angular.z = 0
            self.vel_pub.publish(self.twist)
            return
        
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
        avg_closest = sum(closest) / 3
        avg_ang = 0

        for dist in closest:
            angle = data.ranges.index(dist)
            avg_ang += angle
        avg_ang = avg_ang / 3

        if avg_ang < 180: #turn left
            print('turning left')
            self.twist.linear.x=0
            if avg_ang <= 30: 
                self.twist.angular.z = 0.3
            elif avg_ang <= 60:
                self.twist.angular.z = 0.5
            elif avg_ang <= 90:
                self.twist.angular.z = 0.7
            elif avg_ang <= 120:
                self.twist.angular.z = 0.9
            elif avg_ang <= 150:
                self.twist.angular.z = 1.1
            else:
                self.twist.angular.z = 1.3
                
        else: #turn right
            print("turning right")
            self.twist.linear.x=0
            if avg_ang <= 210: 
                self.twist.angular.z = -0.3
            elif avg_ang <= 240:
                self.twist.angular.z = -0.5
            elif avg_ang <= 270:
                self.twist.angular.z = -0.7
            elif avg_ang <= 300:
                self.twist.angular.z = -0.9
            elif avg_ang <= 330:
                self.twist.angular.z = -1.1
            else:
                self.twist.angular.z = -1.3
        self.vel_pub.publish(self.twist)
        

    def run(self):
        rospy.spin()
        
            
if __name__ == '__main__':
    node = PersonFollower()
    node.run()