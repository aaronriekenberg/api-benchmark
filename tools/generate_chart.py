#!/usr/bin/env python3
import re
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def parse_md_table(md_lines):
    # find header row for the benchmarks table
    header_idx = None
    for i, line in enumerate(md_lines):
        if line.startswith('|') and 'Test Name' in line and 'Requests per Second' in line:
            header_idx = i
            break
    if header_idx is None:
        return []

    header_line = md_lines[header_idx]
    headers = [h.strip() for h in header_line.strip().split('|')[1:-1]]

    rows = []
    for line in md_lines[header_idx+2:]:
        if not line.startswith('|') or set(line.strip()) == {'|', '-'}:
            break
        parts = [p.strip() for p in line.strip().split('|')[1:-1]]
        if len(parts) != len(headers):
            continue
        row = dict(zip(headers, parts))
        rows.append(row)
    return rows


def pick_rows_for_plot(rows, target_conns=800):
    # For each Test Name choose row with target_conns if available, else max conns
    groups = {}
    for r in rows:
        name = r.get('Test Name')
        try:
            conns = int(r.get('HTTP Conns', '0'))
        except ValueError:
            conns = 0
        groups.setdefault(name, []).append((conns, r))

    chosen = []
    for name, lst in groups.items():
        exact = [t for t in lst if t[0] == target_conns]
        if exact:
            chosen.append(exact[0][1])
        else:
            # pick row with max conns
            chosen.append(max(lst, key=lambda x: x[0])[1])
    return chosen


def to_float(s):
    try:
        return float(s.replace(',', ''))
    except Exception:
        return None


def generate_chart(md_path: Path, out_path: Path):
    md_lines = md_path.read_text(encoding='utf-8').splitlines()
    rows = parse_md_table(md_lines)
    if not rows:
        print('No benchmark table found in', md_path)
        return 1

    chosen = pick_rows_for_plot(rows, target_conns=800)

    # Extract labels and RPS
    labels = []
    values = []
    for r in sorted(chosen, key=lambda x: x.get('Test Name')):
        name = r.get('Test Name')
        rps = to_float(r.get('Requests per Second', '0'))
        if name and rps is not None:
            labels.append(name)
            values.append(rps)

    if not labels:
        print('No data to plot')
        return 1

    plt.figure(figsize=(8, 4))
    bars = plt.bar(labels, values, color=['#2b8cbe', '#7b3294', '#66c2a5', '#fdae61', '#ef3b2c'])
    plt.ylabel('Requests per second')
    plt.title('Benchmark: Requests per second (concurrency ~800)')
    plt.grid(axis='y', linestyle='--', alpha=0.4)

    # Label bars
    for bar in bars:
        h = bar.get_height()
        plt.annotate(f'{h:,.0f}', xy=(bar.get_x() + bar.get_width() / 2, h),
                     xytext=(0, 4), textcoords='offset points', ha='center', va='bottom', fontsize=8)

    plt.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, dpi=150)
    print('Wrote chart to', out_path)
    # Also ensure latest.md contains an image link to the chart
    inject_image_link(md_path, out_path)
    return 0


def inject_image_link(md_path: Path, out_path: Path):
    text = md_path.read_text(encoding='utf-8')
    img_rel = str(out_path.as_posix())
    img_md = f'![Benchmark chart]({img_rel})'

    lines = text.splitlines()
    # Insert after the first title line (# Results)
    for i, line in enumerate(lines):
        if line.strip().startswith('#'):
            insert_at = i + 1
            break
    else:
        insert_at = 0

    # If chart link already exists, replace it
    if any('Benchmark chart' in l for l in lines):
        new = []
        for l in lines:
            if 'Benchmark chart' in l:
                new.append(img_md)
            else:
                new.append(l)
        md_path.write_text('\n'.join(new) + '\n', encoding='utf-8')
        print('Updated image link in', md_path)
        return

    lines.insert(insert_at, '')
    lines.insert(insert_at + 1, img_md)
    md_path.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print('Inserted image link into', md_path)


if __name__ == '__main__':
    md = Path('results/latest.md')
    out = Path('results/latest.png')
    raise SystemExit(generate_chart(md, out))
