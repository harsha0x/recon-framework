# ReconFramework

A modular, plugin-based recon/vulnerability-scanning tool written in Python. Every check is a self-contained plugin, discovered and loaded automatically at runtime — adding a new check means dropping a new file into `plugins/`, with no changes to the core.

## Why plugin-based

Real recon tools need to run many independent checks (headers, exposed files, subdomains, etc.) against a target. A plugin architecture means:
- Each check is isolated — one plugin failing doesn't crash the scan
- Every plugin returns results in the same shape, so the core never needs to know what a specific plugin checks for
- New checks can be added by dropping a new file into `plugins/` — no changes to existing code, and no manual registration

## Architecture

- **`module.py`** — the `Module` abstract base class. Every plugin inherits from it and must implement `run()`. The base class provides `execute()`, which calls `run()` and validates that the result matches the expected shape (`target`, `plugin`, `findings`) before handing it back — so a malformed plugin fails safely instead of breaking the scan.
- **`plugin_discovery.py`** — scans the `plugins/` folder at runtime, dynamically imports every `.py` file it finds, and inspects each module for classes that subclass `Module`. No plugin needs to be manually registered anywhere — if it's a valid `Module` subclass sitting in `plugins/`, it gets picked up automatically.
- **`plugins/header_audit.py`** — checks a target for missing security headers (`X-Frame-Options`, `Content-Security-Policy`, `Strict-Transport-Security`).
- **`plugins/sensitive_file_check.py`** — checks a target for commonly exposed sensitive paths (`.env`, `.git/config`, backup files, admin panels, etc.), using baseline-response comparison to avoid false positives on servers that return `200` for every path (custom error/catch-all pages).
- **`main.py`** — the CLI entry point. Takes a target URL, discovers and runs every plugin in `plugins/` against it, and prints a combined report.

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

No registration step, no editing `main.py` — just add the file:

1. Create `plugins/my_check.py`.
2. Define a class that inherits from `Module` and implements `run(self) -> dict`, returning:
   ```python
   {
       "target": self.target,
       "plugin": "my_check",
       "findings": [{"description": "...", "severity": "..."}],
   }
   ```
3. Run `main.py` — the new plugin is discovered and executed automatically.

## Roadmap

- Concurrent plugin execution
- JSON/CSV export of results
- Additional plugins (subdomain enumeration, TLS/certificate checks)
- Config file support (custom header/path lists, per-plugin settings)

## Disclaimer

For authorized security testing only. Only run this against targets you own or have explicit permission to test.