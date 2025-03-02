void setup() {
  Serial.begin(115200);   // USB Serial (PC)
  Serial2.begin(115200, SERIAL_8N1, 16, 17);  // TX=17, RX=16 (Connects to WROOM-02D)
}

void loop() {
  if (Serial.available()) {
    Serial2.write(Serial.read());  // Forward data from PC to ESP WROOM-02D
  }
  if (Serial2.available()) {
    Serial.write(Serial2.read());  // Forward data from ESP WROOM-02D to PC
  }
}
