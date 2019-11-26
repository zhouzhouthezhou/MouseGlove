/****************************************************************
 * Example2_Advanced.ino
 * ICM 20948 Arduino Library Demo 
 * Shows how to use granular configuration of the ICM 20948
 * Owen Lyke @ SparkFun Electronics
 * Original Creation Date: April 17 2019
 * 
 * This code is beerware; if you see me (or any other SparkFun employee) at the
 * local, and you've found our code helpful, please buy us a round!
 * 
 * Distributed as-is; no warranty is given.
 ***************************************************************/
#include "ICM_20948.h"  // Click here to get the library: http://librarymanager/All#SparkFun_ICM_20948_IMU
#include <math.h>

//#define USE_SPI       // Uncomment this to use SPI

#define SERIAL_PORT Serial

#define WIRE_PORT Wire  // Your desired Wire port.      
#define AD0_VAL   1     // The value of the last bit of the I2C address. 
                        // On the SparkFun 9DoF IMU breakout the default is 1, and when 
                        // the ADR jumper is closed the value becomes 0
#ifdef USE_SPI
  ICM_20948_SPI myICM;  // If using SPI create an ICM_20948_SPI object
#else
  ICM_20948_I2C myICM;  // Otherwise create an ICM_20948_I2C object
#endif

void setup() {

  SERIAL_PORT.begin(115200);
  while(!SERIAL_PORT){};

#ifdef USE_SPI
    SPI_PORT.begin();
#else
    WIRE_PORT.begin();
    WIRE_PORT.setClock(400000);  // 400 kHz clock
#endif
  
  bool initialized = false;
  while( !initialized ){

#ifdef USE_SPI
    myICM.begin( CS_PIN, SPI_PORT, SPI_FREQ ); // Here we are using the user-defined SPI_FREQ as the clock speed of the SPI bus 
#else
    myICM.begin( WIRE_PORT, AD0_VAL );
#endif

    SERIAL_PORT.print( F("Initialization of the sensor returned: ") );
    SERIAL_PORT.println( myICM.statusString() );
    if( myICM.status != ICM_20948_Stat_Ok ){
      SERIAL_PORT.println( "Trying again..." );
      delay(500);
    }else{
      initialized = true;
    }
  }

  // In this advanced example we'll cover how to do a more fine-grained setup of your sensor
  SERIAL_PORT.println("Device connected!");

  // Here we are doing a SW reset to make sure the device starts in a known state
  myICM.swReset( );
  if( myICM.status != ICM_20948_Stat_Ok){
    SERIAL_PORT.print(F("Software Reset returned: "));
    SERIAL_PORT.println(myICM.statusString());
  }
  delay(250);
  
  // Now wake the sensor up
  myICM.sleep( false );
  myICM.lowPower( false );

  // The next few configuration functions accept a bit-mask of sensors for which the settings should be applied.

  // Set Gyro and Accelerometer to a particular sample mode
  // options: ICM_20948_Sample_Mode_Continuous
  //          ICM_20948_Sample_Mode_Cycled
  myICM.setSampleMode( (ICM_20948_Internal_Acc | ICM_20948_Internal_Gyr), ICM_20948_Sample_Mode_Continuous ); 
  if( myICM.status != ICM_20948_Stat_Ok){
    SERIAL_PORT.print(F("setSampleMode returned: "));
    SERIAL_PORT.println(myICM.statusString());
  }

  // Set full scale ranges for both acc and gyr
  ICM_20948_fss_t myFSS;  // This uses a "Full Scale Settings" structure that can contain values for all configurable sensors
  
  myFSS.a = gpm2;         // (ICM_20948_ACCEL_CONFIG_FS_SEL_e)
                          // gpm2
                          // gpm4
                          // gpm8
                          // gpm16
                          
  myFSS.g = dps250;       // (ICM_20948_GYRO_CONFIG_1_FS_SEL_e)
                          // dps250
                          // dps500
                          // dps1000
                          // dps2000
                          
  myICM.setFullScale( (ICM_20948_Internal_Acc | ICM_20948_Internal_Gyr), myFSS );  
  if( myICM.status != ICM_20948_Stat_Ok){
    SERIAL_PORT.print(F("setFullScale returned: "));
    SERIAL_PORT.println(myICM.statusString());
  }


  // Set up Digital Low-Pass Filter configuration
  ICM_20948_dlpcfg_t myDLPcfg;            // Similar to FSS, this uses a configuration structure for the desired sensors
  myDLPcfg.a = acc_d473bw_n499bw;         // (ICM_20948_ACCEL_CONFIG_DLPCFG_e)
                                          // acc_d246bw_n265bw      - means 3db bandwidth is 246 hz and nyquist bandwidth is 265 hz
                                          // acc_d111bw4_n136bw
                                          // acc_d50bw4_n68bw8
                                          // acc_d23bw9_n34bw4
                                          // acc_d11bw5_n17bw
                                          // acc_d5bw7_n8bw3        - means 3 db bandwidth is 5.7 hz and nyquist bandwidth is 8.3 hz
                                          // acc_d473bw_n499bw

  myDLPcfg.g = gyr_d361bw4_n376bw5;       // (ICM_20948_GYRO_CONFIG_1_DLPCFG_e)
                                          // gyr_d196bw6_n229bw8
                                          // gyr_d151bw8_n187bw6
                                          // gyr_d119bw5_n154bw3
                                          // gyr_d51bw2_n73bw3
                                          // gyr_d23bw9_n35bw9
                                          // gyr_d11bw6_n17bw8
                                          // gyr_d5bw7_n8bw9
                                          // gyr_d361bw4_n376bw5
                                          
  myICM.setDLPFcfg( (ICM_20948_Internal_Acc | ICM_20948_Internal_Gyr), myDLPcfg );
  if( myICM.status != ICM_20948_Stat_Ok){
    SERIAL_PORT.print(F("setDLPcfg returned: "));
    SERIAL_PORT.println(myICM.statusString());
  }

  // Choose whether or not to use DLPF
  // Here we're also showing another way to access the status values, and that it is OK to supply individual sensor masks to these functions
  ICM_20948_Status_e accDLPEnableStat = myICM.enableDLPF( ICM_20948_Internal_Acc, false );
  ICM_20948_Status_e gyrDLPEnableStat = myICM.enableDLPF( ICM_20948_Internal_Gyr, false );
  SERIAL_PORT.print(F("Enable DLPF for Accelerometer returned: ")); SERIAL_PORT.println(myICM.statusString(accDLPEnableStat));
  SERIAL_PORT.print(F("Enable DLPF for Gyroscope returned: ")); SERIAL_PORT.println(myICM.statusString(gyrDLPEnableStat));

  SERIAL_PORT.println();
  SERIAL_PORT.println(F("Configuration complete!")); 
}

void loop() {
  if( myICM.dataReady() ){
    myICM.getAGMT();                // The values are only updated when you call 'getAGMT'
    float previous_RxEst = (myICM.accX()) * 1000;
    float previous_RyEst = (myICM.accY()) * 1000;
    float previous_RzEst = (myICM.accZ()) * 1000;
    float RzGyro = 0;
    while (1) {
      myICM.getAGMT();
      float RxAcc = (myICM.accX()) * 1000;
      float RyAcc = (myICM.accY()) * 1000;
      float RzAcc = (myICM.accZ()) * 1000;
      float RateAxz = myICM.gyrX();
      float RateAyz = myICM.gyrY();
      float previous_Axz = atan2(previous_RxEst, previous_RzEst);
      float previous_Ayz = atan2(previous_RyEst, previous_RzEst);
      float wGyro = 10;
      float Axz = previous_Axz + (RateAxz * 2.5 * pow(10,-6));
      float Ayz = previous_Ayz + (RateAyz * 2.5 * pow(10,-6));
      float RxGyro = sin(Axz) /  sqrt(1 + pow(cos(Axz),2) * pow(tan(Ayz),2));
      float RyGyro = sin(Ayz) / sqrt(1 + pow(cos(Ayz),2) * pow(tan(Axz),2));
      if (previous_RzEst < 0){
        RzGyro = - sqrt(1 - pow(RxGyro,2) - pow(RyGyro,2));
      }else{
        RzGyro = sqrt(1 - pow(RxGyro,2) - pow(RyGyro,2));
      }
      float RxEst = (RxAcc + RxGyro * wGyro ) / (1 + wGyro);
      float RyEst = (RyAcc + RyGyro * wGyro ) / (1 + wGyro);
      float RzEst = (RzAcc + RzGyro * wGyro ) / (1 + wGyro);
      printScaledAGMT( RxEst, RyEst, RzEst);
      previous_RxEst = (RxAcc + RxGyro * wGyro ) / (1 + wGyro);
      previous_RyEst = (RyAcc + RyGyro * wGyro ) / (1 + wGyro);
      previous_RzEst = (RzAcc + RzGyro * wGyro ) / (1 + wGyro);
      delay(2000);
    }
  }else{
      Serial.println("Waiting for data");
      delay(500);
    }
}

void printFormattedFloat(float val, uint8_t leading, uint8_t decimals){
  float aval = abs(val);
  if(val < 0){
    SERIAL_PORT.print("-");
  }else{
    SERIAL_PORT.print(" ");
  }
  for( uint8_t indi = 0; indi < leading; indi++ ){
    uint32_t tenpow = 0;
    if( indi < (leading-1) ){
      tenpow = 1;
    }
    for(uint8_t c = 0; c < (leading-1-indi); c++){
      tenpow *= 10;
    }
    if( aval < tenpow){
      SERIAL_PORT.print("0");
    }else{
      break;
    }
  }
  if(val < 0){
    SERIAL_PORT.print(-val, decimals);
  }else{
    SERIAL_PORT.print(val, decimals);
  }
}

void printScaledAGMT( float RxEst, float RyEst, float RzEst){
  SERIAL_PORT.print("Scaled. X [ ");
  printFormattedFloat( RxEst, 5, 2 );
  SERIAL_PORT.print(" ], Y [ ");
  printFormattedFloat( RyEst, 5, 2 );
  SERIAL_PORT.print(" ], Z [ ");
  printFormattedFloat( RzEst, 5, 2 );
  SERIAL_PORT.print(" ] ");
  SERIAL_PORT.println();
}

