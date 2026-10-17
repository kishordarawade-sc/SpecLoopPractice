import argparse


def build_greeting(name: str | None) -> str:
    cleaned = (name or "").strip()
    if not cleaned:
        return "Hello, World!"
    return f"Hello, {cleaned}!" 
    


def main() -> None:
    parser = argparse.ArgumentParser(description="Print a friendly greeting.")
    parser.add_argument("name", nargs="?", default=None, help="name to greet")
    args = parser.parse_args()
    print(build_greeting(args.name))


if __name__ == "__main__":
    main()
