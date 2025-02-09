#!/bin/bash

set -e

echo "begin run-benchmarks.sh"

export OUTPUT_FILE=results/latest.csv
echo "OUTPUT_FILE=$OUTPUT_FILE"

# build go
cd go-api
echo "before go build"
go build
echo "after go build"
cd -
echo "pwd = $(pwd)"

# run go benchmarks
export API_NAME='./go-api/go-api'
export TEST_NAME=go-api
./run-api-benchmark.sh

# build rust
cd rust-api
echo "before cargo build"
cargo build --release
echo "after cargo build"
cd -
echo "pwd = $(pwd)"

# run rust benchmarks
export API_NAME='./rust-api/target/release/rust-api'
export TEST_NAME=rust-api
./run-api-benchmark.sh

# commit results
# ./commit-results.sh