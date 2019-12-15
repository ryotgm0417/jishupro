#include <Wire.h>
#include <MPU9250.h>
#include <SoftwareSerial.h>

// Bluetooth
SoftwareSerial hc06(7,8);

// Accelerometer
MPU9250 mpu;
#define BUF_SIZE 10

// prototype declaration of functions
//void serialFloatPrint(float f, int mode);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Wire.begin();
  delay(2000);
  mpu.setup();
  pinMode(13, OUTPUT);

  delay(5000);
  mpu.calibrateAccelGyro();
  mpu.printCalibration();

  hc06.begin(9600);
  delay(1000);
  hc06.write(" Finished Setup;");
  delay(1000);
} 

void loop() {
  static uint32_t prev_ms = millis();
  float data[] = {0,0,0,0,0,0};
  char datastring[6][8];
  char message[60]="";

  for(int i=0;i<BUF_SIZE;i++){
    mpu.update();
    data[0] += mpu.getAcc(0) / BUF_SIZE;
    data[1] += mpu.getAcc(1) / BUF_SIZE;
    data[2] += mpu.getAcc(2) / BUF_SIZE;
    data[3] += mpu.getGyro(0) / BUF_SIZE;
    data[4] += mpu.getGyro(1) / BUF_SIZE;
    data[5] += mpu.getGyro(2) / BUF_SIZE;
  }

//  dtostrf(data[0],4,2,datastring[0]);
//  dtostrf(data[1],4,2,datastring[1]);
//  dtostrf(data[2],4,2,datastring[2]);
//  dtostrf(data[3],4,2,datastring[3]);
//  dtostrf(data[4],4,2,datastring[4]);
//  dtostrf(data[5],4,2,datastring[5]);

  for(int j=0;j<6;j++){
    dtostrf(data[j], 7, 2, datastring[j]);
    strcat(message, datastring[j]);
    strcat(message, ",");
  }

  strcat(message, ";");

  delay(1000);
  //Serial.println(message);
  hc06.write(message);


//      Serial.println(message);

//      data[0] = mpu.getAcc(0);
//      data[1] = mpu.getAcc(1);
//      data[2] = mpu.getAcc(2);
//      data[0] = mpu.getGyro(0);
//      data[1] = mpu.getGyro(1);
//      data[2] = mpu.getGyro(2);

//      hc06.write(" ");
//      for(int i=0;i<6;i++){
//        serialFloatPrint(data[i],0);
//      }
//      hc06.write(";");

}


//void serialFloatPrint(float f, int mode) {
//  byte * b = (byte *) &f;
//  if(mode==0){
//    hc06.write(b[0]);
//    hc06.write(b[1]);
//    hc06.write(b[2]);
//    hc06.write(b[3]);
//  }else{
//    Serial.print(b[0], BIN);
//    Serial.print(b[1], BIN);
//    Serial.print(b[2], BIN);
//    Serial.print(b[3], BIN);
//    Serial.println();
//  }
//}
