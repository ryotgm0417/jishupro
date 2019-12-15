#include <Wire.h>
#include <SoftwareSerial.h>

// Bluetooth
SoftwareSerial hc06(7,8);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(13, OUTPUT);

  hc06.begin(9600);
  delay(1000);
  hc06.write(" Finished Setup;");
  delay(1000);
} 

void loop() {

  // Bluetooth: Send message

  hc06.write(" In");
  hc06.write(" loop;");

  delay(100);
}
