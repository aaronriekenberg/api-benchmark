#!/bin/bash

#set -x

echo "begin run-go.sh"

lscpu

echo

cd go-api
echo "before go build"
go build
echo "after go build"

for NUM_CONNECTIONS in 100; do

    for NUM_THREADS in 1; do

        echo "NUM_CONNECTIONS=$NUM_CONNECTIONS NUM_THREADS=$NUM_THREADS"

        ./go-api &
        API_PID=$!

        sleep 1

        echo "go-api running PID $API_PID"

        rm -f wrk_output
        echo "wrk --latency -t$NUM_THREADS -c$NUM_CONNECTIONS -d10s http://localhost:18080/health"
        wrk --latency -t$NUM_THREADS -c$NUM_CONNECTIONS -d10s http://localhost:18080/health | tee wrk_output

        RPS=$(cat wrk_output | grep 'Requests/sec:' | awk '{print $2}' )
        echo "RPS=$RPS"
        P99=$(cat wrk_output | grep '99%' | awk '{print $2}' )
        echo "P99=$P99"

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