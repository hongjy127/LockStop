#include <MqttCom.h>
#include "HX711.h"

#define calibration_factor_1 -41000.0
#define calibration_factor_2 -120000.0

#define LOADCELL_DOUT_PIN_1 D3
#define LOADCELL_SCK_PIN_1 D4
#define LOADCELL_DOUT_PIN_2 D5
#define LOADCELL_SCK_PIN_2 D6
#define MAG_PIN D7

// const char *ssid = "KT_GiGA_2G_Wave2_05BE";
// const char *password = "hf52ch1863";
const char *ssid = "TECH2_2G";
const char *password = "tech21234!";
// const char *ssid = "Galaxy Z Flip7055";
// const char *password = "0123456789";
const char *server = "172.30.1.87";
const char *sub_topic = "test/led"; // 아두이노는 토픽 하나만 지정 가능, #, + 지원 안됨

HX711 scale_1;
HX711 scale_2;

MqttCom com(ssid, password);

double weight_old_1;
double weight_old_2;
double weight_old;
double weight_new_1;
double weight_new_2;
double weight_new;
double change;
double change_value = 0.2;
int count_open = 0;
int count_close = 0;
int times = 5;

void check() {
    weight_new_1 = scale_1.get_units(times);
    weight_new_2 = scale_2.get_units(times);
    weight_new = weight_new_1 + weight_new_2;

    char buf[128];
    sprintf(buf, "%f", weight_new);
    com.publish("iot/loadcell", buf);
    com.print_d(0, "loadcell: ", weight_new, true);
    
    int mag = digitalRead(MAG_PIN);
    if (mag == 1) {
        // mosquitto_sub -v -h localhost -t iot/magnetic
        if (count_open == 0) {
            count_close = 0;
            com.print(0, "door open", true);
            com.publish("iot/magnetic", "open");
            count_open++;
        }
        com.print_d(0, "old: ", weight_old, "new: ", weight_new, true);
        change = weight_new - weight_old;
        // com.print_d(0, "change: ", change, true);
        if(change > change_value) {
            com.publish("iot/CJ", "full");
            com.print(0, "publish: full", true);
        } else if (change < -change_value) {
            com.publish("iot/CJ", "empty");
            com.print(0, "publish: empty", true);
        }

        // 라즈베리 파이로 사진찍으라고 보내
    } else {
        if (count_close == 0) {
            count_open = 0;
            com.print(0, "door close", true);
            com.publish("iot/magnetic", "close");
            count_close++;
        }
    }
    
    weight_old = weight_new;
    com.print(0, "---------", true);
    
}

void subscribe(char* topic, uint8_t* payload, unsigned int length) {
    char buf[128];
    memcpy(buf, payload, length);   // 메모리 내용 복사
    buf[length] = '\0';

    Serial.println(topic);
    Serial.println(buf);
}

void setup() {
    pinMode(MAG_PIN,INPUT_PULLUP);
    com.init(server, sub_topic, subscribe);

    scale_1.begin(LOADCELL_DOUT_PIN_1, LOADCELL_SCK_PIN_1, 32);
    scale_2.begin(LOADCELL_DOUT_PIN_2, LOADCELL_SCK_PIN_2, 32);
    scale_1.set_scale(calibration_factor_1);
    scale_2.set_scale(calibration_factor_2);
    scale_1.tare();
    scale_2.tare();
    com.print(0, "zero offset", true);

    if (scale_1.is_ready() && scale_2.is_ready()) {
        weight_old_1 = scale_1.get_units(times);
        weight_old_2= scale_2.get_units(times);
        weight_old = weight_old_1 + weight_old_2;
        // com.print_d(0, "weight_old: ", weight_old, true);
        // com.setInterval(3000, check);
    } else {
        com.print(0, "HX711 not found.", true);
    }
}

void loop() {
    com.run();
    if (scale_1.is_ready() && scale_2.is_ready()) {
        check();
        // delay(2000);
    } else {
        com.print(0, "HX711 not found.", true);
    }
}