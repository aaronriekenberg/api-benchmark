#!/bin/bash

set -e

echo "OUTPUT_FILE=$OUTPUT_FILE"

echo "begin commit-results.sh OUTPUT_FILE=$OUTPUT_FILE"
echo "cat $OUTPUT_FILE"
cat $OUTPUT_FILE

echo "final git commands"

git config --global user.email "aaron.riekenberg@gmail.com"
git config --global user.name "Aaron Riekenberg"

git add $OUTPUT_FILE
git status
git commit -m 'results from github actions autocommit'
git push -v