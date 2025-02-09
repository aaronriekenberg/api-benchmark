#!/bin/bash

set -e

echo "begin run-go.sh"

lscpu

echo

cd go-api
echo "before go build"
go build
echo "after go build"

for NUM_CONNECTIONS in 100; do

    for NUM_THREADS in 16; do

        echo "NUM_CONNECTIONS=$NUM_CONNECTIONS NUM_THREADS=$NUM_THREADS"

        ./go-api &
        API_PID=$!

        sleep 1

        echo "go-api running PID $API_PID"

        rm -f h2load_output
        echo "h2load --h1 -n400000 -t$NUM_THREADS -c$NUM_CONNECTIONS -m1000 'http://localhost:18080/health'"
        h2load --h1 -n400000 -t$NUM_THREADS -c$NUM_CONNECTIONS -m1000 'http://localhost:18080/health' 2>&1 | tee h2load_output

        echo "cat h2load_output"
        cat h2load_output

        echo ps -eLf -q $API_PID
        ps -eLf -q $API_PID

        THREADS_IN_APP=$( ps -eLf -q $API_PID | grep -v PID | wc -l)
        echo "THREADS_IN_APP=$THREADS_IN_APP"

        echo ps -eo pid,user,rss,time -q $API_PID
        ps -eo pid,user,rss,time -q $API_PID

        RSS_MB=$(ps -eo pid,user,rss,time -q $API_PID | tail -1 | awk '{print $3}' )
        echo "RSS_MB=$RSS_MB"

        CPU_TIME=$(ps -eo pid,user,rss,time -q $API_PID | tail -1 | awk '{print $4}' )
        echo "CPU_TIME=$CPU_TIME"

        echo kill $API_PID
        kill $API_PID

    done

done