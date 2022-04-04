#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan


class PersonFollower(object):

    def __init__(self):
        rospy.init_node('person_follow')
        self.vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.scan_pub = rospy.Subscriber('/scan', LaserScan, self.process_point)
        self.go_forward = 6

    def process_point(self, data):
        #go through ranges and see where value is less than 5
        #index of that value in ranges list correspond to angle we need to change 

        #check to see if straight ahead, if it is, then just go forward
        if data.ranges[0] <= 5:
            go_for = Twist()
            go_for.linear.x = self.go_forward
            self.vel_pub.publish(go_for)
            return

        for angle, dist in enumerate(data.ranges):
            if dist <= 5:
                #update movement in robot
                update = Twist()
                if angle < 180:
                    update.angular.z = -1.57
                else:
                    update.angular.z = 1.57
                self.vel_pub.publish(update)
                return
                


    def run(self):
        rospy.spin()
        
            
if __name__ == '__main__':
    node = PersonFollower()
    node.run()