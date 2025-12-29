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
    # Remove any existing mermaid blocks (we want the PNG only)
    try:
        remove_mermaid_blocks(md_path)
    except Exception:
        pass
    # Ensure latest.md contains an image link to the chart
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


def generate_mermaid_block(chosen_rows):
    # chosen_rows: list of dicts with 'Test Name' and 'Requests per Second'
    lines = []
    lines.append('```mermaid')
    lines.append("%%{init: {'theme': 'default'}}%%")
    # Use a `pie` chart for GitHub-renderable Mermaid fallback
    lines.append('pie')
    lines.append("    title Requests per second (concurrency ~800)")
    for r in sorted(chosen_rows, key=lambda x: x.get('Test Name')):
        name = r.get('Test Name')
        rps = r.get('Requests per Second', '0')
        # ensure numeric value
        try:
            val = float(rps.replace(',', ''))
            # format number reasonably
            if val.is_integer():
                val_s = str(int(val))
            else:
                val_s = str(round(val, 2))
        except Exception:
            val_s = rps
        # quote label to be safe
        safe_label = '"' + name.replace('"', '\\"') + '"'
        lines.append(f'    {safe_label} : {val_s}')
    lines.append('```')
    return '\n'.join(lines) + '\n'


def inject_mermaid(md_path: Path, chosen_rows):
    text = md_path.read_text(encoding='utf-8')
    block = generate_mermaid_block(chosen_rows)

    # If an existing mermaid block (generated by us) exists, replace it.
    if '```mermaid' in text:
        # naive replacement: replace first mermaid fenced block
        parts = text.split('```mermaid', 1)
        before = parts[0]
        rest = parts[1]
        # find end of that mermaid block
        if '```' in rest:
            after = rest.split('```', 1)[1]
        else:
            after = ''
        new_text = before + block + after
        md_path.write_text(new_text, encoding='utf-8')
        print('Replaced existing mermaid block in', md_path)
        return

    # Otherwise insert after the image link if present, else after title
    lines = text.splitlines()
    insert_at = None
    for i, l in enumerate(lines):
        if 'Benchmark chart' in l or l.strip().startswith('!['):
            insert_at = i + 1
            break
    if insert_at is None:
        for i, line in enumerate(lines):
            if line.strip().startswith('#'):
                insert_at = i + 1
                break
    if insert_at is None:
        insert_at = len(lines)

    lines.insert(insert_at, '')
    lines.insert(insert_at + 1, block.rstrip('\n'))
    md_path.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print('Inserted mermaid block into', md_path)


def remove_mermaid_blocks(md_path: Path):
    text = md_path.read_text(encoding='utf-8')
    if '```mermaid' not in text:
        return
    new_parts = []
    i = 0
    while i < len(text):
        idx = text.find('```mermaid', i)
        if idx == -1:
            new_parts.append(text[i:])
            break
        new_parts.append(text[i:idx])
        # find end of fenced block
        end = text.find('```', idx + len('```mermaid'))
        if end == -1:
            # no closing fence; drop rest
            break
        i = end + len('```')
    new_text = ''.join(new_parts)
    # Remove possible extra blank lines
    new_text = new_text.replace('\n\n\n', '\n\n')
    md_path.write_text(new_text.strip() + '\n', encoding='utf-8')
    print('Removed mermaid blocks from', md_path)


if __name__ == '__main__':
    md = Path('results/latest.md')
    out = Path('results/latest.png')
    raise SystemExit(generate_chart(md, out))
