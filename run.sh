#!/bin/bash

#set -x

echo "begin run.sh"

lscpu

echo sudo apt install -y nghttp2
sudo apt install -y nghttp2

echo

cd go-api
echo "before go build"
go build
echo "after go build"

./go-api &
GO_API_PID=$!

echo "go-api running PID $GO_API_PID"

echo "h2load --h1 -t16 -c16 -n1000000 'http://localhost:18080/health'"
h2load --h1 -t16 -c16 -n1000000 'http://localhost:18080/health'

echo ps -eLf -q $GO_API_PID
ps -eLf -q $GO_API_PID

echo ps -eo pid,user,rss,time -q $GO_API_PID
ps -eo pid,user,rss,time -q $GO_API_PID

echo kill $GO_API_PID
kill $GO_API_PID
