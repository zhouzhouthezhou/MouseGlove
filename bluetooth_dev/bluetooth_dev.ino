#include <Mouse.h>

void setup(){
  Serial.begin(9600);

  pinMode(9, INPUT);
  //pinMode(10, INPUT);
  Mouse.begin();
}

void loop() {
  double index = 5*(analogRead(A1)/1023);
  if(index > 4){
    Mouse.press(MOUSE_LEFT);
    while(index > 4){index = 5*(analogRead(A1)/1023);delay(10);}
    Mouse.release(MOUSE_LEFT);
  }

  double middle = 5*(analogRead(A2)/1023);
  if(middle > 4){
    Mouse.press(MOUSE_RIGHT);
    while(middle > 4){middle = 5*(analogRead(A2)/1023);}
    Mouse.release(MOUSE_RIGHT);
  }
}
