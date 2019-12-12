#include <MPU9250.h>
#include <Wire.h>
#include <SoftwareSerial.h>

#define touchPin 3

MPU9250 mpu;
int s=0;

// Bluetooth
SoftwareSerial hc06(11,12);
String msg="";

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Wire.begin();
  delay(2000);
  mpu.setup();
  pinMode(13, OUTPUT);
  pinMode(touchPin, INPUT);

  hc06.begin(9600);
  delay(2000);
  hc06.write("AT");
  delay(2000);
  hc06.write("AT+NAMEHC06RT");
  delay(2000);
  hc06.write("AT+PIN2019");
  delay(2000);
  hc06.write("AT+BAUD4");
}

void loop() {
  // put your main code here, to run repeatedly:

  // Accelerometer + Gyro
//  static uint32_t prev_ms = millis();
//  if ((millis() - prev_ms) > 1000)
//  {
//      mpu.update();
//      mpu.print();
//
//      Serial.print("roll  (x-forward (north)) : ");
//      Serial.println(mpu.getRoll());
//      Serial.print("pitch (y-right (east))    : ");
//      Serial.println(mpu.getPitch());
//      Serial.print("yaw   (z-down (down))     : ");
//      Serial.println(mpu.getYaw());
//
//      prev_ms = millis();
//  }


  // Switch
//  if(digitalRead(2)==LOW) {
//    s=s+1;
//    if(s>2)
//     s=0;
//    delay(20);
//    while(digitalRead(2)==LOW) {}
//  }
//  if (s==0) {
//    digitalWrite(13, LOW);
//  }
//  if (s==1) {
//    digitalWrite(13, HIGH);
//  }
//  if (s==2) {
//    digitalWrite(13, HIGH);
//    delay(100);
//    digitalWrite(13, LOW);
//    delay(100);
//  }

  // Touch Sensor
//  int touchValue = digitalRead(touchPin);
//  if (touchValue == HIGH) {
//    Serial.println("touched");
//  }
  
  // Bluetooth
  while(hc06.available()>0){
    msg += char(hc06.read());
  }
  if(msg!=""){
   Serial.print("Command recieved : ");
   Serial.println(msg);
   msg=""; //reset
  }

  if (Serial.available()){
    delay(100);
    hc06.write(Serial.read());
  }

  delay(100);
}
