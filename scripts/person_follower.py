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
        #go through ranges and see where value is less than 5
        #index of that value in ranges list correspond to angle we need to change 

        #check to see if straight ahead, if it is, then just go forward
        #print("ranges:", data.ranges)
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

        for dist in closest:
            angle = data.ranges.index(dist)
            if angle < 180:
                    print('turning left')
                    self.twist.linear.x=0
                    if angle <= 30: 
                        self.twist.angular.z = 0.1
                    elif angle <= 60:
                        self.twist.angular.z = 0.3
                    elif angle <= 90:
                        self.twist.angular.z = 0.5
                    elif angle <= 120:
                        self.twist.angular.z = 0.7
                    elif angle <= 150:
                        self.twist.angular.z = 0.9
                    else:
                        self.twist.angular.z = 1.0
                
            else: #turn right
                print("turning right")
                self.twist.linear.x=0
                if angle <= 210: 
                    self.twist.angular.z = -0.1
                elif angle <= 240:
                    self.twist.angular.z = -0.3
                elif angle <= 270:
                    self.twist.angular.z = -0.5
                elif angle <= 300:
                    self.twist.angular.z = -0.7
                elif angle <= 330:
                    self.twist.angular.z = -0.9
                else:
                    self.twist.angular.z = -1.0
            self.vel_pub.publish(self.twist)
            return


        
        print("nothing in range")
        #case where nothing is in range => just move forward
        self.twist.linear.x = 0.3
        self.vel_pub.publish(self.twist)

        #TODO: stop at certain dist from person

    def run(self):
        rospy.spin()
        
            
if __name__ == '__main__':
    node = PersonFollower()
    node.run()