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
            success_rate = float(parts[2].strip().rstrip('%'))
            test_seconds = float(parts[3].strip())
            rps = float(parts[4].strip())
            p99 = float(parts[6].strip())
            memory = float(parts[8].strip())
            # Parse CPU Time (MM:SS format to seconds)
            cpu_time_str = parts[9].strip()
            if ':' in cpu_time_str:
                time_parts = cpu_time_str.split(':')
                if len(time_parts) == 2:
                    m, s = time_parts
                    cpu_seconds = int(m) * 60 + float(s)
                elif len(time_parts) == 3:
                    h, m, s = time_parts
                    cpu_seconds = int(h) * 3600 + int(m) * 60 + float(s)
                else:
                    cpu_seconds = 0
            else:
                cpu_seconds = float(cpu_time_str) if cpu_time_str else 0
            threads = int(parts[10].strip())
            processes = int(parts[11].strip()) if len(parts) > 11 else 1
            
            results.append({
                'api': test_name,
                'conns': http_conns,
                'success_rate': success_rate,
                'test_seconds': test_seconds,
                'rps': rps,
                'p99': p99,
                'memory': memory,
                'cpu_seconds': cpu_seconds,
                'threads': threads,
                'processes': processes
            })
        except (ValueError, IndexError) as e:
            print(f"Warning: Could not parse row: {line}")
            continue
    
    return results


def generate_rps_graph(results, output_file):
    """Generate grouped bar graph for requests per second."""
    # Get unique APIs preserving order from results, and connection levels
    apis = []
    seen = set()
    for r in results:
        if r['api'] not in seen:
            apis.append(r['api'])
            seen.add(r['api'])
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
    ax.legend(fontsize=10, loc='upper right')
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated {output_file}")


def generate_test_seconds_graph(results, output_file):
    """Generate grouped bar graph for test seconds."""
    # Get unique APIs preserving order from results, and connection levels
    apis = []
    seen = set()
    for r in results:
        if r['api'] not in seen:
            apis.append(r['api'])
            seen.add(r['api'])
    conns = sorted(set(r['conns'] for r in results))
    
    fig, ax = plt.subplots(figsize=(14, 6))
    
    x = range(len(apis))
    bar_width = 0.25
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
    
    # Create bars for each connection level
    for i, conn in enumerate(conns):
        test_values = []
        for api in apis:
            matching = [r for r in results if r['api'] == api and r['conns'] == conn]
            if matching:
                test_values.append(matching[0]['test_seconds'])
            else:
                test_values.append(0)
        
        offset = (i - len(conns) / 2 + 0.5) * bar_width
        bars = ax.bar([xi + offset for xi in x], test_values, bar_width, 
                      label=f'{conn} connections', color=colors[i], 
                      edgecolor='black', linewidth=1)
        
        # Add value labels on bars
        for bar, value in zip(bars, test_values):
            if value > 0:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                        f'{value:.1f}',
                        ha='center', va='bottom', fontsize=8, fontweight='bold')
    
    ax.set_xlabel('API', fontsize=12, fontweight='bold')
    ax.set_ylabel('Test Seconds', fontsize=12, fontweight='bold')
    ax.set_title('API Benchmark - Test Duration', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(apis, fontsize=11)
    ax.legend(fontsize=10, loc='upper left')
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated {output_file}")


def generate_success_rate_graph(results, output_file):
    """Generate grouped bar graph for success rate (%)."""
    # Get unique APIs preserving order from results, and connection levels
    apis = []
    seen = set()
    for r in results:
        if r['api'] not in seen:
            apis.append(r['api'])
            seen.add(r['api'])
    conns = sorted(set(r['conns'] for r in results))
    
    fig, ax = plt.subplots(figsize=(14, 6))
    
    x = range(len(apis))
    bar_width = 0.25
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
    
    # Create bars for each connection level
    for i, conn in enumerate(conns):
        success_values = []
        for api in apis:
            matching = [r for r in results if r['api'] == api and r['conns'] == conn]
            if matching:
                success_values.append(matching[0]['success_rate'])
            else:
                success_values.append(0)
        
        offset = (i - len(conns) / 2 + 0.5) * bar_width
        bars = ax.bar([xi + offset for xi in x], success_values, bar_width, 
                      label=f'{conn} connections', color=colors[i], 
                      edgecolor='black', linewidth=1)
        
        # Add value labels on bars
        for bar, value in zip(bars, success_values):
            if value > 0:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                        f'{value:.1f}%',
                        ha='center', va='bottom', fontsize=8, fontweight='bold')
    
    ax.set_xlabel('API', fontsize=12, fontweight='bold')
    ax.set_ylabel('Success Rate (%)', fontsize=12, fontweight='bold')
    ax.set_title('API Benchmark - Success Rate', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(apis, fontsize=11)
    ax.set_ylim(bottom=95, top=100.5)
    ax.legend(fontsize=10, loc='lower right')
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated {output_file}")


def generate_memory_graph(results, output_file):
    """Generate grouped bar graph for API memory usage."""
    # Get unique APIs preserving order from results, and connection levels
    apis = []
    seen = set()
    for r in results:
        if r['api'] not in seen:
            apis.append(r['api'])
            seen.add(r['api'])
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


def generate_cpu_time_graph(results, output_file):
    """Generate grouped bar graph for API CPU time."""
    # Get unique APIs preserving order from results, and connection levels
    apis = []
    seen = set()
    for r in results:
        if r['api'] not in seen:
            apis.append(r['api'])
            seen.add(r['api'])
    conns = sorted(set(r['conns'] for r in results))

    fig, ax = plt.subplots(figsize=(14, 6))

    x = range(len(apis))
    bar_width = 0.25
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']

    for i, conn in enumerate(conns):
        cpu_values = []
        for api in apis:
            matching = [r for r in results if r['api'] == api and r['conns'] == conn]
            if matching:
                cpu_values.append(matching[0]['cpu_seconds'])
            else:
                cpu_values.append(0)

        offset = (i - len(conns) / 2 + 0.5) * bar_width
        bars = ax.bar([xi + offset for xi in x], cpu_values, bar_width,
                      label=f'{conn} connections', color=colors[i],
                      edgecolor='black', linewidth=1)

        for bar, value in zip(bars, cpu_values):
            if value > 0:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width() / 2., height,
                        f'{value:.0f}',
                        ha='center', va='bottom', fontsize=8, fontweight='bold')

    ax.set_xlabel('API', fontsize=12, fontweight='bold')
    ax.set_ylabel('CPU Time (seconds)', fontsize=12, fontweight='bold')
    ax.set_title('API Benchmark - CPU Time', fontsize=14, fontweight='bold')
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
    # Get unique APIs preserving order from results, and connection levels
    apis = []
    seen = set()
    for r in results:
        if r['api'] not in seen:
            apis.append(r['api'])
            seen.add(r['api'])
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
    """Generate latest.md with links to graph images and copy timestamp from raw.md."""
    latest_md = Path(results_dir) / 'latest.md'

    # read timestamp from raw.md (next non-empty line after '## Timestamp')
    raw_md = Path(results_dir) / 'raw.md'
    timestamp_line = None
    if raw_md.exists():
        try:
            with open(raw_md, 'r') as rf:
                lines = [l.rstrip('\n') for l in rf]
            for i, line in enumerate(lines):
                if line.strip().lower().startswith('## timestamp'):
                    j = i + 1
                    while j < len(lines) and lines[j].strip() == '':
                        j += 1
                    if j < len(lines):
                        timestamp_line = lines[j].strip()
                    break
        except Exception:
            timestamp_line = None

    ts_block = f"Timestamp: `{timestamp_line}`\n\n" if timestamp_line else ""

    content = f"""# Latest Results
\n{ts_block}## Requests Per Second
![Requests Per Second](rps.png)
\n## Test Duration
![Test Duration](test_seconds.png)
\n## API Memory Usage
![API Memory MB](memory.png)
\n## API CPU Time
![API CPU Time](cpu_time.png)
\n## P99 Response Time
![P99 Response Time](p99.png)
\n## API Threads
![API Threads](threads.png)
\n## API Processes
![API Processes](api_processes.png)
\n## Success Rate
![Success Rate](success_rate.png)
\n---
*Graphs generated from benchmark results. See raw.md for detailed data.*
"""

    with open(latest_md, 'w') as f:
        f.write(content)

    print(f"Generated {latest_md}")
    


def generate_threads_graph(results, output_file):
    """Generate grouped bar graph for API thread count."""
    # Get unique APIs preserving order from results, and connection levels
    apis = []
    seen = set()
    for r in results:
        if r['api'] not in seen:
            apis.append(r['api'])
            seen.add(r['api'])
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


def generate_api_processes_graph(results, output_file):
    """Generate grouped bar graph for API process count."""
    # Get unique APIs preserving order from results, and connection levels
    apis = []
    seen = set()
    for r in results:
        if r['api'] not in seen:
            apis.append(r['api'])
            seen.add(r['api'])
    conns = sorted(set(r['conns'] for r in results))
    
    fig, ax = plt.subplots(figsize=(14, 6))
    
    x = range(len(apis))
    bar_width = 0.25
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
    
    # Create bars for each connection level
    for i, conn in enumerate(conns):
        processes_values = []
        for api in apis:
            matching = [r for r in results if r['api'] == api and r['conns'] == conn]
            if matching:
                processes_values.append(matching[0]['processes'])
            else:
                processes_values.append(0)
        
        offset = (i - len(conns) / 2 + 0.5) * bar_width
        bars = ax.bar([xi + offset for xi in x], processes_values, bar_width, 
                      label=f'{conn} connections', color=colors[i], 
                      edgecolor='black', linewidth=1)
        
        # Add value labels on bars
        for bar, value in zip(bars, processes_values):
            if value > 0:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                        f'{value:.0f}',
                        ha='center', va='bottom', fontsize=8, fontweight='bold')
    
    ax.set_xlabel('API', fontsize=12, fontweight='bold')
    ax.set_ylabel('Process Count', fontsize=12, fontweight='bold')
    ax.set_title('API Benchmark - Process Usage', fontsize=14, fontweight='bold')
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
    generate_test_seconds_graph(results, str(results_dir / 'test_seconds.png'))
    generate_success_rate_graph(results, str(results_dir / 'success_rate.png'))
    generate_memory_graph(results, str(results_dir / 'memory.png'))
    generate_cpu_time_graph(results, str(results_dir / 'cpu_time.png'))
    generate_threads_graph(results, str(results_dir / 'threads.png'))
    generate_api_processes_graph(results, str(results_dir / 'api_processes.png'))
    generate_p99_graph(results, str(results_dir / 'p99.png'))
    
    # Generate latest.md
    print("\nGenerating latest.md...")
    generate_latest_md(str(results_dir))
    
    print("\nDone!")


if __name__ == '__main__':
    main()
