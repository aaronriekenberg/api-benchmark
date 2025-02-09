#!/bin/bash

set -e

echo "begin setup.sh"

echo sudo apt install -y wrk
sudo apt install -y wrk

OUTPUT_FILE=results/latest.csv
echo "OUTPUT_FILE=$OUTPUT_FILE"

rm -f $OUTPUT_FILE
echo "TEST_NAME,DURATION,NUM_CONNECTIONS,NUM_THREADS,RPS,REQUEST_P50,REQUEST_P99,RSS_KB,CPU_TIME,THREADS_IN_APP" >> $OUTPUT_FILE
echo "created CSV header OUTPUT_FILE=$OUTPUT_FILE"
cat $OUTPUT_FILE