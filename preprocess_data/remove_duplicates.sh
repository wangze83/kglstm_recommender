#!/bin/bash

# Debug mode: Set to 1 to enable debug output
DEBUG=1

# Function to print debug messages
debug_msg() {
    if [ "$DEBUG" -eq 1 ]; then
        echo "[DEBUG] $1"
    fi
}

# Function to count lines in a file
count_lines() {
    lines=$(wc -l < "$1")
    echo "$lines"
}

# Main script

# Check command line arguments
if [ $# -ne 1 ]; then
    echo "Usage: $0 <input_file>"
    exit 1
fi

input_file=$1

# Check if input file exists
if [ ! -f "$input_file" ]; then
    echo "Error: File '$input_file' not found."
    exit 1
fi

debug_msg "Starting to remove duplicates from '$input_file'..."

# Count lines before removing duplicates
before=$(count_lines "$input_file")
debug_msg "Lines before removing duplicates: $before"

# Use awk to remove duplicate lines and output to a temporary file
awk '!seen[$0]++' "$input_file" > "$input_file.tmp"

# Count lines after removing duplicates
after=$(count_lines "$input_file.tmp")
debug_msg "Lines after removing duplicates: $after"

# Replace original file with the temporary file
mv "$input_file.tmp" "$input_file"

debug_msg "Duplicates removed from '$input_file'."

# Print summary
echo "Removed $(($before - $after)) duplicate lines."
echo "Final line count: $after"

exit 0
