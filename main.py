import sys
from plugin_discovery import plugin_discovery


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

    plugin_classes = plugin_discovery("plugins")

    print(f"Scanning {target} ...")

    for plugin_cls in plugin_classes:
        instance = plugin_cls(target)
        result = instance.execute()
        print_report(result)


if __name__ == "__main__":
    main()
