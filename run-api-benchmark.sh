#!/bin/bash

set -e

echo "begin run-api-benchmark.sh"

lscpu
lsmem

#for NUM_CONNECTIONS in 200 400 800; do
for NUM_CONNECTIONS in 200; do

    echo "NUM_CONNECTIONS=$NUM_CONNECTIONS"

    echo "runnning API_COMMAND = $API_COMMAND"

    $API_COMMAND &
    API_PID=$!

    sleep 1

    echo "$TEST_NAME running PID $API_PID"

    rm -f oha_output.json
    echo "oha --http-version=1.1 -n 1000000 -c $NUM_CONNECTIONS --no-tui --json 'http://localhost:18080/test'"
    oha --http-version=1.1 -n 1000000 -c $NUM_CONNECTIONS --no-tui --json 'http://localhost:18080/test' | tee oha_output.json

    echo

    RPS=$(cat oha_output.json | jq '.rps.mean')
    RPS=$(bc <<< "scale=1; $RPS / 1")
    echo "RPS = $RPS"

    REQUEST_P50=$(cat oha_output.json | jq '.latencyPercentiles.p50' )
    REQUEST_P50=$(bc <<< "scale=4; $REQUEST_P50 * 1000 / 1")
    echo "REQUEST_P50 = $REQUEST_P50"

    REQUEST_P99=$(cat oha_output.json | jq '.latencyPercentiles.p99' )
    REQUEST_P99=$(bc <<< "scale=4; $REQUEST_P99 * 1000 / 1")
    echo "REQUEST_P99 = $REQUEST_P99"

    REQUEST_P999=$(cat oha_output.json | jq '.latencyPercentiles."p99.9"' )
    REQUEST_P999=$(bc <<< "scale=4; $REQUEST_P999 * 1000 / 1")
    echo "REQUEST_P999 = $REQUEST_P999"

    echo ps -eLf -q $API_PID
    ps -eLf -q $API_PID

    API_THREADS=$(ps -eLf -q $API_PID | grep -v PID | wc -l)
    echo "API_THREADS=$API_THREADS"

    echo ps -eo pid,user,rss,time -q $API_PID
    ps -eo pid,user,rss,time -q $API_PID

    RSS_KB=$(ps -eo pid,user,rss,time -q $API_PID | tail -1 | awk '{print $3}' )
    echo "RSS_KB=$RSS_KB"
    RSS_MB=$(bc <<< "scale=4; $RSS_KB / 1000")
    echo "RSS_MB=$RSS_MB"

    CPU_TIME=$(ps -eo pid,user,rss,time -q $API_PID | tail -1 | awk '{print $4}' )
    echo "CPU_TIME=$CPU_TIME"

    echo kill $API_PID
    kill $API_PID

    echo "| $TEST_NAME | $NUM_CONNECTIONS | $RPS | $REQUEST_P50 | $REQUEST_P99 | $REQUEST_P999 | $RSS_MB | $CPU_TIME | $API_THREADS |" >> $OUTPUT_FILE

    sleep 1

done

echo "after tests cat $OUTPUT_FILE"
cat $OUTPUT_FILE
