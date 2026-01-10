#!/bin/bash

set -e

echo "OUTPUT_FILE=$OUTPUT_FILE"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"

echo "begin commit-results.sh OUTPUT_FILE=$OUTPUT_FILE"
echo "cat $OUTPUT_FILE"
cat $OUTPUT_FILE

echo "ls -latrh results/"
ls -latrh results/

echo "final git commands"

git config --global user.email "aaron.riekenberg@gmail.com"
git config --global user.name "Aaron Riekenberg"

git add results/*

git status
git commit -m 'results from github actions autocommit'
git push -v