#!/bin/bash
# Usage: ./run.sh recursion/02_Fibonacci.java
# Compiles and runs any Java file — uses actual class name, not filename

FILE=$1

if [ -z "$FILE" ]; then
    echo "Usage: ./run.sh <path/to/File.java>"
    exit 1
fi

# Extract class name from file (not filename — they can differ with numeric prefixes)
CLASS=$(grep -m1 "^class\|^public class" "$FILE" | sed 's/public class //;s/class //;s/[{ ].*//')

mkdir -p target
javac -d target "$FILE" && java -cp target "$CLASS"
