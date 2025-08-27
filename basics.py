"""
Compute mean and maximum from a list of numbers supplied via standard input
or as command-line arguments.

Usage examples:
  echo "1 2 3 4.5" | python basics.py
  python basics.py 1 2 3 4.5
  python basics.py           # when run interactively you'll be prompted

The script accepts numbers separated by whitespace or commas.
"""
import sys
import argparse
from statistics import mean

def parse_tokens(tokens):
    """Convert an iterable of string tokens to floats. Raises ValueError on bad token."""
    nums = []
    for t in tokens:
        t = t.strip()
        if not t:
            continue
        # allow commas inside numbers lists like "1,2,3"
        parts = t.replace(',', ' ').split()
        for p in parts:
            try:
                nums.append(float(p))
            except ValueError as e:
                raise ValueError(f"invalid number: {p}") from e
    return nums

def read_stdin_all():
    """Read all of stdin and return as a string (or empty string)."""
    try:
        return sys.stdin.read()
    except Exception:
        return ''

def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="basics.py",
        description="Read numbers from stdin or arguments and print mean and max."
    )
    parser.add_argument('numbers', nargs='*', help='Numbers (optional). If omitted, read from stdin.')
    args = parser.parse_args(argv)

    tokens = []
    if args.numbers:
        tokens = args.numbers
    else:
        # If stdin is a TTY, prompt the user briefly; otherwise read piped input
        if sys.stdin.isatty():
            try:
                user = input("Enter numbers separated by spaces or commas (empty to abort): ").strip()
            except EOFError:
                user = ''
            if not user:
                print("No input provided. See -h for usage.", file=sys.stderr)
                return 2
            tokens = [user]
        else:
            data = read_stdin_all()
            if not data:
                print("No input (stdin empty). See -h for usage.", file=sys.stderr)
                return 2
            tokens = [data]

    try:
        numbers = parse_tokens(tokens)
    except ValueError as err:
        print(f"Error: {err}", file=sys.stderr)
        return 3

    if not numbers:
        print("Error: no valid numbers found.", file=sys.stderr)
        return 4

    # compute metrics
    try:
        avg = mean(numbers)
        maximum = max(numbers)
    except Exception as err:
        print(f"Computation error: {err}", file=sys.stderr)
        return 5

    # output results
    print(f"count: {len(numbers)}")
    print(f"mean: {avg}")
    print(f"max: {maximum}")
    return 0

if __name__ == "__main__":
    sys.exit(main())