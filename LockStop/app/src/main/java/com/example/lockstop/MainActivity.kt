package com.example.lockstop

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.webkit.WebViewClient
import kotlinx.android.synthetic.main.activity_main.*
import org.jetbrains.anko.startActivity

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

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
}