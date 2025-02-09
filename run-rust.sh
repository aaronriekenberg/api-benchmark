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

for NUM_THREADS in 4 8 16; do

    for NUM_CONNECTIONS in 100 200 400; do

        echo "NUM_CONNECTIONS=$NUM_CONNECTIONS NUM_THREADS=$NUM_THREADS"

        ./rust-api/target/release/rust-api &
        API_PID=$!

        sleep 1

        echo "rust-api running PID $API_PID"

        rm -f h2load_output
        echo "h2load --h1 -n500000 -t$NUM_THREADS -c$NUM_CONNECTIONS -m1 'http://localhost:18080/test'"
        h2load --h1 -n500000 -t$NUM_THREADS -c$NUM_CONNECTIONS -m1 'http://localhost:18080/test' 2>&1 | tee h2load_output

        RPS=$(cat h2load_output | grep 'finished in' | awk '{print $4}' )
        echo "RPS = $RPS"

        REQUEST_MAX=$(cat h2load_output | grep 'time for request: ' | awk '{print $5}' )
        echo "REQUEST_MAX = $REQUEST_MAX"

        REQUEST_MEAN=$(cat h2load_output | grep 'time for request: ' | awk '{print $6}' )
        echo "REQUEST_MEAN = $REQUEST_MEAN"

        REQUEST_SD=$(cat h2load_output | grep 'time for request: ' | awk '{print $7}' )
        echo "REQUEST_SD = $REQUEST_SD"

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

        echo "$TEST_NAME,$NUM_CONNECTIONS,$NUM_THREADS,$RPS,$REQUEST_MAX,$REQUEST_MEAN,$REQUEST_SD,$RSS_KB,$CPU_TIME" >> $OUTPUT_FILE

        sleep 1


    done

done

echo "after tests cat $OUTPUT_FILE"
cat $OUTPUT_FILE
