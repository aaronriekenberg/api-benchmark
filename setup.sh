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

OUTPUT_FILE=results/latest.md
echo "OUTPUT_FILE=$OUTPUT_FILE"

rm -f $OUTPUT_FILE
echo '# Results' >> $OUTPUT_FILE

echo '## CPU Info' >> $OUTPUT_FILE
echo '```' >> $OUTPUT_FILE
lscpu | egrep '(Model name:|CPU\(s\):)' | grep -v NUMA >> $OUTPUT_FILE
echo '```' >> $OUTPUT_FILE

echo '## Memory Info' >> $OUTPUT_FILE
lsmem | grep 'Total online' | awk '{ print $4 }' >> $OUTPUT_FILE

echo '## Benchmark Tests' >> $OUTPUT_FILE
echo '| Test Name | Connections | Requests per Second | P50 Millis | P99 Millis | P999 Millis | API Memory MB | API CPU Time | API Threads |' >> $OUTPUT_FILE
echo '| --------- | ----------- | ------------------- | ---------- | ---------- | ----------- | ------------- | ------------ | ----------- |' >> $OUTPUT_FILE

echo "created md header OUTPUT_FILE=$OUTPUT_FILE"
cat $OUTPUT_FILE