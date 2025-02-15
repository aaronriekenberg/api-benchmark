#!/bin/bash

set -e

echo "begin setup.sh"

echo "deb [signed-by=/usr/share/keyrings/azlux-archive-keyring.gpg] http://packages.azlux.fr/debian/ stable main" | sudo tee /etc/apt/sources.list.d/azlux.list
sudo wget -O /usr/share/keyrings/azlux-archive-keyring.gpg https://azlux.fr/repo.gpg
sudo apt update -y
sudo apt install -y oha

oha --version

echo "java -XX:+PrintFlagsFinal -version"
java -XX:+PrintFlagsFinal -version

OUTPUT_FILE=results/latest.csv
echo "OUTPUT_FILE=$OUTPUT_FILE"

rm -f $OUTPUT_FILE
echo "TEST_NAME,NUM_CONNECTIONS,RPS,REQUEST_P50,REQUEST_P99,REQUEST_P999,RSS_KB,CPU_TIME,THREADS_IN_APP" >> $OUTPUT_FILE
echo "created CSV header OUTPUT_FILE=$OUTPUT_FILE"
cat $OUTPUT_FILE