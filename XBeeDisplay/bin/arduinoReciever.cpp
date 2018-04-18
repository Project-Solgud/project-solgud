void setup(){
  Serial.begin(9600);
}

void loop(){
  unsigned char buf[201]; // TODO actual packet size
  // TODO read transmission to buffer
  Serial.println(buffer); // TODO Arduino is finnicky with strings, so we'd have to mess with this
}
