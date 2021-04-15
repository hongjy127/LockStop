#include <MqttCom.h>

const char *ssid = "KT_GiGA_2G_Wave2_05BE";
const char *password = "hf52ch1863";
const char *server = "172.30.1.39";
const char *sub_topic = "test/led"; // 아두이노는 토픽 하나만 지정 가능, #, + 지원 안됨

MqttCom com(ssid, password);

const int var_pin = A0;
int analog_val;
int res_old;
int res_new;
int change;

void check() {
    res_new = analogRead(var_pin);
    com.print_i(0, "old: ", res_old, "new: ", res_new, true);
    change = res_new-res_old;
    com.print_i(0, "change: ", change);
    if(change > 10) {
        com.publish("test/resister", "Increase");
        com.print(0, "publish: Increase", true);
    } else if (change < -10) {
        com.publish("test/resister", "Decrease");
        com.print(0, "publish: Decrease", true);
    }

    res_old = res_new;
    com.print(0, "---------", true);
    // com.print_i(0, "D_value: ", digital_val, true);
    // com.print_d(1, "Voltage: ", res, true);
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
    res_old = analogRead(var_pin);
    com.setInterval(1000, check);
}

void loop() {
    com.run();
}