#!/bin/bash

set -e

echo "begin setup.sh"

wget https://github.com/hatoo/oha/releases/download/v1.7.0/oha-linux-amd64
chmod +x oha-linux-amd64

ls -altrh oha-linux-amd64

# OUTPUT_FILE=results/latest.csv
# echo "OUTPUT_FILE=$OUTPUT_FILE"

# rm -f $OUTPUT_FILE
# echo "TEST_NAME,DURATION,NUM_CONNECTIONS,NUM_THREADS,RPS,REQUEST_P50,REQUEST_P99,RSS_KB,CPU_TIME,THREADS_IN_APP" >> $OUTPUT_FILE
# echo "created CSV header OUTPUT_FILE=$OUTPUT_FILE"
# cat $OUTPUT_FILE