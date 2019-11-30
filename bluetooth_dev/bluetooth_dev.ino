#include <Mouse.h>

void setup() {
  Serial.begin(9600);
  Mouse.begin();
}

void loop() {
  int i = 0;
  if(Serial.available() > 0){
    i = Serial.read();
    Serial.println("fds");
  }
  //Serial.print(i);
  if(i == 49){Mouse.click();Serial.println("click");}
  delay(500);
}
