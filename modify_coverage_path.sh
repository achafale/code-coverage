#!/bin/bash

# Set variables for the file paths
COVERAGE_FILE=$1 # Path to the .coverage file
REMOTE_PATH=$2  # Remote path to be replaced
LOCAL_PATH=$3  # Local path to replace with

# Check if sqlite3 is installed
if ! command -v sqlite3 &> /dev/null; then
    echo "Error: sqlite3 is not installed. Please install it and try again."
    exit 1
fi

# Check if the coverage file exists
if [ ! -f "$COVERAGE_FILE" ]; then
    echo "Error: Coverage file $COVERAGE_FILE not found."
    exit 1
fi

# Backup the original .coverage file
cp "$COVERAGE_FILE" "${COVERAGE_FILE}.bak"
echo "Backup created at ${COVERAGE_FILE}.bak"

# Remap the paths in the .coverage SQLite database
sqlite3 "$COVERAGE_FILE" <<EOF
UPDATE file
SET path = REPLACE(path, '$REMOTE_PATH', '$LOCAL_PATH');
EOF

# Verify the changes
echo "Updated paths in the .coverage file:"
sqlite3 "$COVERAGE_FILE" "SELECT path FROM file WHERE path LIKE '%$LOCAL_PATH%' LIMIT 10;"

echo "Path remapping completed successfully."
