// Jai Shree Ram
byte cmd;
int size;
void setup()
{
  pinMode(LED_BUILTIN,OUTPUT);
  Serial.begin(9600);
}

void loop()
{
 size  = Serial.available();
  if(size)
  {
    cmd = Serial.read();
    if(cmd == 'F')
    {
      digitalWrite(LED_BUILTIN,HIGH);
    } else if (cmd == 'B')
    {
      digitalWrite(LED_BUILTIN,LOW);
    }
   }
}
