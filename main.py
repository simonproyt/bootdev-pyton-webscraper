import sys


def main() -> int:
    args = sys.argv
    if len(args) < 2:
        print("no website provided")
        return 1
    if len(args) > 2:
        print("too many arguments provided")
        return 1

    base_url = args[1]
    print(f"starting crawl of: {base_url}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
