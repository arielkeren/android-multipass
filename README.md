# Android MultiPass (Frida)

Set multiple additional lock-screen passwords on an Android device by hooking the system lock credential verification flow with Frida.

This project lets you define:

- one real device password
- many extra passwords that should be accepted

When one of the extra passwords is entered, the hook replaces it with the real password before Android verifies credentials.

## Overview

Android MultiPass attaches to Android system_server and installs a runtime hook in `LockSettingsService` using Frida.
The hook checks incoming credentials against a configured list of additional passwords. If the input matches, it swaps the credential bytes with the actual password bytes and lets normal Android verification continue.

This allows multiple accepted input passwords while preserving one canonical real password on the system.

## How It Works

1. Python parses command-line arguments for:

- actual password
- one or more additional passwords

2. Python attaches to process:

- `system_server`

3. Python loads the Frida JavaScript hook and calls an exported initializer with runtime config.

4. JavaScript hooks:

- `com.android.server.locksettings.LockSettingsService.doVerifyCredential`

5. On each verification:

- read incoming credential bytes
- convert bytes to string
- if input is in additional passwords, replace credential with actual password bytes
- call original method

## Features

- Runtime configuration via CLI (no hardcoded passwords required)
- Supports multiple additional passwords
- Keeps the Android verification path intact by forwarding to original method
- Clear separation between argument parsing, injection, and hook logic
- Works through Frida RPC initialization

## Requirements

- Python 3.9+ (recommended)
- Frida Python package
- Frida runtime/tooling compatible with your target device
- Android device connected over USB
- Sufficient privileges to attach to `system_server`
- Environment where hooking `system_server` is possible

## Usage

1. Install Python dependencies:

   ```bash
   py -m pip install frida
   ```

2. Ensure Frida setup on host/device is complete and versions are compatible.

3. Run the script:

   ```bash
   py main.py --actual-password YOUR_REAL_PASSWORD --additional-passwords PASS1 PASS2 PASS3
   ```

**Argument details:**

- `--actual-password`
  The real lock-screen password configured on the device.
- `--additional-passwords`
  One or more alternative passwords that should also be accepted.

## Example

**Example command:**

```bash
py main.py --actual-password 1234 --additional-passwords 1111 2222 3333 4444
```

**Behavior:**

- Every password entered in the lock-screen is intercepted.
- If the entered password matches one of 1111, 2222, 3333 or 4444, it is changed to the actual password, 1234.
- Android unlocks the device, as if 1234 was entered.

## Project Structure

- [main.py](main.py)
  Entry point. Parses arguments, injects hook, and keeps process alive.
- [argument_parser.py](argument_parser.py)
  Defines CLI options and validation.
- [hook_injector.py](hook_injector.py)
  Builds JS with Frida compiler, attaches to system_server, loads script, sends config via RPC.
- [hook.js](hook.js)
  Installs Java hook and performs credential substitution logic.
