



## Calculations

### Vector Calculations

We need special math to calculate how our 

* asteroids move

Each asteroid has a velocity associated with it.
Velocity is speed + direction.
The direction will be just like turtle.  

* A degree between 0 and 360.
* 0 will be towards the top of the screen (the same direction that the space ship faces)
* 180 will be towards the bottom of the screen
* 90 will be towards the right of the screen
* 270 will be towards the left of the screen

It isn't interesting if our ship can only go in these 4 directions (like snake)


So we need other angles.

To do this we need math called "Trigonometry"

Here is a website on how we can calculate what we want.

Given an angle, we want to determine, how much x and y to change
each time the game clock advances.
This new x,y will be how much the asteroid moves.


Note - We could skip all of this... by just calculating the values upfront instead of doing the calculation everytime.

But since we are building this game, and i think the math behind this is interesting... we're building it... the HARD way!

Check out this page for how we might do this:

https://www.mathsisfun.com/polar-cartesian-coordinates.html

### Collision Calculations