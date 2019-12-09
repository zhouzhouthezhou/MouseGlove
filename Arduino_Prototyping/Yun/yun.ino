//yun

#include <SoftwareSerial.h>
#include <Mouse.h>
#include <pt.h>

SoftwareSerial BTSerial(9, 10); // RX | TX

const char delim = ',';
static struct pt accelThread, mouseThread;
const int resolution = 100;
const int scalingFactor = 5;
const int scale = resolution * scalingFactor;
const int mouseSpeed = 20;

bool isLeft = false;
bool isRight = false;

void setup() {
  Serial.begin(9600);
  BTSerial.begin(9600);

  PT_INIT(&accelThread);
  PT_INIT(&mouseThread);
  
  Mouse.begin();
}
/*
static int protothreadAccel(struct pt *pt, double x, double y, double z)
{
  PT_BEGIN(pt);
  for(int i = 0; i < 5; i++){
    Serial.println("yee");
  }
  PT_END(pt);
}

static int protothreadMouse(struct pt *pt, int i, int m)
{
  PT_BEGIN(pt);
  for(int i = 0; i < 5; i++){
    Serial.println("what");
  }
  PT_END(pt);
}
*/

int mapX(int x){
  //double zero = 0.0;
  //x = abs(x) - zero;
  double perc = 1;
  if(x < 8){
    perc = x/35.0;
  }else if (x > 8){
    perc = x/35.0;
  }
  return -1 * (perc * mouseSpeed);
}

int mapY(int y){
  //double zero = 0.0;
  //y = abs(y) - zero;
  double perc = 1;
  if(y < 8){
    perc = y/35.0;
  }else if (y > 8){
    perc = y/35.0;
  }
  return perc * mouseSpeed;
}


void loop(){
  String incoming = "";
  if(BTSerial.available() > 0){
    incoming = BTSerial.readStringUntil('\n');
    int xcomma = incoming.indexOf(',');
    int ycomma = incoming.indexOf(',', xcomma+1);
    int zcomma = incoming.indexOf(',', ycomma+1);
    int icomma = incoming.indexOf(',', zcomma+1);
    int mcomma = incoming.indexOf(',', icomma+1);

    String xs = incoming.substring(0, xcomma);
    String ys = incoming.substring(xcomma+1, ycomma);
    String zs = incoming.substring(ycomma+1, zcomma);
    String is = incoming.substring(zcomma+1, icomma);
    String ms = incoming.substring(icomma+1, mcomma);

    int x = mapX(xs.toDouble() * scale);
    int y = mapY(ys.toDouble() * scale);

    int i = is.toInt();
    int m = ms.toInt();

    //protothreadAccel(&accelThread, x, y, z);
    //protothreadMouse(&mouseThread, i, m);
    
    //delay(1000);
    Mouse.move(y, -x, 0);

    if(i == 0 && isLeft){
      Mouse.release(MOUSE_LEFT);
      isLeft = false;
    }else if(i == 1 && !isLeft){
      Mouse.press(MOUSE_LEFT);
      isLeft = true;
    }else if(m == 0 && isRight){
      Mouse.release(MOUSE_RIGHT);
      isRight = false;
    }else if(m == 1 && !isRight){
      Mouse.press(MOUSE_RIGHT);
      isRight = true;
    }
    
    
    String xss(x);
    String yss(y);
    String xraw(xs.toDouble() * scale);
    String yraw(ys.toDouble() * scale);
    Serial.println(xss + ", " + yss + "," + xraw + ", " + yraw);
    

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
