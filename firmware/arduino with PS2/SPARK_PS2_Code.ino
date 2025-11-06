// JAI SHREE RAM...

        /* 
         *  Front Lights On = W = Auto drive mode on for forward walk 
         *  Front Lights Off = w = Auto drive mode off for forward walk 
         *  Back Lights On = U = Auto drive mode on for backward walk 
         *  Back Lights Off = u = Auto drive mode off for backward walk
         *  
         *  D8 is at HIGH always: D8 = 5V pin 
         */

#include <Adafruit_PWMServoDriver.h>
#include <PS2X_lib.h>  //for v1.6

PS2X ps2x; // create PS2 Controller Class

int error = 0; 
byte type = 0;
byte vibrate = 0;

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();
int pos0 = 102, pos180 = 512, i, j, button = 0;
int kneeCenter = 45,thighCenter = 90-kneeCenter;
int st1 = 1, st2 = 2, st3 = 3, st4 = 4, st5 = 5, st6 = 6, sk1 = 7, sk2 = 8, sk3 = 9, sk4 = 10, sk5 = 11, sk6 = 12;
char cmd,cond;

void setup() {
  
  Serial.begin(9600);
  pinMode(4,OUTPUT);
  pinMode(5,OUTPUT);
  pinMode(6,OUTPUT);
  
  error = ps2x.config_gamepad(10,12,11,13, false, false);   //setup pins and settings:  GamePad(clock, command, attention, data, Pressures?, Rumble?) check for error
  
  if(error == 0){
    Serial.println("Found Controller, configured successful");
    Serial.println("Try out all the buttons, X will vibrate the controller, faster as you press harder;");
    Serial.println("holding L1 or R1 will print out the analog stick values.");
    Serial.println("Go to www.billporter.info for updates and to report bugs.");
  }
   
  else if(error == 1)
    Serial.println("No controller found, check wiring, see readme.txt to enable debug. visit www.billporter.info for troubleshooting tips");
   
  else if(error == 2)
    Serial.println("Controller found but not accepting commands. see readme.txt to enable debug. Visit www.billporter.info for troubleshooting tips");
   
  else if(error == 3)
    Serial.println("Controller refusing to enter Pressures mode, may not support it. ");
   
  type = ps2x.readType(); 
    
  switch(type) {
    case 0:
      Serial.println("Unknown Controller type");
      break;
    case 1:
      Serial.println("DualShock Controller Found");
      break;
    case 2:
      Serial.println("GuitarHero Controller Found");
      break;
    default:
      break;
  }
  pwm.begin();
  pwm.setPWMFreq(50);
  pinMode(8,OUTPUT);
  digitalWrite(8,HIGH);
  delay(200);
}

void loop() {

ps2x.read_gamepad(false, vibrate);          //read controller and set large motor to spin at 'vibrate' speed
    
    if(ps2x.Button(PSB_START)) {                   //will be TRUE as long as button is pressed
      Serial.println("Start is being held");
    }
    if(ps2x.Button(PSB_SELECT)) {
      Serial.println("Select is being held");
    }
    if(ps2x.Button(PSB_PAD_UP)) {         //will be TRUE as long as button is pressed
     // Serial.println("UP is being held");
      Walk_Forward();
      Serial.println("Walking Forward**");
    }
    if(ps2x.Button(PSB_PAD_RIGHT)){
     // Serial.println("Right is being held");
      turnR();
      Serial.println("turning Right**");
    }
    if(ps2x.Button(PSB_PAD_LEFT)){
     // Serial.println("LEFT is being held");
      turnL();
      Serial.println("turning Left**");
    }
    if(ps2x.Button(PSB_PAD_DOWN)){
      //Serial.println("DOWN is being held");
      Walk_Backward();
      Serial.println("Walking Backward**");
    }
    if( ps2x.Button(PSB_PAD_UP) &&  ps2x.Button(PSB_PAD_RIGHT))
    {
      Walk_Right_Forward();
      Serial.println("Walking Right Forward**");
    }
    if( ps2x.Button(PSB_PAD_UP) &&  ps2x.Button(PSB_PAD_LEFT))
    {
      Walk_Left_Forward();
      Serial.println("Walking Left Forward**");
    }
        if( ps2x.Button(PSB_PAD_DOWN) &&  ps2x.Button(PSB_PAD_RIGHT))
    {
      Walk_Right_Backward();
      Serial.println("Walking Right Backward**");
    }
    if( ps2x.Button(PSB_PAD_DOWN) &&  ps2x.Button(PSB_PAD_LEFT))
    {
      Walk_Left_Backward();
      Serial.println("Walking Left Backward**");
    }
    
    if (ps2x.NewButtonState())               //will be TRUE if any button changes state (on to off, or off to on)
    {
        if(ps2x.Button(PSB_L3))
          Serial.println("L3 pressed");
        if(ps2x.Button(PSB_R3))
          Serial.println("R3 pressed");
        if(ps2x.Button(PSB_L2))
          Serial.println("L2 pressed");
        if(ps2x.Button(PSB_R2))
          Serial.println("R2 pressed");
    }   
         
    if(ps2x.ButtonPressed(PSB_RED))             //will be TRUE if button was JUST pressed
          Serial.println("Moving in Right Side");
          
    if(ps2x.ButtonReleased(PSB_RED))             //will be TRUE if button was JUST released
          Serial.println("Stoped");

    if(ps2x.ButtonPressed(PSB_PINK))             //will be TRUE if button was JUST pressed
          Serial.println("Moving in Left Side");
          digitalWrite(5,HIGH);
                  
    if(ps2x.ButtonReleased(PSB_PINK))             //will be TRUE if button was JUST released
          Serial.println("stoped"); 
          digitalWrite(5,LOW);    

    if(ps2x.ButtonPressed(PSB_GREEN))             //will be TRUE if button was JUST pressed
          Serial.println("increasing the kneeCenter value = ");
          /*if (kneeCenter <88){
          kneeCenter = kneeCenter+2;
          thighCenter = 90 - kneeCenter;
          Serial.print(kneeCenter);
          } else {
            Serial.println("Already at max height");
          }*/
                  
    if(ps2x.ButtonReleased(PSB_GREEN))             //will be TRUE if button was JUST released
          Serial.println("stoped");  

    if(ps2x.ButtonPressed(PSB_BLUE))             //will be TRUE if button was JUST pressed
          Serial.println("Decreasing the kneeCenter value = ");
          /*if (kneeCenter > 2) { 
          kneeCenter = kneeCenter-2;
          thighCenter = 90 - kneeCenter;
          Serial.print(kneeCenter);
          } else {
            Serial.println("Already at min height");
          }*/
         
    if(ps2x.ButtonReleased(PSB_BLUE))             //will be TRUE if button was JUST released
         Serial.println("stoped");  
          
    if(ps2x.Button(PSB_L1) || ps2x.Button(PSB_R1)) // print stick values if either is TRUE
    {
        Serial.print("Stick Values:");
        Serial.print(ps2x.Analog(PSS_LY), DEC); // LY
        Serial.print(",");
        Serial.print(ps2x.Analog(PSS_LX), DEC); // LX
        Serial.print(",");
        Serial.print(ps2x.Analog(PSS_RY), DEC); // RY
        Serial.print(",");
        Serial.println(ps2x.Analog(PSS_RX), DEC); // RX
   }
 delay(50);
 }

void servoWrite(int servo, int angle)  // servoWrite(pin address of servo, angle to write)
{
  int duty;  // converted frequency according to angle required
  duty = map(angle, 0, 180, pos0, pos180);
  pwm.setPWM(servo, 0, duty);
}

// untill it could not get conneted with bluetooth, it will be in it's initial position !
void relax() {
  servoWrite(st1, 90);
  servoWrite(st2, 90);
  servoWrite(st3, 90);
  servoWrite(st4, 90);
  servoWrite(st5, 90);
  servoWrite(st6, 90);
    servoWrite(sk1, kneeCenter);
    servoWrite(sk2, kneeCenter);
    servoWrite(sk3, kneeCenter);
    servoWrite(sk4, kneeCenter);
    servoWrite(sk5, kneeCenter);
    servoWrite(sk6, kneeCenter);
    delay(10);
}

// stand position
void hm() {
  servoWrite(st1, 90);
  servoWrite(st2, 90);
  servoWrite(st3, 90);
  servoWrite(st4, 90);
  servoWrite(st5, 90);
  servoWrite(st6, 90);
    servoWrite(sk1, kneeCenter);
    servoWrite(sk2, kneeCenter);
    servoWrite(sk3, kneeCenter);
    servoWrite(sk4, kneeCenter);
    servoWrite(sk5, kneeCenter);
    servoWrite(sk6, kneeCenter);
    delay(10);
}

// *************** Walk_Forward() *********
void Walk_Forward() {
  for(i = kneeCenter; i >= 5; i--) {
    cmd = Serial.read();
    while (cmd=='F') {
    servoWrite(sk2, i);
    servoWrite(sk4, i);
    servoWrite(sk6, i);
    delay(5);
  }
  }
  for (i = 90, j = 90; i >= 50; i--, j++) {
    cmd = Serial.read();
    while (cmd=='F') {
    servoWrite(st1, i);
    servoWrite(st3, i);
    servoWrite(st5, j);
    delay(5);
  }
  }
  for (i = 5; i <= kneeCenter; i++) {
    cmd = Serial.read();
    while (cmd=='F') {
    servoWrite(sk2, i);
    servoWrite(sk4, i);
    servoWrite(sk6, i);
    delay(5);
  }
  }
  for (i = kneeCenter; i >= 5; i--) {
    cmd = Serial.read();
    while (cmd=='F') {
    servoWrite(sk1, i);
    servoWrite(sk3, i);
    servoWrite(sk5, i);
    delay(5);
  }
  }
  for (i = 50, j = 130; i <= 90; i++, j--) {
    cmd = Serial.read();
    while (cmd=='F') {
    servoWrite(st1, i);
    servoWrite(st3, i);
    servoWrite(st5, j);
    delay(5);
  }
  }
  for (i = 90, j = 90; i <= 130; i++, j--) {
    cmd = Serial.read();
    while (cmd=='F') {
    servoWrite(st4, i);
    servoWrite(st6, i);
    servoWrite(st2, j);
    delay(5);
  }
  }
  for (i = 5; i <= kneeCenter; i++) {
    cmd = Serial.read();
    while (cmd=='F') {
    servoWrite(sk1, i);
    servoWrite(sk3, i);
    servoWrite(sk5, i);
    delay(5);
  }
  }
  for (i = 130, j = 50; i >= 90; i--, j++) {
    cmd = Serial.read();
    while (cmd=='F') {
    servoWrite(st4, i);
    servoWrite(st6, i);
    servoWrite(st2, j);
    delay(5);
  }
  }
  }
//************* Walk_Backward() **********
void Walk_Backward() {
    cmd = Serial.read();
    while (cmd=='B') {
  for (i = kneeCenter; i >= 5; i--) {
    servoWrite(sk2, i);
    servoWrite(sk4, i);
    servoWrite(sk6, i);
    delay(5);
  }
    }
  for (i = 90, j = 90; i <= 130; i++, j--) {
    cmd = Serial.read();
    while (cmd=='B') {
    servoWrite(st1, i);
    servoWrite(st3, i);
    servoWrite(st5, j);
    delay(5);
  }
  }
  for (i = 5; i <= kneeCenter; i++) {
    cmd = Serial.read();
    while (cmd=='B') {
    servoWrite(sk2, i);
    servoWrite(sk4, i);
    servoWrite(sk6, i);
    delay(5);
  }
  }
  for (i = kneeCenter; i >= 5; i--) {
    cmd = Serial.read();
    while (cmd=='B') {
    servoWrite(sk1, i);
    servoWrite(sk3, i);
    servoWrite(sk5, i);
    delay(5);
  }
  }
  for (i = 130, j = 50; i >= 90; i--, j++) {
    cmd = Serial.read();
    while (cmd=='B') {
    servoWrite(st1, i);
    servoWrite(st3, i);
    servoWrite(st5, j);
    delay(5);
  }
  }
  for (i = 90, j = 90; i >= 50; i--, j++) {
    cmd = Serial.read();
    while (cmd=='B') {
    servoWrite(st4, i);
    servoWrite(st6, i);
    servoWrite(st2, j);
    delay(5);
  }
  }
  for (i = 5; i <= kneeCenter; i++) {
    cmd = Serial.read();
    while (cmd=='B') {
    servoWrite(sk1, i);
    servoWrite(sk3, i);
    servoWrite(sk5, i);
    delay(5);
  }
  }
  for (i = 50, j = 130; i <= 90; i++, j--) {
    cmd = Serial.read();
    while (cmd=='B') {
    servoWrite(st4, i);
    servoWrite(st6, i);
    servoWrite(st2, j);
    delay(5);
  }
}
}

// ***************************** turnR() ********
void turnR() {
  for (i = kneeCenter; i >= 5; i--) {
    cmd = Serial.read();
    while (cmd=='L') {
    servoWrite(sk1, i);
    servoWrite(sk3, i);
    servoWrite(sk5, i);
    delay(5);
  }
  }
  for (i = 90; i >= 50; i--) {
    cmd = Serial.read();
    while (cmd=='L') {
    servoWrite(st1, i);
    servoWrite(st3, i);
    servoWrite(st5, i);
    delay(5);
  }
  }
  for (i = 5; i <= kneeCenter; i++) {
    cmd = Serial.read();
    while (cmd=='L') {
    servoWrite(sk1, i);
    servoWrite(sk3, i);
    servoWrite(sk5, i);
    delay(5);
  }
  }
  for (i = kneeCenter; i >= 5; i--) {
    cmd = Serial.read();
    while (cmd=='L') {
    servoWrite(sk2, i);
    servoWrite(sk4, i);
    servoWrite(sk6, i);
    delay(5);
  }
  }
  for (i = 90; i >= 50; i--) {
    cmd = Serial.read();
    while (cmd=='L') {
    servoWrite(st2, i);
    servoWrite(st4, i);
    servoWrite(st6, i);
    delay(5);
  }
  }
  for (i = 5; i <= kneeCenter; i++) {
    cmd = Serial.read();
    while (cmd=='L') {
    servoWrite(sk2, i);
    servoWrite(sk4, i);
    servoWrite(sk6, i);
    delay(5);
  }
  }
}

// ********** turnL() ********
void turnL() {
  for (i = kneeCenter; i >= 5; i--) {
    cmd = Serial.read();
    while (cmd=='R') {
    servoWrite(sk1, i);
    servoWrite(sk3, i);
    servoWrite(sk5, i);
    delay(5);
  }
  }
  for (i = 90; i <= 130; i++) {
    cmd = Serial.read();
    while (cmd=='R') {
    servoWrite(st1, i);
    servoWrite(st3, i);
    servoWrite(st5, i);
    delay(5);
  }
  }
  for (i = 5; i <= kneeCenter; i++) {
    cmd = Serial.read();
    while (cmd=='R') {
    servoWrite(sk1, i);
    servoWrite(sk3, i);
    servoWrite(sk5, i);
    delay(5);
  }
  }
  for (i = kneeCenter; i >= 5; i--) {
    cmd = Serial.read();
    while (cmd=='R') {
    servoWrite(sk2, i);
    servoWrite(sk4, i);
    servoWrite(sk6, i);
    delay(5);
  }
  }
  for (i = 90; i <= 130; i++) {
    cmd = Serial.read();
    while (cmd=='R') {
    servoWrite(st2, i);
    servoWrite(st4, i);
    servoWrite(st6, i);
    delay(5);
  }
  }
  for (i = 5; i <= kneeCenter; i++) {
    cmd = Serial.read();
    while (cmd=='R') {
    servoWrite(sk2, i);
    servoWrite(sk4, i);
    servoWrite(sk6, i);
    delay(5);
  }
}
}
/*
//**************** dance() ********
void dance() {
  for (i = 5; i <= kneeCenter; i++) {
    servoWrite(sk1, i);
    delay(5);
  }
  for (i = kneeCenter; i >= 5; i--) {
    servoWrite(sk4, i);
    delay(5);
  }
  for (i = 5; i <= kneeCenter; i++) {
    servoWrite(sk2, i);
    delay(5);
  }
  for (i = kneeCenter; i >= 5; i--) {
    servoWrite(sk5, i);
    delay(5);
  }
  for (i = 5; i <= kneeCenter; i++) {
    servoWrite(sk3, i);
    delay(5);
  }
  for (i = kneeCenter; i >= 5; i--) {
    servoWrite(sk6, i);
    delay(5);
  }
  for (i = kneeCenter; i >= 5; i--) {
    servoWrite(sk1, i);
    delay(5);
  }
  for (i = 5; i <= kneeCenter; i++) {
    servoWrite(sk4, i);
    delay(5);
  }
  for (i = kneeCenter; i >= 5; i--) {
    servoWrite(sk2, i);
    delay(5);
  }
  for (i = 5; i <= kneeCenter; i++) {
    servoWrite(sk5, i);
    delay(5);
  }
  for (i = kneeCenter; i >= 5; i--) {
    servoWrite(sk3, i);
    delay(5);
  }
  for (i = 5; i <= kneeCenter; i++) {
    servoWrite(sk6, i);
    delay(5);
  }
}

// if bluetooth is not conneted with spark, then it will get fold and it will be it's initial position always.
void fold() {
  i=kneeCenter;
    servoWrite(sk1, i);
    servoWrite(sk2, i);
    servoWrite(sk3, i);
    servoWrite(sk4, i);
    servoWrite(sk5, i);
    servoWrite(sk6, i);
    delay(5); 
 //if ( cond == 'u'){
  for (i = 90; i > 2; i--) {
    servoWrite(st1, i);
    servoWrite(st2, i);
    servoWrite(st3, i);
    servoWrite(st4, i);
    servoWrite(st5, i);
    servoWrite(st6, i);
    delay(5);
  }
}
//if bluetooth is conneted with spark, then it will get unFold and ready to do the actions
void unFold() {
 i = kneeCenter;
    servoWrite(sk1, i);
    servoWrite(sk2, i);
    servoWrite(sk3, i);
    servoWrite(sk4, i);
    servoWrite(sk5, i);
    servoWrite(sk6, i);
    delay(5);
  //if(cond=='f'){
  for (i = 2; i <= 90; i++) {
    servoWrite(st1, i);
    servoWrite(st2, i);
    servoWrite(st3, i);
    servoWrite(st4, i);
    servoWrite(st5, i);
    servoWrite(st6, i);
    delay(5);
  }
}
void nothing()
{
  i=0;
}

//*********** New walking mechanism for SPARK *****************************************

void Walk_Left_Forward()
{
  for (i=kneeCenter;i>=5;i--)
  {
    servoWrite(sk2,i);
    servoWrite(sk4,i);
    servoWrite(sk6,i);
    delay(2);
  }
  for (i=90,j=90;i>=thighCenter;i--,j++)
  {
    servoWrite(st3,i);
    servoWrite(st5,i);
    servoWrite(st1,j);
    delay(2);
  }
  for (i=5;i<=kneeCenter;i++)
  {
    servoWrite(sk2,i);
    servoWrite(sk4,i);
    servoWrite(sk6,i);
    delay(2);    
  }
  for (i=kneeCenter;i>=5;i--)
  {
    servoWrite(sk1,i);
    servoWrite(sk3,i);
    servoWrite(sk5,i);
    delay(2);
  }
  for (i=thighCenter,j=(90+thighCenter);i<=90;i++,j--)
  {
    servoWrite(st3,i);
    servoWrite(st5,i);
    servoWrite(st1,j);
    delay(2);
  }
  for (i=90,j=90;i<=(90+thighCenter);i++,j--)
  {
    servoWrite(st2,i);
    servoWrite(st6,i);
    servoWrite(st4,j);
    delay(2);
  }
  for (i=5;i<=kneeCenter;i++)
  {
    servoWrite(sk1,i);
    servoWrite(sk3,i);
    servoWrite(sk5,i);
    delay(2);    
  }
  for (i=(90+thighCenter),j=thighCenter;i>=90;i--,j++)
  {
    servoWrite(st2,i);
    servoWrite(st6,i);
    servoWrite(st4,j);
    delay(2);
  }
}

void WalK_Right_Forward()
{
 for(i=kneeCenter;i<=5;i--)
 {
  servoWrite(sk2,i);
  servoWrite(sk4,i);
  servoWrite(sk6,i);
  delay(2); 
 }
 for(i=90,j=90;i<=(90+thighCenter);i++,j--);
 {
  servoWrite(st1,i);
  servoWrite(st5,i);
  servoWrite(st3,j);
  delay(2);
 }
 for(i=5;i<=kneeCenter;i++)
 {
  servoWrite(sk2,i);
  servoWrite(sk4,i);
  servoWrite(sk6,i);
  delay(2); 
 }
 for(i=kneeCenter;i<=5;i--)
 {
  servoWrite(sk1,i);
  servoWrite(sk3,i);
  servoWrite(sk5,i);
  delay(2); 
 }
 for(i=(90+thighCenter),j=thighCenter;i>=90;i--,j++);
 {
  servoWrite(st1,i);
  servoWrite(st5,i);
  servoWrite(st3,j);
  delay(2);
 }
 for(i=90,j=90;i>=thighCenter;i--,j++);
 {
  servoWrite(st2,i);
  servoWrite(st4,i);
  servoWrite(st6,j);
  delay(2);
 }
 for(i=5;i<=kneeCenter;i++)
 {
  servoWrite(sk1,i);
  servoWrite(sk3,i);
  servoWrite(sk5,i);
  delay(2); 
 }
 for(i=thighCenter,j=(90+thighCenter);i<=90;i++,j--);
 {
  servoWrite(st2,i);
  servoWrite(st4,i);
  servoWrite(st6,j);
  delay(2);
 }
}
//****** I just changed the i into j and j into i to make the robot walk in oposite direction ** like forward-left into backward-right *******
void Walk_Right_Backward()
{
  for (i=kneeCenter;i>=5;i--)
  {
    servoWrite(sk2,i);
    servoWrite(sk4,i);
    servoWrite(sk6,i);
    delay(2);
  }
  for (i=90,j=90;i>=thighCenter;i--,j++)
  {
    servoWrite(st3,j);
    servoWrite(st5,j);
    servoWrite(st1,i);
    delay(2);
  }
  for (i=5;i<=kneeCenter;i++)
  {
    servoWrite(sk2,i);
    servoWrite(sk4,i);
    servoWrite(sk6,i);
    delay(2);    
  }
  for (i=kneeCenter;i>=5;i--)
  {
    servoWrite(sk1,i);
    servoWrite(sk3,i);
    servoWrite(sk5,i);
    delay(2);
  }
  for (i=thighCenter,j=(90+thighCenter);i<=90;i++,j--)
  {
    servoWrite(st3,j);
    servoWrite(st5,j);
    servoWrite(st1,i);
    delay(2);
  }
  for (i=90,j=90;i<=(90+thighCenter);i++,j--)
  {
    servoWrite(st2,j);
    servoWrite(st6,j);
    servoWrite(st4,i);
    delay(2);
  }
  for (i=5;i<=kneeCenter;i++)
  {
    servoWrite(sk1,i);
    servoWrite(sk3,i);
    servoWrite(sk5,i);
    delay(2);    
  }
  for (i=(90+thighCenter),j=thighCenter;i>=90;i--,j++)
  {
    servoWrite(st2,j);
    servoWrite(st6,j);
    servoWrite(st4,i);
    delay(2);
  }
}

void WalK_Left_Backward()
{
 for(i=kneeCenter;i<=5;i--)
 {
  servoWrite(sk2,i);
  servoWrite(sk4,i);
  servoWrite(sk6,i);
  delay(2); 
 }
 for(i=90,j=90;i<=(90+thighCenter);i++,j--);
 {
  servoWrite(st1,j);
  servoWrite(st5,j);
  servoWrite(st3,i);
  delay(2);
 }
 for(i=5;i<=kneeCenter;i++)
 {
  servoWrite(sk2,i);
  servoWrite(sk4,i);
  servoWrite(sk6,i);
  delay(2); 
 }
 for(i=kneeCenter;i<=5;i--)
 {
  servoWrite(sk1,i);
  servoWrite(sk3,i);
  servoWrite(sk5,i);
  delay(2); 
 }
 for(i=(90+thighCenter),j=thighCenter;i>=90;i--,j++);
 {
  servoWrite(st1,j);
  servoWrite(st5,j);
  servoWrite(st3,i);
  delay(2);
 }
 for(i=90,j=90;i>=thighCenter;i--,j++);
 {
  servoWrite(st2,j);
  servoWrite(st4,j);
  servoWrite(st6,i);
  delay(2);
 }
 for(i=5;i<=kneeCenter;i++)
 {
  servoWrite(sk1,i);
  servoWrite(sk3,i);
  servoWrite(sk5,i);
  delay(2); 
 }
 for(i=thighCenter,j=(90+thighCenter);i<=90;i++,j--);
 {
  servoWrite(st2,j);
  servoWrite(st4,j);
  servoWrite(st6,i);
  delay(2);
 }
}*/
