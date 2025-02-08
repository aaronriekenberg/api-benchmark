#!/bin/bash

#set -x

echo "begin run-go.sh"

lscpu

echo

cd go-api
echo "before go build"
go build
echo "after go build"

for NUM_CONNECTIONS in 100 200 400 800; do

    for NUM_THREADS in 1 2 4 8; do

        echo "NUM_CONNECTIONS=$NUM_CONNECTIONS NUM_THREADS=$NUM_THREADS"

        ./go-api &
        API_PID=$!

        sleep 1

        echo "go-api running PID $API_PID"

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