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

