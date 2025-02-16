#!/bin/bash

set -e

echo "begin run-benchmarks.sh"

export OUTPUT_FILE=results/latest.md
echo "OUTPUT_FILE=$OUTPUT_FILE"

# build go
cd go-api
echo "before go build"
go build
echo "after go build"
cd -
echo "pwd = $(pwd)"

# run go benchmarks
export API_COMMAND='./go-api/go-api'
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
export API_COMMAND='./rust-api/target/release/rust-api'
export TEST_NAME=rust-api
./run-api-benchmark.sh

# build kotlin
cd kotlin-api
echo "before kotlin-api gradle build"
./gradlew clean build
echo "killall java"
killall java
cd -
echo "finished gradle build"

# run kotlin benchmarks
export API_COMMAND='java -jar ./kotlin-api/build/libs/kotlin-api.jar'
export TEST_NAME=kotlin-api
./run-api-benchmark.sh

# commit results
./commit-results.sh