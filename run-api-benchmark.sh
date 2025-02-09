#!/bin/bash

set -e

echo "begin run-api-benchmark.sh"

lscpu
lsmem

echo

$API_NAME &
API_PID=$!

sleep 1

echo "$TEST_NAME running PID $API_PID"

echo "./oha-linux-amd64 --http2 -n 1000000 -c 16 -p 100 --no-tui --json 'http://localhost:18080/test'"
./oha-linux-amd64 --http2 -n 1000000 -c 16 -p 100 --no-tui --json 'http://localhost:18080/test'

# rm -f wrk_output
# echo "wrk --latency -d$DURATION -t$NUM_THREADS -c$NUM_CONNECTIONS 'http://localhost:18080/test'"
# wrk --latency -d$DURATION -t$NUM_THREADS -c$NUM_CONNECTIONS 'http://localhost:18080/test' 2>&1 | tee wrk_output

# RPS=$(cat wrk_output | grep 'Requests/sec:' | awk '{print $2}' )
# echo "RPS = $RPS"

# REQUEST_P50=$(cat wrk_output | grep -A5 'Latency Distribution' | grep '50%' | awk '{print $2}' )
# echo "REQUEST_P50 = $REQUEST_P50"

# REQUEST_P99=$(cat wrk_output | grep -A5 'Latency Distribution' | grep '99%' | awk '{print $2}' )
# echo "REQUEST_P99 = $REQUEST_P99"

# echo ps -eLf -q $API_PID
# ps -eLf -q $API_PID

# THREADS_IN_APP=$(ps -eLf -q $API_PID | grep -v PID | wc -l)
# echo "THREADS_IN_APP=$THREADS_IN_APP"

# echo ps -eo pid,user,rss,time -q $API_PID
# ps -eo pid,user,rss,time -q $API_PID

# RSS_KB=$(ps -eo pid,user,rss,time -q $API_PID | tail -1 | awk '{print $3}' )
# echo "RSS_KB=$RSS_KB"

# CPU_TIME=$(ps -eo pid,user,rss,time -q $API_PID | tail -1 | awk '{print $4}' )
# echo "CPU_TIME=$CPU_TIME"

echo kill $API_PID
kill $API_PID

# echo "$TEST_NAME,$DURATION,$NUM_CONNECTIONS,$NUM_THREADS,$RPS,$REQUEST_P50,$REQUEST_P99,$RSS_KB,$CPU_TIME,$THREADS_IN_APP" >> $OUTPUT_FILE

# sleep 1


# echo "after tests cat $OUTPUT_FILE"
# cat $OUTPUT_FILE
