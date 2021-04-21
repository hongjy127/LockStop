#include <MqttCom.h>

// const char *ssid = "KT_GiGA_2G_Wave2_05BE";
// const char *password = "hf52ch1863";
const char *ssid = "TECH2_2G";
const char *password = "tech21234!";
const char *server = "172.30.1.114";
const char *sub_topic = "test/led"; // 아두이노는 토픽 하나만 지정 가능, #, + 지원 안됨

MqttCom com(ssid, password);

const int var_pin = A0;
int analog_val;
int res_old;
int res_new;
int change;
int change_value = 10;

void check() {
    res_new = analogRead(var_pin);
    com.print_i(0, "old: ", res_old, "new: ", res_new, true);
    change = res_new-res_old;
    com.print_i(0, "change: ", change);
    if(change > change_value) {
        com.publish("iot/CJ", "full");
        com.print(0, "publish: full", true);
    } else if (change < -change_value) {
        com.publish("iot/CJ", "empty");
        com.print(0, "publish: empty", true);
    }
    char buf[128];
    sprintf(buf, "%d", res_new);
    com.publish("iot/loadcell", buf);
    com.print_i(0, "loadcell: ", res_new);

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
    res_old = analogRead(var_pin);
    com.setInterval(1000, check);
}

void loop() {
    com.run();
}