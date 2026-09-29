package com.gungv.nexus.worker

import android.content.Context
import java.net.HttpURLConnection
import java.net.URI
import java.net.URL
import java.nio.charset.StandardCharsets
import java.util.concurrent.Executors

object NexusTransport {
    private val executor = Executors.newSingleThreadExecutor()

    fun send(context: Context, endpoint: String, token: String, callback: (String) -> Unit) {
        val clean = endpoint.trim().removeSuffix("/")
        executor.execute {
            val result = try {
                val uri = URI("${clean}/device/capabilities")
                require(uri.scheme == "https" || uri.host == "10.0.2.2" || uri.host == "127.0.0.1") {
                    "Nexus endpoint must use HTTPS"
                }
                val payload = CapabilityReporter.snapshot(context, WorkerState.connected)
                    .toString()
                    .toByteArray(StandardCharsets.UTF_8)
                val connection = (URL(uri.toString()).openConnection() as HttpURLConnection).apply {
                    requestMethod = "POST"
                    connectTimeout = 10000
                    readTimeout = 10000
                    doOutput = true
                    setRequestProperty("Content-Type", "application/json")
                    setRequestProperty("Authorization", "Bearer ${token}")
                }
                connection.outputStream.use { it.write(payload) }
                val body = connection.inputStream.bufferedReader().use { it.readText() }
                "HTTP ${connection.responseCode}: $body"
            } catch (error: Exception) {
                "ERROR: ${error.javaClass.simpleName}: ${error.message}"
            }
            callback(result)
        }
    }
}
