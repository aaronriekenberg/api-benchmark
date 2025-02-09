#!/bin/bash

set -e

echo "begin run-rust.sh"

lscpu
lsmem

echo

OUTPUT_FILE=results/latest.csv
echo "OUTPUT_FILE=$OUTPUT_FILE"

TEST_NAME=rust-api

cd rust-api
echo "before cargo build"
cargo build --release
echo "after cargo build"
cd -
echo "pwd = $(pwd)"

DURATION=10s

for NUM_THREADS in 1 2 4 8; do

    for NUM_CONNECTIONS in 100 200 400; do

        echo "NUM_CONNECTIONS=$NUM_CONNECTIONS NUM_THREADS=$NUM_THREADS"

        ./rust-api/target/release/rust-api &
        API_PID=$!

        sleep 1

        echo "rust-api running PID $API_PID"

        rm -f wrk_output
        echo "wrk --latency -d$DURATION -t$NUM_THREADS -c$NUM_CONNECTIONS 'http://localhost:18080/test'"
        wrk --latency -d$DURATION -t$NUM_THREADS -c$NUM_CONNECTIONS 'http://localhost:18080/test' 2>&1 | tee wrk_output

        RPS=$(cat wrk_output | grep 'Requests/sec:' | awk '{print $2}' )
        echo "RPS = $RPS"

        REQUEST_P50=$(cat wrk_output | grep '50%' | awk '{print $2}' )
        echo "REQUEST_P50 = $REQUEST_P50"

        REQUEST_P99=$(cat wrk_output | grep '99%' | awk '{print $2}' )
        echo "REQUEST_P99 = $REQUEST_P99"

        echo ps -eLf -q $API_PID
        ps -eLf -q $API_PID

        THREADS_IN_APP=$( ps -eLf -q $API_PID | grep -v PID | wc -l)
        echo "THREADS_IN_APP=$THREADS_IN_APP"

        echo ps -eo pid,user,rss,time -q $API_PID
        ps -eo pid,user,rss,time -q $API_PID

        RSS_KB=$(ps -eo pid,user,rss,time -q $API_PID | tail -1 | awk '{print $3}' )
        echo "RSS_KB=$RSS_KB"

        CPU_TIME=$(ps -eo pid,user,rss,time -q $API_PID | tail -1 | awk '{print $4}' )
        echo "CPU_TIME=$CPU_TIME"

        echo kill $API_PID
        kill $API_PID

        echo "$TEST_NAME,$DURATION,$NUM_CONNECTIONS,$NUM_THREADS,$RPS,$REQUEST_P50,$REQUEST_P99,$RSS_KB,$CPU_TIME,$THREADS_IN_APP" >> $OUTPUT_FILE

        sleep 1
    done

done

echo "after tests cat $OUTPUT_FILE"
cat $OUTPUT_FILE
