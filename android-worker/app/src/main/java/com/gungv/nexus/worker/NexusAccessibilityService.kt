package com.gungv.nexus.worker

import android.accessibilityservice.AccessibilityService
import android.view.accessibility.AccessibilityEvent

class NexusAccessibilityService : AccessibilityService() {
    override fun onServiceConnected() {
        super.onServiceConnected()
        WorkerState.connected = true
        WorkerState.lastSnapshot = CapabilityReporter.snapshot(this, true).toString()
    }

    override fun onAccessibilityEvent(event: AccessibilityEvent?) {
        WorkerState.lastSnapshot = CapabilityReporter.snapshot(this, true).toString()
    }

    override fun onInterrupt() {
        WorkerState.connected = false
        WorkerState.lastSnapshot = CapabilityReporter.snapshot(this, false).toString()
    }
}

object WorkerState {
    @Volatile var connected: Boolean = false
    @Volatile var lastSnapshot: String = "{}"
}
