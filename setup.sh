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
echo '| TEST_NAME | NUM_CONNECTIONS | REQUESTS_PER_SECOND | P50_MILLIS | P99_MILLIS | P999_MILLIS | API_RSS_MB | API_CPU_TIME | API_THREADS |' >> $OUTPUT_FILE
echo '| --------- | --------------- | ------------------- | ---------- | ---------- | ----------- | ---------- | ------------ | ----------- |' >> $OUTPUT_FILE

echo "created md header OUTPUT_FILE=$OUTPUT_FILE"
cat $OUTPUT_FILE