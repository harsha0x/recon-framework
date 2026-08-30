# ReconFramework

A modular, plugin-based recon/vulnerability-scanning tool written in Python. Instead of one monolithic script, every check is a self-contained plugin that inherits from a shared abstract base class — new checks can be added without touching the core.

## Why plugin-based

Real recon tools need to run many independent checks (headers, exposed files, subdomains, etc.) against a target. A plugin architecture means:
- Each check is isolated — one plugin failing doesn't crash the scan
- Every plugin returns results in the same shape, so the core never needs to know what a specific plugin checks for
- New checks can be added by writing a new class, without modifying existing code

## Architecture

- **`module.py`** — the `Module` abstract base class. Every plugin inherits from it and must implement `run()`. The base class provides `execute()`, which calls `run()` and validates that the result matches the expected shape (`target`, `plugin`, `findings`) before handing it back — so a malformed plugin fails safely instead of breaking the scan.
- **`header_audit.py`** — checks a target for missing security headers (`X-Frame-Options`, `Content-Security-Policy`, `Strict-Transport-Security`).
- **`sensitive_file_check.py`** — checks a target for commonly exposed sensitive paths (`.env`, `.git/config`, backup files, admin panels, etc.), using baseline-response comparison to avoid false positives on sites that return `200` for every path (custom error pages).
- **`main.py`** — the CLI entry point. Takes a target URL, runs every registered plugin against it, and prints a combined report.

## Usage

```bash
pip install requests
python3 main.py https://example.com
```

Example output:
```
Scanning https://example.com ...
[header_audit] target: https://example.com
  [MEDIUM] X-Frame-Options header not found
[sensitive_file_check] target: https://example.com
  No issues found.
```

## Adding a new plugin

1. Create a new file, e.g. `my_check.py`.
2. Define a class that inherits from `Module` and implements `run(self) -> dict`, returning:
   ```python
   {
       "target": self.target,
       "plugin": "my_check",
       "findings": [{"description": "...", "severity": "..."}],
   }
   ```
3. Import and add it to the `plugins` list in `main.py`.

## Roadmap

- Dynamic plugin discovery (auto-load any valid plugin from a `plugins/` folder, instead of hardcoding the list in `main.py`)
- Concurrent plugin execution
- JSON/CSV export of results
- Additional plugins (subdomain enumeration, TLS/cert checks)

## Disclaimer

For authorized security testing only. Only run this against targets you own or have explicit permission to test.