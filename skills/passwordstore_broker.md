---
name: passwordstore-broker
description: Enforce safe secret handling by collecting secrets through one-time HTTPS forms, storing them in pass via scripts/vault.sh, and executing tools with environment injection via scripts/run_with_secret.sh so raw secrets do not enter chat context or logs.
author: bieggerm
version: 2.1.0
trigger: "store a secret", "add credentials", "run with secret", "vault", "password store", "secret management"
---

# Passwordstore Broker

A secure bridge between AI agents and the Unix `pass` password manager. Secrets are collected through one-time HTTPS forms, stored in the GPG-encrypted vault, and injected into child processes as environment variables — so **raw secrets never enter chat context or logs**.

## Architecture

```
User --> HTTPS one-time form --> scripts/vault.sh --> GPG-encrypted pass store
                                                          |
                                                    scripts/run_with_secret.sh
                                                          |
                                                   child process (env var)
```

## Prerequisites

The following tools must be available. Install them if missing:

```bash
brew install pass gnupg qrencode
pip install pyotp cryptography flask
```

## Setup

### 1. Initialize GPG Key

If the user doesn't have a GPG key, generate one:

```bash
gpg --full-generate-key
```

### 2. Initialize the Password Store

```bash
pass init <gpg-key-id>
```

### 3. Set Up TOTP for LAN Access

Generate a TOTP secret for securing the one-time HTTPS intake form:

```bash
python3 -c "import pyotp; s = pyotp.random_base32(); print(s)" > ~/.passwordstore-broker/totp.secret
chmod 600 ~/.passwordstore-broker/totp.secret
```

Optionally generate a QR code for the user's authenticator app:

```bash
qrencode -t ansiutf8 "otpauth://totp/PasswordstoreBroker?secret=$(cat ~/.passwordstore-broker/totp.secret)"
```

## Actions

### Collect a Secret (HTTPS Intake)

Start the one-time HTTPS form server to collect a secret from the user's browser:

```bash
python3 scripts/get_password_from_user.py --port 8443 --secret-name <name>
```

The server:
- Reads the TOTP secret from `~/.passwordstore-broker/totp.secret`
- Serves a single-use HTTPS form on `https://localhost:8443`
- Validates the user's TOTP code before accepting the secret
- Pipes the submitted value directly to `scripts/vault.sh put <name>`
- Shuts down after one successful submission

### Store a Secret (Vault)

```bash
scripts/vault.sh put <secret-name>
```

Reads from stdin and stores the value in `pass` under the given name. The value is GPG-encrypted at rest.

```bash
scripts/vault.sh get <secret-name>
```

Decrypts and prints the secret to stdout. Use only within pipes or subshells — never display to the user.

```bash
scripts/vault.sh list
```

Lists stored secret names (not values).

### Run a Command with a Secret

```bash
scripts/run_with_secret.sh <secret-name> <ENV_VAR_NAME> <command> [args...]
```

This decrypts the named secret and injects it as the specified environment variable into the child process:

```bash
secret_value="$(scripts/vault.sh get "$secret_name")"
exec env "$env_name=$secret_value" "$@"
```

**Example:**

```bash
scripts/run_with_secret.sh github-token GITHUB_TOKEN gh api /user
```

### Quick Inline Usage (Fallback)

For one-off commands where the wrapper script is overkill:

```bash
<ENV_VAR>="$(scripts/vault.sh get <secret-name>)" <command> [args...]
```

Example:

```bash
OPENAI_API_KEY="$(scripts/vault.sh get openai-key)" python3 my_script.py
```

## Security Guardrails

- Never ask users to paste raw secrets into chat.
- Never echo secret values back to user.
- Never store secrets in repo files, commit messages, issue comments, or transcripts.
- Always use the HTTPS intake form or `vault.sh put` with stdin for secret collection.
- Always use `run_with_secret.sh` or the inline fallback for secret injection.
- If a secret is needed for a command, retrieve it through the vault — never ask the user to supply it in conversation.

## Supported Secret Types

- API keys (OpenAI, GitHub, AWS, etc.)
- Database passwords
- OAuth tokens
- SSH passphrases
- Any string credential

## Error Handling

- If `pass` is not installed, prompt the user to run `brew install pass gnupg`.
- If no GPG key exists, walk the user through `gpg --full-generate-key`.
- If the TOTP secret file is missing, regenerate it with the setup command.
- If the HTTPS form server fails to start, check that port 8443 is available and `openssl` can generate a self-signed cert.
