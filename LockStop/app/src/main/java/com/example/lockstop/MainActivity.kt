package com.example.lockstop

import android.os.Bundle
import android.util.Log
import android.webkit.WebViewClient
import androidx.appcompat.app.AppCompatActivity
import com.example.mylib.Notification
import com.example.mylib.net.Mqtt
import kotlinx.android.synthetic.main.activity_main.*
import org.eclipse.paho.client.mqttv3.MqttMessage
import org.jetbrains.anko.startActivity

const val SUB_TOPIC = "iot/#"
// 주소
//const val SERVER_URI = "tcp://192.168.138.162:1883"  // 정연PC
const val SERVER_URI = "tcp://172.30.1.87:1883"  // 정연PC
// const val SERVER_URI = "tcp://192.168.0.4:1883"  // 해준PC
// const val SERVER_URI = "tcp://192.168.0.36:1883"  // 태석PC
// const val SERVER_URI = "tcp://172.30.1.43:1883"  // 현수PC

class MainActivity : AppCompatActivity() {

    lateinit var mqttClient: Mqtt

    companion object {
        const val CHANNEL_ID1 = "com.example.lockstop1"
        const val CHANNEL_ID2 = "com.example.lockstop2"
        const val CHANNEL_NAME = "My Channel"
        const val CHANNEL_DESCRIPTION = "Channel Test"
        const val NOTIFICATION_REQUEST = 0
        const val NOTIFICATION_ID1 = 100
        const val NOTIFICATION_ID2 = 200
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        mqttClient = Mqtt(this, SERVER_URI)
        try {
            mqttClient.setCallback(::onReceived)
            Log.d("Mqtt", "connect")
            mqttClient.connect(arrayOf<String>(SUB_TOPIC))
        } catch (e: Exception) {
            e.printStackTrace()
        }

        btnImgDoor.setOnClickListener {
            startActivity<DoorLockActivity>(
            )
        }

        btnCJ.setOnClickListener {
            startActivity<CJActivity>(
            )
        }

        btnImgSt.setOnClickListener {
            startActivity<StreamingActivity>(
            )
        }

        btnLog.setOnClickListener {
            startActivity<LogActivity>(
            )
        }

    }

    fun onReceived(topic: String, message: MqttMessage) {
        var msg = String(message.payload)

//        Log.i("mqtt_main", "$topic: $msg")

        when (topic) {
            "iot/doorlock" -> {
                val noti = Notification(this)
                noti.createNotificationChannel(CHANNEL_ID1, CHANNEL_NAME, CHANNEL_DESCRIPTION)
                val pendingIntent = noti.getPendingIntent(
                        DoorLockActivity::class.java,
                        NOTIFICATION_REQUEST,
                        msg)

                when (msg) {
                    "open" -> noti.notifyBasic(CHANNEL_ID1, NOTIFICATION_ID1,
                            "Alarm", "문열림",
                            R.drawable.ic_launcher_foreground, pendingIntent)
                    "error3" -> noti.notifyBasic(CHANNEL_ID1, NOTIFICATION_ID1,
                            "Alarm", "비밀번호 3회 오류",
                            R.drawable.ic_launcher_foreground, pendingIntent)
                    
                }
            }
            "iot/CJ" -> {
                val noti = Notification(this)
                noti.createNotificationChannel(CHANNEL_ID2, CHANNEL_NAME, CHANNEL_DESCRIPTION)
                val pendingIntent = noti.getPendingIntent(
                        CJActivity::class.java,
                        NOTIFICATION_REQUEST,
                        msg)
                when (msg) {
                    "full" -> noti.notifyBasic(CHANNEL_ID2, NOTIFICATION_ID2,
                            "Alarm", "택배 도착",
                            R.drawable.ic_launcher_foreground, pendingIntent)
                    "empty" -> noti.notifyBasic(CHANNEL_ID2, NOTIFICATION_ID2,
                            "Alarm", "택배 수거",
                            R.drawable.ic_launcher_foreground, pendingIntent)
                }

            }
        }
    }
}