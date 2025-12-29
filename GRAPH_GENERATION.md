# Benchmark Graph Generation Implementation

## Summary
Successfully added automated generation of PNG bar graphs from benchmark results to the GitHub Actions workflow.

## Files Created

### 1. generate-graphs.py
- Python script that parses `results/raw.md` markdown table
- Extracts benchmark metrics for each API (rust, go, kotlin, node, python)
- Generates 3 PNG bar graphs using matplotlib:
  - **results/rps.png** - Requests Per Second (average across connection levels)
  - **results/memory.png** - API Memory MB usage (average)
  - **results/threads.png** - API Thread count (average)
- Creates **results/latest.md** with links to the generated graphs

### 2. Updated .github/workflows/main.yml
Added 3 new workflow steps after the benchmark execution:

#### Step 1: Install matplotlib
```yaml
- name: Install matplotlib
  run: pip install matplotlib
```

#### Step 2: Generate benchmark graphs
```yaml
- name: Generate benchmark graphs
  run: python3 generate-graphs.py
```

#### Step 3: Commit and push results
```yaml
- name: Commit and push results
  run: |
    git config --global user.email "aaron.riekenberg@gmail.com"
    git config --global user.name "Aaron Riekenberg"
    git add results/rps.png results/memory.png results/threads.png results/latest.md
    if git diff --cached --quiet; then
      echo "No changes to commit"
    else
      git commit -m 'Add benchmark graphs and latest results'
      git push -v
    fi
```

## Generated Graphs

### Requests Per Second (rps.png)
- Bar chart showing average RPS for each API implementation
- Rust: ~110k RPS (fastest)
- Go: ~82k RPS
- Kotlin: ~65k RPS
- Node: ~27k RPS
- Python: ~7k RPS (slowest)

### API Memory (memory.png)
- Bar chart showing average memory usage for each API
- Kotlin: ~559 MB (highest)
- Node: ~132 MB
- Go: ~27 MB
- Python: ~38 MB
- Rust: ~14 MB (lowest)

### API Threads (threads.png)
- Bar chart showing average thread count for each API
- Kotlin: 30 threads (highest)
- Go: 11 threads
- Rust: 5 threads
- Node: 7 threads
- Python: 1 thread (lowest)

## Generated Summary File

### results/latest.md
Contains markdown links to all three PNG graphs for easy viewing and documentation.

## Workflow Execution

When the benchmark action runs:
1. Executes all benchmarks → produces `results/raw.md`
2. Installs matplotlib dependency
3. Runs `generate-graphs.py` to parse data and generate graphs
4. Commits and pushes all `.png` files and `latest.md` to the repository

The commit will only occur if there are changes to commit, preventing empty commits.

## Testing

Script has been tested locally and successfully:
- ✅ Parsed benchmark data from results/raw.md
- ✅ Generated all 3 PNG graphs
- ✅ Created results/latest.md with proper markdown links
- ✅ All files are properly formatted and ready for GitHub commit
