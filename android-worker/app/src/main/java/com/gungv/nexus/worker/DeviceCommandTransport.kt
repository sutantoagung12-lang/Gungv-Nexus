package com.gungv.nexus.worker

import java.net.HttpURLConnection
import java.net.URI
import java.net.URL
import java.nio.charset.StandardCharsets
import java.util.concurrent.Executors
import org.json.JSONObject

object DeviceCommandTransport {
    private val executor = Executors.newSingleThreadExecutor()

    fun poll(endpoint: String, token: String, callback: (JSONObject?) -> Unit) {
        val clean = endpoint.trim().removeSuffix("/")
        executor.execute {
            val command = try {
                val uri = URI(clean + "/device/commands")
                val connection = open(uri, token, "GET")
                val body = response(connection)
                if (body.startsWith("HTTP ")) null else {
                    val json = JSONObject(body)
                    if (json.optBoolean("available", false)) json.optJSONObject("command") else null
                }
            } catch (_: Exception) { null }
            callback(command)
        }
    }

    fun result(endpoint: String, token: String, result: CommandResult) {
        val clean = endpoint.trim().removeSuffix("/")
        executor.execute {
            try {
                val uri = URI(clean + "/device/command-result")
                val payload = result.toJson().toString().toByteArray(StandardCharsets.UTF_8)
                val connection = open(uri, token, "POST").apply {
                    doOutput = true
                    setRequestProperty("Content-Type", "application/json")
                }
                connection.outputStream.use { it.write(payload) }
                response(connection)
            } catch (_: Exception) { }
        }
    }

    private fun open(uri: URI, token: String, method: String): HttpURLConnection {
        require(uri.scheme == "https" || uri.host == "10.0.2.2" || uri.host == "127.0.0.1")
        return (URL(uri.toString()).openConnection() as HttpURLConnection).apply {
            requestMethod = method; connectTimeout = 10000; readTimeout = 10000
            setRequestProperty("Authorization", "Bearer " + token)
            setRequestProperty("Accept", "application/json")
        }
    }

    private fun response(connection: HttpURLConnection): String {
        val stream = if (connection.responseCode in 200..399) connection.inputStream else connection.errorStream
        val body = stream?.bufferedReader()?.use { it.readText() } ?: ""
        return "HTTP " + connection.responseCode + ": " + body
    }
}