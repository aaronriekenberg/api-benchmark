#!/bin/bash

#set -x

echo "begin run.sh"

lscpu

echo

cd go-api
echo "before go build"
go build
echo "after go build"

for NUM_THREADS in 1 2 4; do

    echo "NUM_THREADS=$NUM_THREADS"

    ./go-api &
    GO_API_PID=$!

    echo "go-api running PID $GO_API_PID"

    echo "wrk --latency -t$NUM_THREADS -c100 -d10s http://localhost:18080/health"
    wrk --latency -t$NUM_THREADS -c100 -d10s http://localhost:18080/health

    echo ps -eLf -q $GO_API_PID
    ps -eLf -q $GO_API_PID

    echo ps -eo pid,user,rss,time -q $GO_API_PID
    ps -eo pid,user,rss,time -q $GO_API_PID

    echo kill $GO_API_PID
    kill $GO_API_PID

done