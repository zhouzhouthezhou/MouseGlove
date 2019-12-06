//nano

#include <SoftwareSerial.h>

SoftwareSerial BTSerial(2,3); // RX | TX

void setup() {
  BTSerial.begin(9600);
}

void loop() {
  double index = 5*(analogRead(A1)/1023);
  if(index > 4){
    BTSerial.print('l');
    while(index > 4){index = 5*(analogRead(A1)/1023);delay(10);}
    BTSerial.print('L');
  }

  double middle = 5*(analogRead(A2)/1023);
  if(middle > 4){
    BTSerial.print('r');
    while(middle > 4){middle = 5*(analogRead(A2)/1023);}
    BTSerial.print('R');
  }
}
