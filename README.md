# Android MultiPass (Frida)

Android MultiPass hooks Android lock credential verification with Frida and lets you unlock using multiple strategies, while still forwarding verification through the real device password.

## Features

MultiPass supports several acceptance modes in addition to the main password:

- Additional exact passwords (`-a`, `--additional`)
- Regex-based password matching (`-r`, `--regex`)
- Unordered-character matching (`-u`, `--unordered`)
- Full bypass mode (`-d`, `--disable`)

All accepted inputs are converted into the real password before Android performs verification.

## How It Works

1. Python parses and validates CLI arguments.
2. Python attaches to `system_server` over USB using Frida.
3. Python builds and loads `hook.js`.
4. Python passes runtime config to JavaScript via Frida RPC.
5. JavaScript hooks:
   `com.android.server.locksettings.LockSettingsService.doVerifyCredential`.
6. On each password attempt, the hook:
   - reads the input credential
   - checks configured acceptance rules
   - replaces accepted input with the real password
   - calls the original Android method

## Acceptance Rules

An entered password is accepted if any rule matches:

1. Disable mode is enabled (`--disable`)
2. It exactly equals the real password (`--password`)
3. It is in the additional password list (`--additional`)
4. It matches the regex pattern (`--regex`)
5. It is a character-anagram match of real/additional passwords (`--unordered`)

## CLI Arguments

- `-p`, `--password` (required)
  Real lock-screen password configured on the device.
- `-a`, `--additional` (optional, default: empty list)
  One or more additional exact passwords.
- `-r`, `--regex` (optional, default: `(?!)`)
  Regex pattern used to accept additional passwords. Default pattern rejects everything.
- `-u`, `--unordered` (optional flag)
  Accept passwords that contain the same characters in any order.
- `-d`, `--disable` (optional flag)
  Disable verification checks and accept any entered password.

### Validation

- `--password` must be at least 4 characters.
- Every entry in `--additional` must be at least 4 characters.
- `--regex` must compile as a valid Python regular expression.

## Requirements

- Python 3.9+
- `frida` Python package
- Android device connected over USB
- Frida environment compatible with target device
- Privileges sufficient to attach to `system_server`

## Install

```bash
py -m pip install frida
```

## Usage

Basic:

```bash
py main.py -p 1234
```

With additional passwords:

```bash
py main.py -p 1234 -a 1111 2222 3333
```

With regex:

```bash
py main.py -p 1234 -r "^(1111|2222)$"
```

With unordered matching:

```bash
py main.py -p 1234 -a 9876 -u
```

With disable mode:

```bash
py main.py -p 1234 -d
```

Combined example:

```bash
py main.py -p 1234 -a 1111 2222 -r "^9[0-9]{3}$" -u
```

## Logging

At runtime, MultiPass logs:

- each entered password
- why a password was accepted (password/additional/regex/unordered/disable)
- rejected attempts
- Frida script errors (description + stack)

## Project Structure

- [main.py](main.py): Entry point, logging setup, argument parsing, injection, process keep-alive.
- [argument_parser.py](argument_parser.py): CLI definition and argument validation.
- [hook_injector.py](hook_injector.py): Frida compile/load, process attach, RPC config injection, message handling.
- [hook.js](hook.js): Credential interception and acceptance logic.
