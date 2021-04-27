package com.example.lockstop

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.webkit.WebViewClient
import kotlinx.android.synthetic.main.activity_log.*
import kotlinx.android.synthetic.main.activity_streaming.*

class LogActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_log)

        LogView.apply {
            settings.javaScriptEnabled = true
            webViewClient = WebViewClient()
        }

        // 주소
        LogView.loadUrl("http://172.30.1.31:8000/record")
    }

    override fun onPause() {
        super.onPause()
        LogView.loadUrl("about:blank")
    }

}