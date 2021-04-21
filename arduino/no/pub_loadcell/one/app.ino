#include <MqttCom.h>
#include "HX711.h"

#define LOADCELL_DOUT_PIN D3
#define LOADCELL_SCK_PIN D4
#define calibration_factor -410000

// mosquitto_sub -v -h localhost -t iot/#
// const char *ssid = "KT_GiGA_2G_Wave2_05BE";
// const char *password = "hf52ch1863";
const char *ssid = "TECH2_2G";
const char *password = "tech21234!";
const char *server = "172.30.1.87";
const char *sub_topic = "test/led"; // 아두이노는 토픽 하나만 지정 가능, #, + 지원 안됨
// const char *ssid = "Galaxy Z Flip7055";
// const char *password = "0123456789";
// const char *server = "192.168.138.162";

HX711 scale;

MqttCom com(ssid, password);

double res_old;
double res_new;
double change;
double change_value = 0.01;

void check() {
    res_new = scale.get_units();
    com.print_d(0, "old: ", res_old, "new: ", res_new, true);
    
    change = res_new-res_old;
    com.print_d(0, "change: ", change, true);
    if(change > change_value) {
        com.publish("iot/CJ", "full");
        com.print(0, "publish: full", true);
    } else if (change < -change_value) {
        com.publish("iot/CJ", "empty");
        com.print(0, "publish: empty", true);
    }
    char buf[128];
    sprintf(buf, "%f", res_new);
    com.publish("iot/loadcell", buf);
    com.print_d(0, "loadcell: ", res_new, true);

    res_old = res_new;
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
    com.init(server, sub_topic, subscribe);
    // Serial.begin(115200);
    scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
    scale.set_scale(calibration_factor);
    scale.tare();
    com.print(0, "zero offset", true);

    if (scale.is_ready()) {
        res_old = scale.get_units();
    } else {
        com.print(0, "HX711 not found.", true);
    }
    
}

void loop() {
    com.run();
    if (scale.is_ready()) {
        check();
        delay(1000);

    } else {
        com.print(0, "HX711 not found.", true);
        // Serial.println("HX711 not found.");
    }
    
}
