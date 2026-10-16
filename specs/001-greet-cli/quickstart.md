# Quickstart: Greet CLI

## Prerequisites

- Python 3.11+ on PATH
- `pytest` installed (`pip install pytest`)

## Run it

```powershell
python greet.py Alice
# Hello, Alice!

python greet.py
# Hello, World!
```

## Validate it

```powershell
pytest tests/test_greet.py -v
```

Expected: all tests pass, covering the scenarios in
[contracts/cli-contract.md](./contracts/cli-contract.md).
