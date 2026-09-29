package com.gungv.nexus.worker

import android.content.Intent
import android.os.Bundle
import android.provider.Settings
import android.widget.Button
import android.widget.EditText
import android.widget.LinearLayout
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {
    private lateinit var status: TextView
    private lateinit var endpoint: EditText
    private lateinit var token: EditText

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        endpoint = EditText(this).apply {
            hint = "Nexus Worker URL (https://...)"
            setText(getPreferences(MODE_PRIVATE).getString("endpoint", ""))
        }
        token = EditText(this).apply {
            hint = "NEXUS_DEVICE_TOKEN"
            inputType = 0x00000081
            setText(getPreferences(MODE_PRIVATE).getString("token", ""))
        }

        status = TextView(this).apply {
            textSize = 14f
            setPadding(32, 48, 32, 24)
        }

        val openAccessibility = Button(this).apply {
            text = "Open Accessibility settings"
            setOnClickListener {
                startActivity(Intent(Settings.ACTION_ACCESSIBILITY_SETTINGS))
            }
        }

        val send = Button(this).apply {
            text = "Send capabilities to Nexus"
            setOnClickListener { sendCapabilities() }
        }

        val refresh = Button(this).apply {
            text = "Refresh capabilities"
            setOnClickListener { refreshStatus() }
        }

        setContentView(
            LinearLayout(this).apply {
                orientation = LinearLayout.VERTICAL
                addView(status)
                addView(endpoint)
                addView(token)
                addView(send)
                addView(openAccessibility)
                addView(refresh)
            }
        )
        refreshStatus()
    }

    override fun onResume() {
        super.onResume()
        refreshStatus()
    }

    private fun sendCapabilities() {
        val url = endpoint.text.toString().trim()
        val secret = token.text.toString()
        if (url.isEmpty() || secret.isEmpty()) {
            Toast.makeText(this, "Endpoint dan token harus diisi", Toast.LENGTH_SHORT).show()
            return
        }
        getPreferences(MODE_PRIVATE).edit()
            .putString("endpoint", url)
            .putString("token", secret)
            .apply()
        NexusTransport.send(this, url, secret) { result ->
            runOnUiThread { Toast.makeText(this, result, Toast.LENGTH_LONG).show() }
        }
    }

    private fun refreshStatus() {
        status.text = CapabilityReporter.snapshot(this, WorkerState.connected).toString(2)
    }
}
