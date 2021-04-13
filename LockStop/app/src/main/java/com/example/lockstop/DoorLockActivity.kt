package com.example.lockstop

import android.content.Intent
import android.content.res.ColorStateList
import android.graphics.Color
import android.net.Uri
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import android.widget.Toast
import com.example.mylib.openapi.piapi.PiApi
import kotlinx.android.synthetic.main.activity_door_lock.*
import kotlinx.android.synthetic.main.activity_door_lock.btnAlarm
import kotlinx.android.synthetic.main.activity_door_lock.btnCall
import kotlinx.android.synthetic.main.activity_door_lock.btnHome
import kotlinx.android.synthetic.main.activity_door_lock.btnOK
import org.jetbrains.anko.startActivity

class DoorLockActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_door_lock)

        val intent = getIntent()
        var msg = intent.getStringExtra("message")
//        Log.i("mqtt_msg", "$msg")


        when(msg) {
            "open" -> txtDoor.text = "문열림"
            "error" -> txtDoor.text = "비밀번호 3회 오류"
        }

        btnHome.setOnClickListener {
            startActivity<MainActivity>(
            )
        }

        btnCJ.setOnClickListener {
            startActivity<CJActivity>(
            )
        }

        btnOK.setOnClickListener {
            Toast.makeText(application, "확인 되었습니다.", Toast.LENGTH_LONG).show()
        }

        btnAlarm.setOnClickListener{
            PiApi.controlBuzzer("1", "on") {
//                if(it.result == "OK") {
//                    Toast.makeText(application, "경보음이 울립니다.", Toast.LENGTH_LONG).show()
//                }
            }
        }

        btnCall.setOnClickListener{
            var uri = Uri.parse("tel:010-0000-0000")
            var intent = Intent(Intent.ACTION_DIAL, uri)
            startActivity(intent)
        }
        

    }
}