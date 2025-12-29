#!/bin/bash

set -e

echo "begin setup.sh"

echo "wget https://github.com/hatoo/oha/releases/latest/download/oha-linux-amd64"
wget https://github.com/hatoo/oha/releases/latest/download/oha-linux-amd64
mv oha-linux-amd64 oha
chmod +x ./oha

echo "oha --version"
./oha --version

OUTPUT_FILE=results/table.md
echo "OUTPUT_FILE=$OUTPUT_FILE"

rm -f $OUTPUT_FILE
echo '# Results' >> $OUTPUT_FILE
echo '## Timestamp' >> $OUTPUT_FILE
date | xargs echo -n >> $OUTPUT_FILE

echo '## Hardware Info' >> $OUTPUT_FILE
echo '| CPU Model | Num CPUs | Memory |' >> $OUTPUT_FILE
echo '| --------- | -------- | ------ |' >> $OUTPUT_FILE

CPU_MODEL=$(lscpu  | grep 'Model name' | cut -f2 -d ':' | xargs)
echo "CPU_MODEL=$CPU_MODEL"

NUM_CPUS=$(lscpu | grep 'CPU(s):' | grep -v NUMA  | cut -f2 -d ':' | xargs)
echo "NUM_CPUS=$NUM_CPUS"

TOTAL_MEMORY=$(lsmem  |grep 'Total online' | cut -f2 -d':' | xargs)
echo "TOTAL_MEMORY=$TOTAL_MEMORY"

echo "| $CPU_MODEL | $NUM_CPUS | $TOTAL_MEMORY |" >> $OUTPUT_FILE
echo >> $OUTPUT_FILE

echo '## Benchmarks of 1 Million Requests' >> $OUTPUT_FILE
echo '| Test Name | HTTP Conns | Success Rate | Test Seconds | Requests per Second | P50 Millis | P99 Millis | P99.9 Millis | API Memory MB | API CPU Time | API Threads |' >> $OUTPUT_FILE
echo '| --------- | ---------- | ------------ | ------------ | ------------------- | ---------- | ---------- | ------------ | ------------- | ------------ | ----------- |' >> $OUTPUT_FILE

echo "created md header OUTPUT_FILE=$OUTPUT_FILE"
cat $OUTPUT_FILE