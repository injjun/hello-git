import csv
import argparse
from collections import defaultdict, OrderedDict
from datetime import datetime
import sys
import os

try:
    import matplotlib.pyplot as plt
except Exception:
    plt = None  # plotting optional


COMMON_DATE_FORMATS = [
    "%Y-%m-%d", "%Y/%m/%d", "%d-%m-%Y", "%m/%d/%Y", "%Y-%m", "%Y%m%d",
]


def parse_date(s: str):
    s = s.strip()
    for fmt in COMMON_DATE_FORMATS:
        try:
            return datetime.strptime(s, fmt)
        except Exception:
            continue
    # 마지막 시도: ISO8601 parse via fromisoformat (python3.7+)
    try:
        return datetime.fromisoformat(s)
    except Exception:
        raise ValueError(f"Unknown date format: {s}")


def parse_amount(s: str):
    s = s.strip().replace(",", "").replace(" ", "")
    # remove common currency symbols
    for ch in "$€₩￦£¥":
        s = s.replace(ch, "")
    if s == "":
        return 0.0
    return float(s)


def read_sales(path: str):
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    monthly = defaultdict(float)
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        # peek header row
        try:
            first = next(reader)
        except StopIteration:
            return monthly
        # detect header: if any non-numeric cell in first row -> header
        has_header = any(not cell.replace(",", "").replace(".", "").strip().lstrip("+-").isdigit() for cell in first)
        if has_header:
            # use DictReader to get fieldnames
            f.seek(0)
            dreader = csv.DictReader(f)
            fieldnames = [n.lower() for n in dreader.fieldnames or []]
            # find date and amount columns
            date_keys = [k for k in fieldnames if any(x in k for x in ("date", "day", "time"))]
            amt_keys = [k for k in fieldnames if any(x in k for x in ("amount", "sales", "revenue", "value", "price", "total"))]
            date_key = date_keys[0] if date_keys else dreader.fieldnames[0]
            amt_key = amt_keys[0] if amt_keys else (dreader.fieldnames[1] if len(dreader.fieldnames) > 1 else dreader.fieldnames[0])
            for row in dreader:
                raw_date = row.get(date_key, "").strip()
                raw_amt = row.get(amt_key, "").strip()
                if not raw_date:
                    continue
                try:
                    dt = parse_date(raw_date)
                except Exception:
                    # skip bad date
                    continue
                try:
                    amt = parse_amount(raw_amt)
                except Exception:
                    amt = 0.0
                key = f"{dt.year:04d}-{dt.month:02d}"
                monthly[key] += amt
        else:
            # no header: assume two columns date, amount
            # first row is data, process it and the rest
            rows = [first] + list(reader)
            for row in rows:
                if len(row) < 1:
                    continue
                raw_date = row[0]
                raw_amt = row[1] if len(row) > 1 else "0"
                try:
                    dt = parse_date(raw_date)
                except Exception:
                    continue
                try:
                    amt = parse_amount(raw_amt)
                except Exception:
                    amt = 0.0
                key = f"{dt.year:04d}-{dt.month:02d}"
                monthly[key] += amt
    # return OrderedDict sorted by key (chronological)
    return OrderedDict(sorted(monthly.items()))


def print_monthly(monthly):
    if not monthly:
        print("데이터가 없습니다.")
        return
    print("월별 매출 합계:")
    for k, v in monthly.items():
        print(f"{k}: {v:.2f}")


def plot_monthly(monthly, save_path=None):
    if plt is None:
        print("matplotlib이 설치되어 있지 않아 그래프를 그릴 수 없습니다.", file=sys.stderr)
        return
    months = list(monthly.keys())
    values = [monthly[m] for m in months]
    fig, ax = plt.subplots(figsize=(max(6, len(months) * 0.6), 4))
    ax.bar(months, values, color="tab:blue")
    ax.set_xlabel("월 (YYYY-MM)")
    ax.set_ylabel("매출 합계")
    ax.set_title("월별 매출 합계")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    if save_path:
        fig.savefig(save_path)
        print(f"그래프를 {save_path}에 저장했습니다.")
    else:
        plt.show()


def generate_sample_csv(path: str, months: int = 6, rows_per_month: int = 4):
    """Generate a sample CSV with 'date,amount' covering the last `months` months."""
    import random
    from datetime import date
    # compute year-month pairs for recent months
    today = date.today()
    year = today.year
    month = today.month
    ym = []
    for i in range(months - 1, -1, -1):
        m = month - i
        y = year
        while m <= 0:
            m += 12
            y -= 1
        ym.append((y, m))
    # create rows: multiple days per month
    rows = []
    for y, m in ym:
        for d in (5, 10, 15, 20)[:rows_per_month]:
            dt = f"{y:04d}-{m:02d}-{d:02d}"
            amt = round(random.uniform(50, 1000), 2)
            rows.append((dt, amt))
    # write CSV
    try:
        with open(path, "w", newline="", encoding="utf-8") as fh:
            fh.write("date,amount\n")
            for dt, amt in rows:
                fh.write(f"{dt},{amt}\n")
    except Exception as e:
        raise


def main():
    p = argparse.ArgumentParser(description="sales.csv를 읽어 월별 매출 합계를 출력합니다.")
    p.add_argument("--file", "-f", default="sales.csv", help="읽을 CSV 파일 경로 (기본: sales.csv)")
    p.add_argument("--plot", action="store_true", help="그래프를 표시합니다 (matplotlib 필요)")
    p.add_argument("--save", "-s", help="그래프 이미지를 저장할 파일 경로 (예: out.png)")
    p.add_argument("--sample", action="store_true", help="CSV 파일이 없거나 --sample을 지정하면 샘플 파일을 생성합니다.")
    args = p.parse_args()

    # if sample requested or file missing -> create sample CSV and continue
    if args.sample:
        print(f"샘플 CSV를 생성합니다: {args.file}", file=sys.stderr)
        try:
            generate_sample_csv(args.file)
        except Exception as e:
            print(f"샘플 생성 실패: {e}", file=sys.stderr)
            sys.exit(2)
    elif not os.path.exists(args.file):
        print(f"파일을 찾을 수 없습니다: {args.file}\n샘플 CSV를 생성합니다.", file=sys.stderr)
        try:
            generate_sample_csv(args.file)
        except Exception as e:
            print(f"샘플 생성 실패: {e}", file=sys.stderr)
            sys.exit(2)

    try:
        monthly = read_sales(args.file)
    except FileNotFoundError:
        print(f"파일을 찾을 수 없습니다: {args.file}", file=sys.stderr)
        sys.exit(2)

    print_monthly(monthly)

    if args.plot or args.save:
        plot_monthly(monthly, save_path=args.save)


if __name__ == "__main__":
    main()