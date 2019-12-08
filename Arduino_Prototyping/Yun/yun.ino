//yun

#include <SoftwareSerial.h>
#include <Mouse.h>

SoftwareSerial BTSerial(9, 10); // RX | TX

void setup() {
  Serial.begin(9600);
  BTSerial.begin(9600);
  Mouse.begin();
}

void loop(){
  string incoming = "";

  if(BTSerial.available() > 0){
    incoming = BTSerial.readStringUntil(\n)
  }
}

/*
void loop() {
  char incoming = 0;
  
  if(BTSerial.available() > 0){
    Serial.println("byte found");
    incoming = BTSerial.read();
  }
  switch(incoming){
  case 'l':
    Serial.println("left press");
    Mouse.press(MOUSE_LEFT);
    break;
  case 'L':
    Serial.println("left release");
    Mouse.release(MOUSE_LEFT);
    break;
  case 'r':
    Serial.println("right press");
    Mouse.press(MOUSE_RIGHT);
    break;
  case 'R':
    Serial.println("right release");
    Mouse.release(MOUSE_RIGHT);
    break;
  default:
    break;
  }
} 
*/
