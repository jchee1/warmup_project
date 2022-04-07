# warmup_project

Drive_square:
The task was to get the turtlebot to drive in a square path. My approach
was to use a timing method: it would move forward for a couple of seconds
and then it would make a 90 degree turn and then repeat.

A majority of my functionality is in the run function of the Square class.
I would set the rospy rate to 5 Hz. Then in my while loop, I set a Twist
with a positive linear x direction to move the turtlebot forward. 
I publish this over and over again in a for loop where I set the range to 10. This would then mean that it would publish this for 2 seconds (5 hz / 10 = 0.5 hz = 2 seconds) For turning the bot, I set the angular velocity to 0.785, which is 45 degrees per second. I then publish this in another for loop that would do this for 2 seconds, which then in theory should turn the bot at 90 degrees.

https://user-images.githubusercontent.com/60594579/161670524-1309c007-8dae-4d7d-8324-7369e5a3c1a9.mov

Person follower:
The task was to get the turtlebot to follow a person or the closest object while mainting a safe distance. My approach was to first check whether if something was directly in front of the robot. If there is, then the bot would move forward. I would then go through turning the bot if the person is not directly in front of the person. I would get the 3 smallest nonzero values in the /scan ranges to signify the distance of the closest object/person. The reason I did it this way vs. just using the ranges.min value was to help alleviate noise. I then got the indexes of each of those 3 values to get the angles the distances corresponded to. I then took the average distance value and the angle index of these 3 ranges. Based on the angle, I would then update the angular velocity to turn the bot.  

Essentially all of my logic is in the process_point function, which is the callback function for the \scan subscriber. The first conditional checks if the bot is close enough to the person and determines if it should stop. The next conditional check if the person is directly in front of the bot and would move forward if they are. The next chunk gets the 3 smallest nonzero values of ranges and takes the average of those values and the average of their angle indexes. Then I check if the average angle is less than 180, indicating the bot to turn left, and would update the angular velocity at different speeds based on the angle (and same thing for turning right for angles greater than equal to 180).