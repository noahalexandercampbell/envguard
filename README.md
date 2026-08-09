# envguard

**Environment variable guard for local builds and CI.**

Compare one or more `.env` files against a contract and immediately see missing, extra, or empty variables. Useful for onboarding, CI checks, and eliminating `works on my machine` bugs.

Source and issues: https://github.com/noahalexandercampbell/envguard

## Features

- Load `.env`, `.env.local`, `.env.ci`, and other dotenv variants.
- Validate against a YAML/JSON **required-variables profile**.
- Show missing, extra, blank, and unmasked/secret variables.
- Export a clean subset suitable for CI consumption.
- Safe by default: never prints secret values to stdout/stderr.

## Installation

```bash
pip install envguard
```

## Usage

```bash
# Check default .env files in current directory
envguard check

# Check specific file against a profile
envguard check --file .env.local --profile profiles/default.yml

# Show diff: missing vs extra
envguard diff --file .env --profile profiles/production.yml

# Merge plus validation in one step
envguard merge --base .env --overlay .env.local --destination merged.env --profile profiles/default.yml
```

## Project structure

```
envguard/
├── envguard/
│   ├── __init__.py
│   ├── cli.py
│   ├── loader.py
│   ├── models.py
│   ├── profile.py
│   └── reporter.py
├── profiles/
│   ├── ci.yml
│   ├── default.yml
│   ├── strict.yml
│   ├── default.json
│   └── strict.json
├── pyproject.toml
├── tests/
│   └── test_envguard.py
└── README.md
```
