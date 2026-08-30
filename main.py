import sys
from header_audit import HeaderAudit
from sensitive_file_check import SensitiveFileCheck


def print_report(result):
    if not result:
        return
    print(f"\n[{result['plugin']}] target: {result['target']}")
    if not result["findings"]:
        print("  No issues found.")
    else:
        for finding in result["findings"]:
            print(f"  [{finding['severity'].upper()}] {finding['description']}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <target_url>")
        sys.exit(1)

    target = sys.argv[1]

    plugins = [
        HeaderAudit(target, timeout=10),
        SensitiveFileCheck(target, timeout=10),
    ]

    print(f"Scanning {target} ...")

    for plugin in plugins:
        result = plugin.execute()
        print_report(result)


if __name__ == "__main__":
    main()
