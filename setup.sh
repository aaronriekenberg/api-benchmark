#!/bin/bash

set -e

echo "begin setup.sh"

echo sudo apt install -y nghttp2
sudo apt install -y nghttp2

OUTPUT_FILE=results/latest.csv
echo "OUTPUT_FILE=$OUTPUT_FILE"

rm -f $OUTPUT_FILE
echo "TEST_NAME,NUM_REQUESTS,NUM_CONNECTIONS,NUM_THREADS,RPS,REQUEST_MAX,REQUEST_MEAN,REQUEST_SD,RSS_KB,CPU_TIME,THREADS_IN_APP" >> $OUTPUT_FILE
echo "created CSV header OUTPUT_FILE=$OUTPUT_FILE"
cat $OUTPUT_FILE