package com.gungv.nexus.worker

import android.accessibilityservice.AccessibilityService
import android.graphics.Path
import android.os.Bundle
import android.view.accessibility.AccessibilityNodeInfo
import org.json.JSONObject

data class CommandResult(val id: String, val ok: Boolean, val action: String, val error: String? = null, val detail: String? = null) {
    fun toJson(): JSONObject = JSONObject().apply {
        put("id", id); put("ok", ok); put("action", action)
        if (error != null) put("error", error)
        if (detail != null) put("detail", detail)
    }
}

object DeviceCommandExecutor {
    private val allowed = setOf("back", "home", "recents", "notifications", "quick_settings", "tap", "swipe", "set_text")

    fun execute(service: AccessibilityService, command: JSONObject): CommandResult {
        val id = command.optString("id")
        val action = command.optString("action")
        if (id.isBlank()) return CommandResult("", false, action, "missing_command_id")
        if (action !in allowed) return CommandResult(id, false, action, "unsupported_action")
        return try {
            when (action) {
                "back" -> global(service, id, action, AccessibilityService.GLOBAL_ACTION_BACK)
                "home" -> global(service, id, action, AccessibilityService.GLOBAL_ACTION_HOME)
                "recents" -> global(service, id, action, AccessibilityService.GLOBAL_ACTION_RECENTS)
                "notifications" -> global(service, id, action, AccessibilityService.GLOBAL_ACTION_NOTIFICATIONS)
                "quick_settings" -> global(service, id, action, AccessibilityService.GLOBAL_ACTION_QUICK_SETTINGS)
                "tap" -> tap(service, command)
                "swipe" -> swipe(service, command)
                "set_text" -> setText(service, command)
                else -> CommandResult(id, false, action, "unsupported_action")
            }
        } catch (e: Exception) { CommandResult(id, false, action, "execution_error", e.message) }
    }

    private fun global(service: AccessibilityService, id: String, action: String, globalAction: Int): CommandResult {
        val ok = service.performGlobalAction(globalAction)
        return if (ok) CommandResult(id, true, action) else CommandResult(id, false, action, "global_action_failed")
    }

    private fun tap(service: AccessibilityService, command: JSONObject): CommandResult {
        val id = command.optString("id")
        val x = command.optDouble("x", Double.NaN); val y = command.optDouble("y", Double.NaN)
        if (!x.isFinite() || !y.isFinite() || x < 0 || y < 0) return CommandResult(id, false, "tap", "invalid_coordinates")
        val path = Path().apply { moveTo(x.toFloat(), y.toFloat()) }
        val gesture = android.accessibilityservice.GestureDescription.Builder().addStroke(
            android.accessibilityservice.GestureDescription.StrokeDescription(path, 0, 80)).build()
        val accepted = service.dispatchGesture(gesture, null, null)
        return if (accepted) CommandResult(id, true, "tap") else CommandResult(id, false, "tap", "gesture_dispatch_failed")
    }

    private fun swipe(service: AccessibilityService, command: JSONObject): CommandResult {
        val id = command.optString("id")
        val x1 = command.optDouble("x1", Double.NaN); val y1 = command.optDouble("y1", Double.NaN)
        val x2 = command.optDouble("x2", Double.NaN); val y2 = command.optDouble("y2", Double.NaN)
        val duration = command.optLong("duration_ms", 400L).coerceIn(80L, 5000L)
        if (!listOf(x1, y1, x2, y2).all { it.isFinite() && it >= 0 }) return CommandResult(id, false, "swipe", "invalid_coordinates")
        val path = Path().apply { moveTo(x1.toFloat(), y1.toFloat()); lineTo(x2.toFloat(), y2.toFloat()) }
        val gesture = android.accessibilityservice.GestureDescription.Builder().addStroke(
            android.accessibilityservice.GestureDescription.StrokeDescription(path, 0, duration)).build()
        val accepted = service.dispatchGesture(gesture, null, null)
        return if (accepted) CommandResult(id, true, "swipe") else CommandResult(id, false, "swipe", "gesture_dispatch_failed")
    }

    private fun setText(service: AccessibilityService, command: JSONObject): CommandResult {
        val id = command.optString("id"); val text = command.optString("text", "")
        if (text.length > 10000) return CommandResult(id, false, "set_text", "text_too_long")
        val node = service.findFocus(AccessibilityNodeInfo.FOCUS_INPUT)
            ?: return CommandResult(id, false, "set_text", "input_focus_not_found")
        val args = Bundle().apply { putCharSequence(AccessibilityNodeInfo.ACTION_ARGUMENT_SET_TEXT_CHARSEQUENCE, text) }
        val ok = node.performAction(AccessibilityNodeInfo.ACTION_SET_TEXT, args)
        node.recycle()
        return if (ok) CommandResult(id, true, "set_text") else CommandResult(id, false, "set_text", "set_text_failed")
    }
}