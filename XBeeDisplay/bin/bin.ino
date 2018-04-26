#include <Wire.h>
#include <Adafruit_MMA8451.h>
#include <Adafruit_Sensor.h>
#include "Adafruit_SI1145.h"
#include <SPI.h>
#include <Adafruit_BMP280.h>
#include <RH_RF95.h>

#define BMP_SCK 13
#define BMP_MISO 12
#define BMP_MOSI 11
#define BMP_CS 10

Adafruit_SI1145 uv = Adafruit_SI1145();
Adafruit_BMP280 bmp; // I2C
Adafruit_MMA8451 mma = Adafruit_MMA8451();
RH_RF95 rf95;

uint8_t buf[151];

int length;
int id = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600); //May need to decrease baud

  while (!Serial) ; // Wait for serial port to be available
  if (!rf95.init())
    Serial.println("init failed");
  
  Serial.println(F("All Sensor test"));

  if (! uv.begin()) {
    Serial.println("Didn't find Si1145");
    while (1);
  }

 if (!bmp.begin()) {
    Serial.println(F("Could not find a valid BMP280 sensor, check wiring!"));
    while (1);
  }

  if (! mma.begin()) {
    Serial.println("Couldnt start");
    while (1);
  }
  Serial.println("MMA8451 found!");

  mma.setRange(MMA8451_RANGE_8_G);

  Serial.print("Range = "); Serial.print(2 << mma.getRange());
  Serial.println("G");
}

void loop() {


  if(Serial.available()){
    int incomingByte = Serial.read();
    if(incomingByte == 0 || incomingByte == 0xfd || incomingByte == 0xfe || incomingByte == 0xf0){
      incomingByte = 1;
    }
    buf[length] = incomingByte;
    length++;

    if(length == 151){

      String message = "";

      message += (char) 0xfd;

      message += (String(id));
      message += (char) 0xf0;

      id++;

      length = 0;

      message += bmp.readTemperature();
      message += (char) 0xf0;
      message += bmp.readPressure();
      message += (char) 0xf0;
      message += bmp.readAltitude(1013.25);
      message += (char) 0xf0;

      message += uv.readVisible();
      message += (char) 0xf0;
      message += uv.readIR();
      message += (char) 0xf0;
      message += uv.readUV();
      message += (char) 0xf0;

      mma.read();

      message += mma.x;
      message += (char) 0xf0;
      message += mma.y;
      message += (char) 0xf0;
      message += mma.z;
      message += (char) 0xf0;

      sensors_event_t event;
      mma.getEvent(&event);

      message += event.acceleration.x;
      message += (char) 0xf0;
      message += event.acceleration.y;
      message += (char) 0xf0;
      message += event.acceleration.z;
      message += (char) 0xf0;

      message += mma.getOrientation();
      message += (char) 0xf0;

      message += analogRead(0);
      message += (char) 0xf0;

      message += (char*) buf;
      
      message += (char) 0xfe;

      uint8_t mBuffer[message.length()+1];

      message.toCharArray(mBuffer, message.length()+1);

      rf95.send(mBuffer, sizeof(mBuffer));

      rf95.waitPacketSent();
      Serial.println(message);

    }
  }

}
