/***********************************************************************
 * Exp2_DriveForward -- RedBot Experiment 2
 * 
 * Drive forward and stop.
 * 
 * Hardware setup:
 * The Power switch must be on, the motors must be connected, and the board must be receiving power 
 * from the battery. The motor switch must also be switched to RUN.
 *
 * 23 Sept 2013 N. Seidle/M. Hord
 * 04 Oct 2014 B. Huang
 ***********************************************************************/

#include <RedBot.h>  // This line "includes" the RedBot library into your sketch.
// Provides special objects, methods, and functions for the RedBot.

RedBotMotors motors; // Instantiate the motor control object. This only needs
// to be done once.

void setup()
{
  motors.rightMotor(255);   // Turn on Left and right motors at full speed forward.
  delay(2000);         // Waits for 2 seconds
  motors.brake();       // Stops both motors
  motors.leftMotor(255);
  delay(2000);
  motors.brake();
}

void loop()
{
  // Nothing here. We'll get to this in the next experiment.
}


