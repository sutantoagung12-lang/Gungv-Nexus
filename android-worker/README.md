# Nexus Android Worker

A small Android-side capability adapter for Gungv-Nexus.

It implements the next Dextop-inspired layer without assuming privileged
Android APIs. The worker reports conservative capabilities and can use an
AccessibilityService only after the user explicitly enables it in Android
settings.

Current capabilities:

- Android SDK / manufacturer / model / device identity
- accessibility-service state
- window-content capability when the service is connected
- gesture-dispatch capability when the service is connected
- MediaProjection API availability
- observed display count
- explicit false values for virtual-display control, window repositioning,
  and privileged system control until a device-specific backend is added

The worker intentionally does not silently enable Accessibility, capture the
screen, inject input, change system settings, or claim Dextop-level privileged
control.

## Android policy boundary

Android requires the user to explicitly enable an AccessibilityService.
Gesture dispatch requires the corresponding service capability. Accessibility
is therefore an opt-in control channel, not a hidden background mechanism.

The next implementation stage is a Nexus transport adapter that sends this
capability snapshot to a configured Nexus endpoint after explicit user setup.
