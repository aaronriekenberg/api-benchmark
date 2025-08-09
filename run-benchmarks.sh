#!/bin/bash

set -e

echo "begin run-benchmarks.sh"

export OUTPUT_FILE=results/latest.md
echo "OUTPUT_FILE=$OUTPUT_FILE"

# python api
echo "python --version"
python --version

# python install tornado
echo "pip install tornado"
pip install tornado

# run python benchmarks
export API_COMMAND='python python-api/server.py'
export TEST_NAME=python
./run-api-benchmark.sh

# node api
echo "node --version"
node --version

# run node benchmarks
export API_COMMAND='node node-api/server.mjs'
export TEST_NAME=node
./run-api-benchmark.sh

# build kotlin
cd kotlin-api
echo "$(date) before kotlin-api gradle build"
./gradlew clean build
echo "killall java"
killall java
cd -
echo "$(date) after gradle build"
echo "pwd = $(pwd)"

# run kotlin benchmarks
export API_COMMAND='java -jar ./kotlin-api/build/libs/kotlin-api.jar'
export TEST_NAME=kotlin
./run-api-benchmark.sh

# build go
cd go-api
echo "$(date) before go build"
go build
echo "$(date) after go build"
cd -
echo "pwd = $(pwd)"

# run go benchmarks
export API_COMMAND='./go-api/go-api'
export TEST_NAME=go
./run-api-benchmark.sh

# build rust
echo "rustup update"
rustup update
cd rust-api
echo "$(date) before cargo build"
cargo build --release
echo "$(date) after cargo build"
cd -
echo "pwd = $(pwd)"

# run rust benchmarks
export API_COMMAND='./rust-api/target/release/rust-api'
export TEST_NAME=rust
./run-api-benchmark.sh

# commit results
./commit-results.sh