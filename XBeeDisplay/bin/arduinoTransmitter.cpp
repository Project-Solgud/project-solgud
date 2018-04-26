/*int length = 0;
long long int id = 0;

void setup(){
  Serial.begin(9600);
}

void loop(){
  unsigned char buf[201];
  if (Serial.available()){

    int incomingByte = Serial.read();

    if(length == 201){
      length = 0;
      // TODO: poll sensors
      // TODO: transmit one large message [start byte + id left padded with zeroes + sensor data + incoming data + end byte]
      Serial.println(); // TODO: get data
      id++;
    }
  }
}*/
