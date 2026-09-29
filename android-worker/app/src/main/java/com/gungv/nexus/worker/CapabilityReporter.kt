package com.gungv.nexus.worker

import android.content.Context
import android.media.projection.MediaProjectionManager
import android.os.Build
import android.view.WindowManager
import android.hardware.display.DisplayManager
import org.json.JSONObject

object CapabilityReporter {
    fun snapshot(context: Context, serviceConnected: Boolean): JSONObject {
        val dm = context.getSystemService(DisplayManager::class.java)
        val mediaProjection =
            context.getSystemService(MediaProjectionManager::class.java)

        val displayCount = dm?.displays?.size ?: 0

        return JSONObject().apply {
            put("worker", "nexus-android")
            put("version", "0.1.0")
            put("android_sdk", Build.VERSION.SDK_INT)
            put("manufacturer", Build.MANUFACTURER)
            put("model", Build.MODEL)
            put("device", Build.DEVICE)
            put("accessibility_service", serviceConnected)
            put("window_content", serviceConnected)
            put("gesture_dispatch", serviceConnected && Build.VERSION.SDK_INT >= 24)
            put("media_projection_api", mediaProjection != null)
            put("display_count_observed", displayCount)
            put("virtual_display_control", false)
            put("window_reposition_control", false)
            put("privileged_system_control", false)
            put("note", "Capability flags are conservative; unsupported privileged operations remain false.")
        }
    }
}
