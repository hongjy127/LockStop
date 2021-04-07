package com.example.lockstop

import android.app.Activity
import android.content.Intent
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
const val SERVER_URI = "tcp://172.30.1.39:1883"

class MainActivity : AppCompatActivity() {

    val TAG = "MqttActivity"
    lateinit var mqttClient: Mqtt

    companion object {
        const val CHANNEL_ID = "com.example.lockstop"
        const val CHANNEL_NAME = "My Channel"
        const val CHANNEL_DESCRIPTION = "Channel Test"
        const val NOTIFICATION_REQUEST = 0
        const val NOTIFICATION_ID = 100
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

        btnDoor.setOnClickListener {
            startActivity<DoorLockActivity>(
            )
        }

        btnCJ.setOnClickListener {
            startActivity<CJActivity>(
            )
        }

        doorLockView.apply {
            settings.javaScriptEnabled = true
            webViewClient = WebViewClient()
        }

        // mjpeg-streamer 실행
        doorLockView.loadUrl("http://www.naver.com")
    }

    fun onReceived(topic: String, message: MqttMessage) {
        val msg = String(message.payload)



//        val msg = "open"
//        Log.i(TAG, "$topic: $msg")

        when (topic) {
            "iot/doorlock" -> {
                val nextIntent = Intent(this, DoorLockActivity::class.java)
                nextIntent.putExtra("message", msg)


                val noti = Notification(this)
                noti.createNotificationChannel(CHANNEL_ID, CHANNEL_NAME, CHANNEL_DESCRIPTION)
                val pendingIntent = noti.getPendingIntent(
                        DoorLockActivity::class.java,
                        NOTIFICATION_REQUEST)
                when (msg) {
                    "open" -> noti.notifyBasic(CHANNEL_ID, NOTIFICATION_ID,
                            "Alarm", "문열림",
                            R.drawable.ic_launcher_foreground, pendingIntent)
                    "error" -> noti.notifyBasic(CHANNEL_ID, NOTIFICATION_ID,
                            "Alarm", "비밀번호 3회 오류",
                            R.drawable.ic_launcher_foreground, pendingIntent)
                    else -> noti.notifyBasic(CHANNEL_ID, NOTIFICATION_ID,
                            "error", "error",
                            R.drawable.ic_launcher_foreground, pendingIntent)
                }
            }
            "iot/CJ" -> {
                val nextIntent = Intent(this,CJActivity::class.java)
                nextIntent.putExtra("message", msg)


                val noti = Notification(this)
                noti.createNotificationChannel(CHANNEL_ID, CHANNEL_NAME, CHANNEL_DESCRIPTION)
                val pendingIntent = noti.getPendingIntent(
                        CJActivity::class.java,
                        NOTIFICATION_REQUEST)
                when (msg) {
                    "full" -> noti.notifyBasic(CHANNEL_ID, NOTIFICATION_ID,
                            "Alarm", "택배 도착",
                            R.drawable.ic_launcher_foreground, pendingIntent)
                    "empty" -> noti.notifyBasic(CHANNEL_ID, NOTIFICATION_ID,
                            "Alarm", "택배 수거",
                            R.drawable.ic_launcher_foreground, pendingIntent)
                    else -> noti.notifyBasic(CHANNEL_ID, NOTIFICATION_ID,
                            "error", "error",
                            R.drawable.ic_launcher_foreground, pendingIntent)
                }

//        if (topic == "iot/doorlock") {
////            txtMqtt.text = "$topic: $msg"
//            val noti = Notification(this)
//            noti.createNotificationChannel(CHANNEL_ID, CHANNEL_NAME, CHANNEL_DESCRIPTION)
//            val pendingIntent = noti.getPendingIntent(
//                    DoorLockActivity::class.java,
//                    NOTIFICATION_REQUEST)
//            when (msg){
//                "open"->noti.notifyBasic(CHANNEL_ID, NOTIFICATION_ID,
//                        "Alarm", "문열림",
//                        R.drawable.ic_launcher_foreground, pendingIntent)
//                "error"->noti.notifyBasic(CHANNEL_ID, NOTIFICATION_ID,
//                        "Alarm", "비밀번호 3회 오류",
//                        R.drawable.ic_launcher_foreground, pendingIntent)
//                else->noti.notifyBasic(CHANNEL_ID, NOTIFICATION_ID,
//                        "error", "error",
//                        R.drawable.ic_launcher_foreground, pendingIntent)
//            }

            }
        }
    }
}