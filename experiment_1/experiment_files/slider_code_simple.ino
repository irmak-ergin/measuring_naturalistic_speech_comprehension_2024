void setup() {
  pinMode(13, OUTPUT);
  analogReadResolution(8); // Can be 8, 10, 12 or 14
  Serial.begin(500000);
}

void loop() {
  static unsigned long start = 0;

  if (start == 0)
    start = micros();
  else
    delayMicroseconds(start - micros());

  uint8_t raw = analogRead(A5);
  analogWrite(13, raw);

  Serial.printf("%d %u\n", raw, millis());

  if ((micros() - start > 4000) && (micros() - start > 4294963295))
  {
    start += 8000;
  }
  else
  {
    start += 4000;
  }
}
