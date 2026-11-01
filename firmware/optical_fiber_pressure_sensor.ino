// Acquisition template only.
// Verify the photodetector circuit, ADC pin, reference voltage, and sampling
// rate before connecting this code to real hardware.

const int SENSOR_PIN = A0;
const unsigned long SAMPLE_PERIOD_MS = 100;

void setup() {
  Serial.begin(115200);
  Serial.println("timestamp_ms,raw_adc");
}

void loop() {
  static unsigned long next_sample_ms = 0;
  const unsigned long now_ms = millis();
  if (now_ms < next_sample_ms) {
    return;
  }
  next_sample_ms = now_ms + SAMPLE_PERIOD_MS;

  const int raw_adc = analogRead(SENSOR_PIN);
  Serial.print(now_ms);
  Serial.print(',');
  Serial.println(raw_adc);
}

