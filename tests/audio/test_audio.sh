#!/bin/bash

# Array of values for N
values=(1 2 3 4 5 6 7 8 9 10 13 20 52 83 50 100 128 256 500 503 1000 1095 1952 2024)

# Loop through each value of N and run the command
for n in "${values[@]}"; do
    echo "Running with N = $n"
    python speech2text_test.py $n
    echo "Completed N = $n"
    echo ""
done
