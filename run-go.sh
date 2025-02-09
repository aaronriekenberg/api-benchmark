#!/bin/bash

set -e

echo "begin run-go.sh"

lscpu

echo

OUTPUT_FILE=output/latest.csv
echo "OUTPUT_FILE=$OUTPUT_FILE"

rm -f $OUTPUT_FILE
touch $OUTPUT_FILE
echo "NUM_CONNECTIONS,NUM_THREADS,RPS,REQUEST_MAX,REQUEST_MEAN,REQUEST_SD,RSS_KB,CPU_TIME" >> $OUTPUT_FILE

cd go-api
echo "before go build"
go build
echo "after go build"

for NUM_THREADS in 8; do

    for NUM_CONNECTIONS in 100; do

        echo "NUM_CONNECTIONS=$NUM_CONNECTIONS NUM_THREADS=$NUM_THREADS"

        ./go-api &
        API_PID=$!

        sleep 1

        echo "go-api running PID $API_PID"

        rm -f h2load_output
        echo "h2load --h1 -n400000 -t$NUM_THREADS -c$NUM_CONNECTIONS -m1 'http://localhost:18080/test'"
        h2load --h1 -n400000 -t$NUM_THREADS -c$NUM_CONNECTIONS -m1 'http://localhost:18080/test' 2>&1 | tee h2load_output

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

        echo "$NUM_CONNECTIONS,$NUM_THREADS,$RPS,$REQUEST_MAX,$REQUEST_MEAN,$REQUEST_SD,$RSS_KB,$CPU_TIME" >> $OUTPUT_FILE

        sleep 1

    done

done

echo "after tests cat $OUTPUT_FILE"
cat $OUTPUT_FILE

echo "final git commands"
set -e

git add $OUTPUT_FILE
git status
git commit -m 'results from github actions'
git push -v