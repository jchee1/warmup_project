#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist

class Square(object):

    def __init__(self):
        rospy.init_node('set_vl')
        self.vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

    def run(self):
        
        #set rate to 5 hz
        r = rospy.Rate(5)
        while not rospy.is_shutdown():
            #set initial speed to go straight forward to x dir
            go_for = Twist()        
            go_for.linear.x = 6

            #publish move forward for couple of seconds
            for _ in range(10):
                self.vel_pub.publish(go_for)
                r.sleep()
            turn = Twist()
            turn.angular.z = 0.785 #45 degrees/s
            for _ in range(10):
                self.vel_pub.publish(turn)
                r.sleep()
            
if __name__ == '__main__':
    node = Square()
    node.run()