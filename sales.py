"""
Read a CSV with 'date' and 'amount' columns and plot monthly sales sums as a bar chart.

CSV format (header expected):
date,amount
2025-01-03,100.5
2025-01-15,200
...

Usage examples:
  python sales.py --file sales.csv          # read sales.csv and show plot
  python sales.py --file sales.csv --out monthly.png   # save plot to monthly.png
  python sales.py --sample --out demo.png  # use generated sample data and save plot
"""
import sys
import argparse
import csv
from collections import defaultdict, OrderedDict
from datetime import datetime
import matplotlib.pyplot as plt

DATE_FORMATS = ("%Y-%m-%d", "%Y/%m/%d", "%Y%m%d")


def parse_date(s):
    s = s.strip()
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    # try ISO fallback (Python 3.7+)
    try:
        return datetime.fromisoformat(s).date()
    except Exception:
        raise ValueError(f"unrecognized date format: {s}")


def read_sales_csv(path):
    """Read CSV file and return list of (date, amount). Raises exceptions on errors."""
    rows = []
    try:
        with open(path, newline="", encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            if "date" not in reader.fieldnames or "amount" not in reader.fieldnames:
                raise ValueError("CSV must contain 'date' and 'amount' columns")
            for i, row in enumerate(reader, start=2):  # header is line 1
                raw_date = row.get("date", "").strip()
                raw_amount = row.get("amount", "").strip()
                if not raw_date or not raw_amount:
                    raise ValueError(f"missing data on line {i}")
                try:
                    d = parse_date(raw_date)
                except ValueError as e:
                    raise ValueError(f"line {i}: {e}")
                try:
                    amt = float(raw_amount)
                except ValueError:
                    raise ValueError(f"line {i}: invalid amount: {raw_amount}")
                rows.append((d, amt))
    except FileNotFoundError:
        raise
    return rows


def generate_sample_data():
    """Return sample list of (date, amount) for a few months."""
    sample = []
    base = datetime(2025, 1, 1).date()
    import random

    for month in range(1, 7):  # Jan..Jun
        for day in (5, 10, 15, 20):
            sample.append(
                (datetime(2025, month, day).date(), round(random.uniform(50, 500), 2))
            )
    return sample


def aggregate_by_month(rows):
    """Aggregate list of (date, amount) into OrderedDict[YYYY-MM] = sum"""
    sums = defaultdict(float)
    for d, amt in rows:
        key = f"{d.year:04d}-{d.month:02d}"
        sums[key] += amt
    # sort keys chronologically
    ordered = OrderedDict(sorted(sums.items(), key=lambda kv: kv[0]))
    return ordered


def plot_monthly_sums(month_sums, title="Monthly Sales", out_path=None):
    if not month_sums:
        raise ValueError("no data to plot")
    months = list(month_sums.keys())
    values = list(month_sums.values())

    plt.figure(figsize=(max(6, len(months) * 0.8), 4.5))
    bars = plt.bar(months, values, color="tab:blue")
    plt.xlabel("Month")
    plt.ylabel("Sales (sum)")
    plt.title(title)
    plt.xticks(rotation=45, ha="right")
    # annotate bars with values
    for b, v in zip(bars, values):
        plt.text(
            b.get_x() + b.get_width() / 2,
            v,
            f"{v:.2f}",
            ha="center",
            va="bottom",
            fontsize=8,
        )
    plt.tight_layout()

    if out_path:
        plt.savefig(out_path)
        print(f"Saved plot to {out_path}")
    else:
        plt.show()


def main(argv=None):
    parser = argparse.ArgumentParser(description="Plot monthly sales sums from a CSV file.")
    parser.add_argument(
        "--file", "-f", help="Path to CSV file with 'date' and 'amount' columns."
    )
    parser.add_argument(
        "--out", "-o", help="If given, save plot to this image file instead of showing."
    )
    parser.add_argument(
        "--sample",
        action="store_true",
        help="Use generated sample data instead of reading CSV.",
    )
    args = parser.parse_args(argv)

    try:
        if args.sample:
            rows = generate_sample_data()
        elif args.file:
            rows = read_sales_csv(args.file)
        else:
            # no file and not sample: suggest usage and exit
            print(
                "Provide --file PATH to read CSV or use --sample to generate demo data. See -h for details.",
                file=sys.stderr,
            )
            return 2

        if not rows:
            print("No sales records found.", file=sys.stderr)
            return 3

        month_sums = aggregate_by_month(rows)
        plot_monthly_sums(month_sums, title="Monthly Sales Sum", out_path=args.out)
    except FileNotFoundError:
        print(f"Error: file not found: {args.file}", file=sys.stderr)
        return 4
    except ValueError as ve:
        print(f"Error: {ve}", file=sys.stderr)
        return 5
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 10

    return 0


if __name__ == "__main__":
    sys.exit(main())