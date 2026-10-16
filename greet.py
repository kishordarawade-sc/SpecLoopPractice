import argparse


def build_greeting(name: str | None) -> str:
    raise NotImplementedError


def main() -> None:
    parser = argparse.ArgumentParser(description="Print a friendly greeting.")
    parser.add_argument("name", nargs="?", default=None, help="name to greet")
    args = parser.parse_args()
    print(build_greeting(args.name))


if __name__ == "__main__":
    main()
