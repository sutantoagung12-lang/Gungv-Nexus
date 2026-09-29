# Nexus Android Worker

The Android worker is the device-side counterpart of Nexus's Dextop-inspired
adaptive runtime.

Architecture:

    Android Worker
      |
      +-- device identity
      +-- capability probes
      +-- optional AccessibilityService
      +-- capability transport
      |
      v
    Nexus Serverless /device/capabilities
      |
      v
    persistent device snapshot

The worker is intentionally conservative. It reports what is available; it
does not claim privileged virtual-display or window-repositioning support
until a device-specific backend proves those capabilities.

## Setup

1. Build `android-worker` with Android Studio/Gradle.
2. Install the APK on the Android device.
3. Open the app and, only if needed, enable its AccessibilityService from
   Android Settings.
4. Deploy the Nexus serverless runtime.
5. Configure the serverless secret:

   `wrangler secret put NEXUS_DEVICE_TOKEN`

6. Enter the deployed HTTPS Worker URL and the same token in the Android app.
7. Press **Send capabilities to Nexus**.

The server rejects capability registration without the bearer token.

## Current bridge

The Android worker sends:

- Android SDK, manufacturer, model, device
- AccessibilityService state
- window-content capability
- gesture-dispatch capability
- MediaProjection API availability
- observed display count
- conservative privileged capability flags

The server stores the latest report under the Durable Object state and exposes
it through the authenticated `GET /device/capabilities` endpoint.

## Security boundary

The worker does not silently enable Accessibility, capture the screen, inject
input, modify system settings, or execute arbitrary commands. Any future
device-control backend must remain behind explicit Nexus authorization and
must use the capability resolver before selecting a strategy.

Android's AccessibilityService is user-enabled through system settings and can
retrieve window content or dispatch gestures only when the corresponding
service capabilities are declared and granted.
