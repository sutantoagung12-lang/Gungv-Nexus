package com.gungv.nexus.worker

import android.accessibilityservice.AccessibilityService
import android.view.accessibility.AccessibilityEvent
import java.util.concurrent.Executors
import java.util.concurrent.ScheduledFuture
import java.util.concurrent.TimeUnit
import org.json.JSONObject

class NexusAccessibilityService : AccessibilityService() {
    private val executor = Executors.newSingleThreadScheduledExecutor()
    private var pollJob: ScheduledFuture<*>? = null

    override fun onServiceConnected() {
        super.onServiceConnected()
        WorkerState.connected = true
        WorkerState.lastSnapshot = CapabilityReporter.snapshot(this, true).toString()
        startCommandPolling()
    }

    override fun onAccessibilityEvent(event: AccessibilityEvent?) {
        WorkerState.lastSnapshot = CapabilityReporter.snapshot(this, true).toString()
    }

    override fun onInterrupt() {
        stopCommandPolling()
        WorkerState.connected = false
        WorkerState.lastSnapshot = CapabilityReporter.snapshot(this, false).toString()
    }

    override fun onDestroy() {
        stopCommandPolling()
        executor.shutdownNow()
        super.onDestroy()
    }

    private fun startCommandPolling() {
        if (pollJob != null) return
        pollJob = executor.scheduleWithFixedDelay({
            val endpoint = WorkerState.endpoint
            val token = WorkerState.token
            if (!endpoint.isNullOrBlank() && !token.isNullOrBlank()) {
                NexusTransport.pollCommands(endpoint, token) { command ->
                    if (command != null) executeCommand(command)
                }
            }
        }, 0, 2, TimeUnit.SECONDS)
    }

    private fun stopCommandPolling() {
        pollJob?.cancel(true)
        pollJob = null
    }

    private fun executeCommand(command: JSONObject) {
        val result = DeviceCommandExecutor.execute(this, command)
        val endpoint = WorkerState.endpoint
        val token = WorkerState.token
        if (!endpoint.isNullOrBlank() && !token.isNullOrBlank()) {
            NexusTransport.sendCommandResult(endpoint, token, result)
        }
    }
}

object WorkerState {
    @Volatile var connected: Boolean = false
    @Volatile var lastSnapshot: String = "{}"
    @Volatile var endpoint: String? = null
    @Volatile var token: String? = null
}
