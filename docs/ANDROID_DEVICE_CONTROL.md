# Nexus Android device-control bridge

Adds a narrow authenticated command queue between the serverless Nexus runtime and the Android worker.

Supported actions: back, home, recents, notifications, quick_settings, tap, swipe, and set_text on the focused input field.

Commands use unique IDs, bearer authorization, a short lease for retry after worker interruption, and an explicit result acknowledgement. Unknown actions are rejected.

The Android worker executes commands through the user-enabled AccessibilityService. Android documents global actions and dispatchGesture as AccessibilityService capabilities, and ACTION_SET_TEXT can set text on an accessibility node.

The worker does not expose shell execution, arbitrary JavaScript, credential extraction, screen capture, or privileged system settings.

Current limitation: command polling starts while the AccessibilityService is connected. A foreground-service implementation is intentionally deferred until the command contract is stable.