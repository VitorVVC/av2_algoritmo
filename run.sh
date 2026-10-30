#!/bin/sh
set -eu
cd "$(dirname "$0")"
mkdir -p target/classes
find src/main/java -name '*.java' > target/sources.txt
javac --release 21 -encoding UTF-8 -d target/classes @target/sources.txt
java -cp target/classes br.edu.unifor.cpc.Main "$@"
