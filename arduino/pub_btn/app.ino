#include <MqttCom.h>
#include <Button.h>
#include <Led.h>

const char *ssid = "KT_GiGA_2G_Wave2_05BE";
const char *password = "hf52ch1863";
const char *server = "172.30.1.39";
const char *sub_topic = "test/led"; // 아두이노는 토픽 하나만 지정 가능, #, + 지원 안됨

Button btn(D5);
Led led(D6);
MqttCom com(ssid, password);
bool state = false;

void check() {
    if(!state) {
        // com.print(0, "Blink mode", true);
        led.toggle();
        com.publish("test/led", "Blink mode");
        state = true;
    } else {
        led.off();
        state = false;
        // com.print(0, "Off mode", true);
        com.publish("test/led", "Off mode");
    }
}

// 외부에서 장치 제어
void subscribe(char* topic, uint8_t* payload, unsigned int length) {
    char buf[128];
    memcpy(buf, payload, length);   // 메모리 내용 복사
    buf[length] = '\0';

    Serial.println(topic);
    Serial.println(buf);
}

void setup() {
    // com.init(server);
    com.init(server, sub_topic, subscribe);
    btn.setCallback(check);
}

void loop() {
    btn.check();
    com.run();
}