#include<Servo.h>

Servo st1, st2, st3, st4, st5, st6, sk1, sk2, sk3, sk4, sk5, sk6;

void setup() {
  
st1.attach(1);
st2.attach(2);
st3.attach(3);
st4.attach(4);
st5.attach(5);
st6.attach(6);
sk1.attach(7);
sk2.attach(8);
sk3.attach(9);
sk4.attach(10);
sk5.attach(11);
sk6.attach(12);

}

void loop() {
  st1.write(90);
  st2.write(90);
  st3.write(90);
  st4.write(90);
  st5.write(90);
  st6.write(90);
  sk1.write(90);
  sk2.write(90);
  sk3.write(90);
  sk4.write(90);
  sk5.write(90);
  sk6.write(90);
}
