#include "HX711.h"

const int calibration_factor = -410000;

// HX711 circuit wiring
const int LOADCELL_DOUT_PIN = D2;
const int LOADCELL_SCK_PIN = D1;

HX711 scale;

double value;

void setup() {
  Serial.begin(9600);
  Serial.println("HX711 kg demo");
  scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
  scale.set_scale(calibration_factor);
  scale.tare();
  Serial.println("Readings:");
}

void loop() {

  if (scale.is_ready()) {
    // long reading = scale.read();
    Serial.print("Reading: ");

    value = scale.get_units();
    Serial.print(value, 5);
    Serial.println("kg");
  } else {
    Serial.println("HX711 not found.");
  }

  delay(1000);
  
}