const int MAG_PIN = D5;

void setup() {
    Serial.begin(9600);
    pinMode(MAG_PIN,INPUT_PULLUP);
}

void loop() {
    int a = digitalRead(MAG_PIN);
    // Serial.println(a);
    if(a == 0) {
        Serial.println("close");
    } else {
        Serial.println("open");
    }
    delay(1000);
}