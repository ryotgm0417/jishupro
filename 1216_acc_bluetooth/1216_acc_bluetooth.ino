#include <Wire.h>
#include <MPU9250.h>
#include <SoftwareSerial.h>

// Bluetooth
SoftwareSerial hc06(7,8);

// Accelerometer
MPU9250 mpu;
#define BUF_SIZE 20

// Switch
int flag = 0;

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
  char message[60]=" ";

  for(int i=0;i<BUF_SIZE;i++){
    mpu.update();
    data[0] += mpu.getAcc(0)*100 / BUF_SIZE;  // 100 = 1g (gravity)
    data[1] += mpu.getAcc(1)*100 / BUF_SIZE;
    data[2] += mpu.getAcc(2)*100 / BUF_SIZE;
    data[3] += mpu.getGyro(0) / BUF_SIZE;
    data[4] += mpu.getGyro(1) / BUF_SIZE;
    data[5] += mpu.getGyro(2) / BUF_SIZE;
  }

  for(int j=0;j<6;j++){
    dtostrf(data[j], 7, 2, datastring[j]);
    strcat(message, datastring[j]);
    strcat(message, ",");
  }

  strcat(message, ";");

  delay(20);
  //Serial.println(message);
  hc06.write(message);


 // Switch
  if(digitalRead(2)==LOW && flag==0) {
    hc06.write(" P;");  // Pressed
    flag = 1;
  }else if(digitalRead(2)==HIGH && flag==1){
    hc06.write(" R;"); // Released
    flag = 0;
  }

}
