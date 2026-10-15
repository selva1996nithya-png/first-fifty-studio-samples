"""Trim CSV fields and remove exact duplicate rows without changing field case."""
import argparse
import csv
import io
from pathlib import Path


def clean(text):
    rows = csv.reader(io.StringIO(text.lstrip('\ufeff'), newline=''))
    try:
        header = [cell.strip() for cell in next(rows)]
    except StopIteration:
        raise ValueError('CSV is empty') from None
    if not header or any(not cell for cell in header):
        raise ValueError('Headers must be nonempty')
    if len(set(header)) != len(header):
        raise ValueError('Headers collide after trimming')
    out = io.StringIO(newline='')
    writer = csv.writer(out)
    writer.writerow(header)
    seen = set()
    kept = duplicates = blanks = 0
    for number, row in enumerate(rows, 2):
        if not row or all(not cell.strip() for cell in row):
            blanks += 1
            continue
        if len(row) != len(header):
            raise ValueError(f'Row {number} has {len(row)} fields; expected {len(header)}')
        row = tuple(cell.strip() for cell in row)
        if row in seen:
            duplicates += 1
            continue
        seen.add(row)
        writer.writerow(row)
        kept += 1
    return out.getvalue(), dict(kept=kept, duplicates=duplicates, blanks=blanks)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    result, report = clean(args.input.read_text(encoding='utf-8'))
    with args.output.open('x', encoding='utf-8', newline='') as dest:
        dest.write(result)
    print(report)
