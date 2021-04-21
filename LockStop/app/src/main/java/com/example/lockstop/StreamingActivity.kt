package com.example.lockstop

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.webkit.WebViewClient
import kotlinx.android.synthetic.main.activity_streaming.*

class StreamingActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_streaming)

        doorLockView.apply {
            settings.javaScriptEnabled = true
            webViewClient = WebViewClient()
        }

        // 주소
        doorLockView.loadUrl("http://172.30.1.93:8000/mjpeg")
//        doorLockView.loadUrl("http://172.30.1.42:8000/mjpeg/?mode=stream")
    }
    override fun onPause() {
        super.onPause()
        doorLockView.loadUrl("about:blank")
    }
}