#!/bin/bash

#set -x

echo "begin run-rust.sh"

lscpu

echo

cd rust-api
echo "before cargo build"
cargo build --release
echo "after cargo build"

for NUM_CONNECTIONS in 100 200 400 800; do

    for NUM_THREADS in 1 2 4 8; do

        echo "NUM_CONNECTIONS=$NUM_CONNECTIONS NUM_THREADS=$NUM_THREADS"

        ./target/release/rust-api &
        API_PID=$!

        sleep 1

        echo "api running PID $API_PID"

        echo "wrk --latency -t$NUM_THREADS -c$NUM_CONNECTIONS -d10s http://localhost:18080/health"
        wrk --latency -t$NUM_THREADS -c$NUM_CONNECTIONS -d10s http://localhost:18080/health

        echo ps -eLf -q $API_PID
        ps -eLf -q $API_PID

        echo ps -eo pid,user,rss,time -q $API_PID
        ps -eo pid,user,rss,time -q $API_PID

        echo kill $API_PID
        kill $API_PID

    done

done