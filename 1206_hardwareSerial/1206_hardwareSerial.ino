#include <Wire.h>

// Bluetooth
String msg="";

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(13, OUTPUT);
  delay(2000);

  delay(1000);
  Serial.write("AT");
  delay(1000);
  Serial.write("AT+NAMEHC06RT");
  delay(1000);
  Serial.write("AT+PIN1234");
  delay(1000);
  Serial.write("AT+BAUD4");
  Serial.println();
}

void loop() {
  // put your main code here, to run repeatedly:
  
  // Bluetooth
  while(Serial.available()>0){
    msg += char(Serial.read());
  }
  if(msg!=""){
   Serial.print("Command recieved : ");
   Serial.println(msg);
   msg=""; //reset
  }

  while (Serial.available()){
    delay(50);
    Serial.write(Serial.read());
  }

  delay(100);
}
