#include <MPU9250.h>
#include <Wire.h>

MPU9250 mpu;

int s=0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  Wire.begin();
  delay(2000);
  mpu.setup();
  pinMode(13, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:

  // Accelerometer + Gyro
  static uint32_t prev_ms = millis();
  if ((millis() - prev_ms) > 1000)
  {
      mpu.update();
      mpu.print();

      Serial.print("roll  (x-forward (north)) : ");
      Serial.println(mpu.getRoll());
      Serial.print("pitch (y-right (east))    : ");
      Serial.println(mpu.getPitch());
      Serial.print("yaw   (z-down (down))     : ");
      Serial.println(mpu.getYaw());

      prev_ms = millis();
  }


  // Switch
  if(digitalRead(2)==LOW) {
    s=s+1;
    if(s>2)
     s=0;
    delay(20);
    while(digitalRead(2)==LOW) {}
  }
  if (s==0) {
    digitalWrite(13, LOW);
  }
  if (s==1) {
    digitalWrite(13, HIGH);
  }
  if (s==2) {
    digitalWrite(13, HIGH);
    delay(100);
    digitalWrite(13, LOW);
    delay(100);
  }

  // Touch Sensor
  
  
  
}
