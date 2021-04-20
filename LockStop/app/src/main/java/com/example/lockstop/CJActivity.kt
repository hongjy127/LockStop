package com.example.lockstop

import android.content.Intent
import android.net.Uri
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import android.widget.Toast
import com.example.mylib.Notification
import com.example.mylib.net.Mqtt
import com.example.mylib.openapi.piapi.PiApi
import kotlinx.android.synthetic.main.activity_c_j.*
import kotlinx.android.synthetic.main.activity_c_j.btnAlarm
import kotlinx.android.synthetic.main.activity_c_j.btnCall
import kotlinx.android.synthetic.main.activity_c_j.btnHome
import kotlinx.android.synthetic.main.activity_c_j.btnOK
import org.eclipse.paho.client.mqttv3.MqttMessage
import org.jetbrains.anko.startActivity


class CJActivity : AppCompatActivity() {

    lateinit var mqttClient: Mqtt

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_c_j)

        mqttClient = Mqtt(this, SERVER_URI)
        try {
            mqttClient.setCallback(::onReceived)
            Log.d("Mqtt", "connect")
            mqttClient.connect(arrayOf<String>("iot/loadcell"))
        } catch (e: Exception) {
            e.printStackTrace()
        }

        val intent = getIntent()
        var msg = intent.getStringExtra("message")
//        Log.i("mqtt_msg", "$msg")

        when(msg) {
            "full" -> txtCJ.text = "택배 도착"
            "empty" -> txtCJ.text = "택배 수거"
        }

        btnHome.setOnClickListener {
            startActivity<MainActivity>(
            )
        }

        btnDoor.setOnClickListener {
            startActivity<DoorLockActivity>(
            )
        }

        btnOK.setOnClickListener {
            Toast.makeText(application, "확인 되었습니다.", Toast.LENGTH_LONG).show()
        }

        btnAlarm.setOnClickListener{
            Toast.makeText(application, "경보음이 울립니다.", Toast.LENGTH_LONG).show()
            PiApi.controlBuzzer("1", "on") {

            }
        }

        btnCall.setOnClickListener{
            var uri = Uri.parse("tel:010-0000-0000")
            var intent = Intent(Intent.ACTION_DIAL, uri)
            startActivity(intent)
        }

    }
    fun onReceived(topic: String, message: MqttMessage) {
        var msg = String(message.payload)
        txtWeight.text = "택배 무게: $msg kg"
    }
}