#include <Wire.h>
#include <SoftwareSerial.h>

// Bluetooth
SoftwareSerial hc06(7,8);
String msg="";

int mode=0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(13, OUTPUT);

  hc06.begin(9600);
  delay(1000);
  hc06.write("AT");
  delay(1000);
  hc06.write("AT+NAMEHC06RT");
  delay(1000);
  hc06.write("AT+PIN1234");
  delay(1000);
  hc06.write("AT+BAUD4");
} 

void loop() {

  // Bluetooth
  
  while(hc06.available()>0){
    msg += char(hc06.read());
  }
  if(msg!=""){
   Serial.print("Command recieved : ");
   Serial.println(msg);

   if(msg=="1") mode = 1;
   else if(msg=="0") mode = 0;
   
   msg=""; //reset
  }

  while (Serial.available()){
    delay(50);
    hc06.write(Serial.read());
  }

  //Turn on or off LED
  switch(mode){
    case 0:
      digitalWrite(13,LOW);
      break;
    case 1:
      digitalWrite(13,HIGH);
      break;
  }

  delay(100);
}
