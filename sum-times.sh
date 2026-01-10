#!/bin/bash

# Sum CPU times in HH:MM:SS format
# Usage: ./sum-times.sh HH:MM:SS [HH:MM:SS ...]
# Example: ./sum-times.sh 00:01:30 00:02:15

total_seconds=0

for time_str in "$@"; do
    # Parse HH:MM:SS format
    hours=$(echo "$time_str" | cut -d: -f1)
    minutes=$(echo "$time_str" | cut -d: -f2)
    seconds=$(echo "$time_str" | cut -d: -f3)
    
    # Remove leading zeros to prevent octal interpretation
    hours=$((10#$hours))
    minutes=$((10#$minutes))
    seconds=$((10#$seconds))

    # Convert to total seconds
    time_seconds=$((hours * 3600 + minutes * 60 + seconds))
    total_seconds=$((total_seconds + time_seconds))
done

# Convert back to HH:MM:SS
result_hours=$((total_seconds / 3600))
result_minutes=$(((total_seconds % 3600) / 60))
result_seconds=$((total_seconds % 60))

# Format with leading zeros
printf "%02d:%02d:%02d\n" "$result_hours" "$result_minutes" "$result_seconds"
