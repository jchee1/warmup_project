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

https://user-images.githubusercontent.com/60594579/162107616-f8812ea1-cd37-4fd1-8dd8-561863e7b7d8.mov

Wall follower:

The task was to have the turtlebot navigate close to the wall and drive alongside it while handling corners. My approach was to use proportional control (Kp*e(t)) on the angular velocity. I wanted the bot to follow the wall on its left side. The error difference is then the difference between the desired angle of the closest object of the bot, which is 90, and the sensor angle. I set the Kp constant to an arbitrary value and updated it as I tested it. 

Again, all of my logic is in the callback function for the \scan subscriber. The first conditional checks if something is directly in front of the turtlebot (within distance of 0.40 and 0.50). If there is, the bot would stop and turn right. This conditional is for handling the case if the bot has to make an inward corner turn. The second conditional checks if something is directly to the left of the bot, which is for handling the case of following the wall. If there is, the angular velocity would be 0 and would just move forward. The next portion is the same as person_follower of getting the average closest distance and angle from the ranges scan. I then have another conditional to check if the angle of the average closest distance is between 90 and 180, which would then slow down the bots linear velocity. This is to help the bot handle outward corners. Finally, the proportional control is then used to set the bot's angular velocity.



Challenges:

I found the main challenge of this project was understanding the ranges of the data for person and wall follower and how those ranges would affect the turtlebot's movement. When I first started working on the calback function for the \scan with the person follower, I tried to go through each of the ranges in a for loop, but I realized I only need the smallest nonzero value of the range list. Thus, I then implemented my logic for getting the average closest distance and angle. 

Future work:

For the person follower, my current implementation stops and whenever it turns. I would like to improve upon it by doing smooth turns (i.e. the turtlebot would not stop whenever it turns to face the person). For the wall follower, I only have the bot follow the wall if it's on the left side, but I would've liked to impelement a more generic script that could apply to both if the wall was on the left and right side. 

Takeaways:

One of my takeaways from the project is working in bject-oriented programming in ROS. This was especially useful when organizing the callback function for the \scan subscriber and when coding more complex behavior in future projects.

Another takeaway was working with the \scan and the \cmd_vel topics. THese were essential as they controlled how the turtlebot moves and the sensor readings which would affect the turtlebot's actions. 