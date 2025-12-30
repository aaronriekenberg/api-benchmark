#!/usr/bin/env python3
"""
Generate bar graphs from benchmark results and create summary markdown.
Reads results/raw.md, generates PNG graphs, and creates results/latest.md
"""

import re
import sys
from pathlib import Path
from collections import defaultdict

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Parse the markdown table
def parse_markdown_table(raw_file):
    """Parse benchmark results from raw.md markdown table."""
    with open(raw_file, 'r') as f:
        content = f.read()
    
    # Find the benchmark table section
    lines = content.split('\n')
    
    # Find the header row (starts with "| Test Name |")
    header_idx = -1
    for i, line in enumerate(lines):
        if '| Test Name |' in line:
            header_idx = i
            break
    
    if header_idx == -1:
        print("ERROR: Could not find benchmark table header")
        sys.exit(1)
    
    # Skip header and separator lines
    data_start = header_idx + 2
    
    # Parse data rows - keep connection levels separate
    results = []
    
    for line in lines[data_start:]:
        if not line.startswith('|') or '---' in line:
            continue
        
        # Parse table row
        parts = [p.strip() for p in line.split('|')[1:-1]]
        
        if len(parts) < 11:
            continue
        
        test_name = parts[0].strip()
        http_conns = parts[1].strip()
        
        try:
            rps = float(parts[4].strip())
            p99 = float(parts[6].strip())
            memory = float(parts[8].strip())
            threads = int(parts[10].strip())
            
            results.append({
                'api': test_name,
                'conns': http_conns,
                'rps': rps,
                'p99': p99,
                'memory': memory,
                'threads': threads
            })
        except (ValueError, IndexError) as e:
            print(f"Warning: Could not parse row: {line}")
            continue
    
    return results


def generate_rps_graph(results, output_file):
    """Generate grouped bar graph for requests per second."""
    # Get unique APIs and connection levels
    apis = sorted(set(r['api'] for r in results))
    conns = sorted(set(r['conns'] for r in results))
    
    fig, ax = plt.subplots(figsize=(14, 6))
    
    x = range(len(apis))
    bar_width = 0.25
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
    
    # Create bars for each connection level
    for i, conn in enumerate(conns):
        rps_values = []
        for api in apis:
            # Find matching result
            matching = [r for r in results if r['api'] == api and r['conns'] == conn]
            if matching:
                rps_values.append(matching[0]['rps'])
            else:
                rps_values.append(0)
        
        offset = (i - len(conns) / 2 + 0.5) * bar_width
        bars = ax.bar([xi + offset for xi in x], rps_values, bar_width, 
                      label=f'{conn} connections', color=colors[i], 
                      edgecolor='black', linewidth=1)
        
        # Add value labels on bars
        for bar, value in zip(bars, rps_values):
            if value > 0:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                        f'{value:,.0f}',
                        ha='center', va='bottom', fontsize=8, fontweight='bold')
    
    ax.set_xlabel('API', fontsize=12, fontweight='bold')
    ax.set_ylabel('Requests Per Second', fontsize=12, fontweight='bold')
    ax.set_title('API Benchmark - Requests Per Second', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(apis, fontsize=11)
    ax.legend(fontsize=10, loc='upper left')
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated {output_file}")


def generate_memory_graph(results, output_file):
    """Generate grouped bar graph for API memory usage."""
    apis = sorted(set(r['api'] for r in results))
    conns = sorted(set(r['conns'] for r in results))

    fig, ax = plt.subplots(figsize=(14, 6))

    x = range(len(apis))
    bar_width = 0.25
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']

    for i, conn in enumerate(conns):
        memory_values = []
        for api in apis:
            matching = [r for r in results if r['api'] == api and r['conns'] == conn]
            if matching:
                memory_values.append(matching[0]['memory'])
            else:
                memory_values.append(0)

        offset = (i - len(conns) / 2 + 0.5) * bar_width
        bars = ax.bar([xi + offset for xi in x], memory_values, bar_width,
                      label=f'{conn} connections', color=colors[i],
                      edgecolor='black', linewidth=1)

        for bar, value in zip(bars, memory_values):
            if value > 0:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width() / 2., height,
                        f'{value:.1f}',
                        ha='center', va='bottom', fontsize=8, fontweight='bold')

    ax.set_xlabel('API', fontsize=12, fontweight='bold')
    ax.set_ylabel('Memory (MB)', fontsize=12, fontweight='bold')
    ax.set_title('API Benchmark - Memory Usage', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(apis, fontsize=11)
    ax.legend(fontsize=10, loc='upper left')
    ax.grid(axis='y', alpha=0.3, linestyle='--')

    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated {output_file}")



def generate_p99_graph(results, output_file):
    """Generate grouped bar graph for P99 response time (ms)."""
    apis = sorted(set(r['api'] for r in results))
    conns = sorted(set(r['conns'] for r in results))

    fig, ax = plt.subplots(figsize=(14, 6))

    x = range(len(apis))
    bar_width = 0.25
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']

    for i, conn in enumerate(conns):
        p99_values = []
        for api in apis:
            matching = [r for r in results if r['api'] == api and r['conns'] == conn]
            if matching:
                p99_values.append(matching[0]['p99'])
            else:
                p99_values.append(0)

        offset = (i - len(conns) / 2 + 0.5) * bar_width
        bars = ax.bar([xi + offset for xi in x], p99_values, bar_width,
                      label=f'{conn} connections', color=colors[i],
                      edgecolor='black', linewidth=1)

        for bar, value in zip(bars, p99_values):
            if value > 0:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width() / 2., height,
                        f'{value:.2f}',
                        ha='center', va='bottom', fontsize=8, fontweight='bold')

    ax.set_xlabel('API', fontsize=12, fontweight='bold')
    ax.set_ylabel('P99 (ms)', fontsize=12, fontweight='bold')
    ax.set_title('API Benchmark - P99 Response Time', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(apis, fontsize=11)
    ax.legend(fontsize=10, loc='upper left')
    ax.grid(axis='y', alpha=0.3, linestyle='--')

    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated {output_file}")


def generate_latest_md(results_dir='results'):
    """Generate latest.md with links to graph images."""
    latest_md = Path(results_dir) / 'latest.md'

    content = """# Latest Benchmark Results

## Performance Metrics

### Requests Per Second
![Requests Per Second](rps.png)

### API Memory Usage
![API Memory MB](memory.png)

### API Threads
![API Threads](threads.png)

### P99 Response Time
![P99 Response Time](p99.png)

---
*Graphs generated from benchmark results. See raw.md for detailed data.*
"""

    with open(latest_md, 'w') as f:
        f.write(content)

    print(f"Generated {latest_md}")
    


def generate_threads_graph(results, output_file):
    """Generate grouped bar graph for API thread count."""
    # Get unique APIs and connection levels
    apis = sorted(set(r['api'] for r in results))
    conns = sorted(set(r['conns'] for r in results))
    
    fig, ax = plt.subplots(figsize=(14, 6))
    
    x = range(len(apis))
    bar_width = 0.25
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
    
    # Create bars for each connection level
    for i, conn in enumerate(conns):
        threads_values = []
        for api in apis:
            # Find matching result
            matching = [r for r in results if r['api'] == api and r['conns'] == conn]
            if matching:
                threads_values.append(matching[0]['threads'])
            else:
                threads_values.append(0)
        
        offset = (i - len(conns) / 2 + 0.5) * bar_width
        bars = ax.bar([xi + offset for xi in x], threads_values, bar_width, 
                      label=f'{conn} connections', color=colors[i], 
                      edgecolor='black', linewidth=1)
        
        # Add value labels on bars
        for bar, value in zip(bars, threads_values):
            if value > 0:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                        f'{value:.0f}',
                        ha='center', va='bottom', fontsize=8, fontweight='bold')
    
    ax.set_xlabel('API', fontsize=12, fontweight='bold')
    ax.set_ylabel('Thread Count', fontsize=12, fontweight='bold')
    ax.set_title('API Benchmark - Thread Usage', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(apis, fontsize=11)
    ax.legend(fontsize=10, loc='upper left')
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated {output_file}")





def main():
    results_dir = Path('results')
    raw_file = results_dir / 'raw.md'
    
    if not raw_file.exists():
        print(f"ERROR: {raw_file} not found")
        sys.exit(1)
    
    print(f"Parsing {raw_file}...")
    results = parse_markdown_table(str(raw_file))
    
    if not results:
        print("ERROR: No benchmark data found in raw.md")
        sys.exit(1)
    
    print(f"Found {len(results)} benchmark results")
    apis = sorted(set(r['api'] for r in results))
    conns = sorted(set(r['conns'] for r in results))
    print(f"APIs: {apis}")
    print(f"Connection levels: {conns}")
    
    # Generate graphs
    print("\nGenerating graphs...")
    generate_rps_graph(results, str(results_dir / 'rps.png'))
    generate_memory_graph(results, str(results_dir / 'memory.png'))
    generate_threads_graph(results, str(results_dir / 'threads.png'))
    generate_p99_graph(results, str(results_dir / 'p99.png'))
    
    # Generate latest.md
    print("\nGenerating latest.md...")
    generate_latest_md(str(results_dir))
    
    print("\nDone!")


if __name__ == '__main__':
    main()
