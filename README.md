# Android MultiPass (Frida)

Android MultiPass hooks Android lock credential verification with Frida and lets you control password acceptance using multiple strategies, while still forwarding verification through the real device password when appropriate.

## Features

MultiPass supports several acceptance modes and device-state controls in addition to the main password:

- Extra exact passwords (`--extra`)
- Regex-based password matching (`--regex`)
- Anagram matching (`--anagram`)
- Immutable mode (`--immutable`)
- Full bypass mode (`--unlocked`)
- Hard lock mode (`--locked`)

Accepted inputs are converted into the real password before Android performs verification. Rejected inputs are replaced with an always-failing credential.

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
- rejects input when `--locked` is enabled or when `--immutable` is enabled and the device is already unlocked
- calls the original Android method

## Acceptance Rules

An entered password is accepted if any rule matches:

1. Full bypass mode is enabled (`--unlocked`)
2. It exactly equals the real password (`--password`)
3. It is in the extra password list (`--extra`)
4. It matches the regex pattern (`--regex`)
5. It is a character-anagram match of the real or extra passwords (`--anagram`)

An entered password is rejected before acceptance checks if either rule matches:

1. `--locked` is enabled
2. `--immutable` is enabled and the device is currently unlocked

## CLI Arguments

- `--password` (required)
  Real lock-screen password configured on the device.
- `--extra` (optional, default: empty list)
  One or more additional exact passwords.
- `--regex` (optional, default: `(?!)`)
  Regex pattern used to accept passwords. Default pattern rejects everything.
- `--anagram` (optional flag)
  Accept passwords that contain the same characters in any order.
- `--immutable` (optional flag)
  Do not allow password changes while the device is already unlocked.
- `--unlocked` (optional flag)
  Accept any entered password.
- `--locked` (optional flag)
  Reject all entered passwords.

### Validation

- `--password` must be at least 4 characters.
- Every entry in `--extra` must be at least 4 characters.
- `--regex` must compile as a valid Python regular expression.
- `--locked` and `--unlocked` cannot be used together.

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

With extra passwords:

```bash
py main.py -p 1234 -e 1111 2222 3333
```

With regex:

```bash
py main.py -p 1234 -r "^(1111|2222)$"
```

With anagram matching:

```bash
py main.py -p 1234 -e 9876 -a
```

With immutable mode:

```bash
py main.py -p 1234 -i
```

With full bypass mode:

```bash
py main.py -p 1234 -u
```

With hard lock mode:

```bash
py main.py -p 1234 -l
```

Combined example:

```bash
py main.py -p 1234 -e 1111 2222 -r "^9[0-9]{3}$" -a
```

## Logging

At runtime, MultiPass logs:

- each entered password
- why a password was accepted or rejected (password/extra/regex/anagram/unlocked/locked/immutable)
- rejected attempts
- colored log prefixes for debug/info/warning/error/critical messages
- Frida script errors (description + stack)

## Project Structure

- [main.py](main.py): Entry point, logging setup, argument parsing, injection, process keep-alive.
- [argument_parser.py](argument_parser.py): CLI definition and argument validation.
- [logger_configuration.py](logger_configuration.py): Colored log prefix formatting.
- [hook_injector.py](hook_injector.py): Frida compile/load, process attach, RPC config injection, message handling.
- [hook.js](hook.js): Credential interception and acceptance logic.
