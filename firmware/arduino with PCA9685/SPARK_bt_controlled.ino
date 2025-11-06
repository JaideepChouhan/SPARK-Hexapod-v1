// Jai Shree Ram

#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();
int pos0 = 102, pos180 = 512, i, j;
int kneeCenter = 80;
int thighThreshold = 20; // threshold of the moment of thigh (20 degree)
int thighLowest = 90 - thighThreshold; // Lowest point of the thigh moment
int thighHighest = 90 + thighThreshold; // Highest point of the thigh moment
int center = 90; // center of the thigh
int lowest = 5; // lowest point of the moment
int power = 8; // power pin to power the HC05 Module

int st1 = 1, st2 = 2, st3 = 3, st4 = 4, st5 = 5, st6 = 6, sk1 = 7, sk2 = 8, sk3 = 9, sk4 = 10, sk5 = 11, sk6 = 12;
char cmd; // received command in cmd

// *******************void setup()*************

void setup() {
  Serial.begin(9600);
  pwm.begin();
  pwm.setPWMFreq(50);
  pinMode(power, OUTPUT);
  digitalWrite(power, HIGH);
  delay(20);
}
// *************************void loop()******************
void loop()
{
  if (Serial.available())
  {
    cmd = Serial.read(); // take commands from the Serial commmunication in cmd
    switch (cmd)
    {
      case 'F': // Forward button
        Walk_Forward();
      case 'B': // Backward button
        Walk_Backward();
      case 'L': // Left side turn
        turnL();
      case 'R': // Right side turn
        turnR();
      case '1':
        kneeCenter = 5; break;
      case '2':
        kneeCenter = 15; break;
      case '3':
        kneeCenter = 25; break;
      case '4':
        kneeCenter = 35; break;
      case '5':
        kneeCenter = 45; break;
      case '6':
        kneeCenter = 55; break;
      case '7':
        kneeCenter = 65; break;
      case '8':
        kneeCenter = 75; break;
      case '9':
        kneeCenter = 80; break;
      case 'q': // Max speed
        kneeCenter = 80; break;
      default : hm(); break;
    }
  } else {
    hm();
  }
}

    // ******************Function for the servoWrite *************

    void servoWrite(int servo, int angle)  // servoWrite(pin address of servo, angle to write)
    {
      int duty;  // converted frequency according to angle required
      duty = map(angle, 0, 180, pos0, pos180);
      pwm.setPWM(servo, 0, duty);
    }

    // *********************stand position***********************

    void hm() {
      servoWrite(st1, center);
      servoWrite(st2, center);
      servoWrite(st3, center);
      servoWrite(st4, center);
      servoWrite(st5, center);
      servoWrite(st6, center);
      servoWrite(sk1, kneeCenter);
      servoWrite(sk2, kneeCenter);
      servoWrite(sk3, kneeCenter);
      servoWrite(sk4, kneeCenter);
      servoWrite(sk5, kneeCenter);
      servoWrite(sk6, kneeCenter);
      delay(2);
    }

    // ********************************* Walk_Forward() *********************

    void Walk_Forward() {
      for (i = kneeCenter; i >= lowest; i--) {
        servoWrite(sk2, i);
        servoWrite(sk4, i);
        servoWrite(sk6, i);
        delay(6);
      }
      for (i = center, j = center; i >= thighLowest ; i--, j++) {
        servoWrite(st1, i);
        servoWrite(st3, i);
        servoWrite(st5, j);
        delay(6);
      }
      for (i = lowest; i <= kneeCenter; i++) {
        servoWrite(sk2, i);
        servoWrite(sk4, i);
        servoWrite(sk6, i);
        delay(6);
      }
      for (i = kneeCenter; i >= lowest; i--) {
        servoWrite(sk1, i);
        servoWrite(sk3, i);
        servoWrite(sk5, i);
        delay(6);
      }
      for (i = thighLowest, j = thighHighest; i <= center; i++, j--) {
        servoWrite(st1, i);
        servoWrite(st3, i);
        servoWrite(st5, j);
        delay(6);
      }
      for (i = center, j = center; i <= thighHighest; i++, j--) {
        servoWrite(st4, i);
        servoWrite(st6, i);
        servoWrite(st2, j);
        delay(6);
      }
      for (i = lowest; i <= kneeCenter; i++) {
        servoWrite(sk1, i);
        servoWrite(sk3, i);
        servoWrite(sk5, i);
        delay(6);
      }
      for (i = thighHighest, j = thighLowest; i >= center; i--, j++) {
        servoWrite(st4, i);
        servoWrite(st6, i);
        servoWrite(st2, j);
        delay(6);
      }
    }

    //****************************** Walk_Backward() **********

    void Walk_Backward() {
      for (i = kneeCenter; i >= lowest; i--) {
        servoWrite(sk2, i);
        servoWrite(sk4, i);
        servoWrite(sk6, i);
        delay(6);
      }
      for (i = center, j = center; i <= thighHighest; i++, j--) {
        servoWrite(st1, i);
        servoWrite(st3, i);
        servoWrite(st5, j);
        delay(6);
      }
      for (i = lowest; i <= kneeCenter; i++) {
        servoWrite(sk2, i);
        servoWrite(sk4, i);
        servoWrite(sk6, i);
        delay(6);
      }
      for (i = kneeCenter; i >= lowest; i--) {
        servoWrite(sk1, i);
        servoWrite(sk3, i);
        servoWrite(sk5, i);
        delay(6);
      }
      for (i = thighHighest, j = thighLowest; i >= center; i--, j++) {
        servoWrite(st1, i);
        servoWrite(st3, i);
        servoWrite(st5, j);
        delay(6);
      }
      for (i = center, j = center; i >= thighLowest; i--, j++) {
        servoWrite(st4, i);
        servoWrite(st6, i);
        servoWrite(st2, j);
        delay(6);
      }
      for (i = lowest; i <= kneeCenter; i++) {
        servoWrite(sk1, i);
        servoWrite(sk3, i);
        servoWrite(sk5, i);
        delay(6);
      }
      for (i = thighLowest, j = thighHighest; i <= center; i++, j--) {
        servoWrite(st4, i);
        servoWrite(st6, i);
        servoWrite(st2, j);
        delay(6);
      }
    }

    // ***************************************** turn Left ********************
    void turnL() {
      for (i = kneeCenter; i >= lowest; i--) {
        servoWrite(sk1, i);
        servoWrite(sk3, i);
        servoWrite(sk5, i);
        delay(6);
      }
      for (i = center; i >= thighLowest; i--) {
        servoWrite(st1, i);
        servoWrite(st3, i);
        servoWrite(st5, i);
        delay(6);
      }
      for (i = lowest; i <= kneeCenter; i++) {
        servoWrite(sk1, i);
        servoWrite(sk3, i);
        servoWrite(sk5, i);
        delay(6);
      }
      for (i = kneeCenter; i >= lowest; i--) {
        servoWrite(sk2, i);
        servoWrite(sk4, i);
        servoWrite(sk6, i);
        delay(6);
      }
      for (i = thighLowest; i < center; i++)
      {
        servoWrite(st1, i);
        servoWrite(st3, i);
        servoWrite(st5, i);
        delay(6);
      }
      for (i = center; i >= thighLowest; i--) {
        servoWrite(st2, i);
        servoWrite(st4, i);
        servoWrite(st6, i);
        delay(6);
      }
      for (i = lowest; i <= kneeCenter; i++) {
        servoWrite(sk2, i);
        servoWrite(sk4, i);
        servoWrite(sk6, i);
        delay(6);
      }
    }

    // ************************************************ turn Right ********

    void turnR() {
      for (i = kneeCenter; i >= lowest; i--) {
        servoWrite(sk1, i);
        servoWrite(sk3, i);
        servoWrite(sk5, i);
        delay(6);
      }
      for (i = center; i <= thighHighest; i++) {
        servoWrite(st1, i);
        servoWrite(st3, i);
        servoWrite(st5, i);
        delay(6);
      }
      for (i = lowest; i <= kneeCenter; i++) {
        servoWrite(sk1, i);
        servoWrite(sk3, i);
        servoWrite(sk5, i);
        delay(6);
      }
      for (i = kneeCenter; i >= lowest; i--) {
        servoWrite(sk2, i);
        servoWrite(sk4, i);
        servoWrite(sk6, i);
        delay(6);
      }
      for (i = thighHighest; i > center; i--)
      {
        servoWrite(st1, i);
        servoWrite(st3, i);
        servoWrite(st5, i);
        delay(6);
      }
      for (i = center; i <= thighHighest; i++) {
        servoWrite(st2, i);
        servoWrite(st4, i);
        servoWrite(st6, i);
        delay(6);
      }
      for (i = lowest; i <= kneeCenter; i++) {
        servoWrite(sk2, i);
        servoWrite(sk4, i);
        servoWrite(sk6, i);
        delay(6);
      }
    }
