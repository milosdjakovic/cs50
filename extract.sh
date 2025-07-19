#!/bin/bash

# Default values
INPUT_DIR=""
OUTPUT_DIR=""

# Get the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Function to display usage
usage() {
    echo "Usage: $0 -i <input_directory> -o <output_directory>"
    echo "  -i: Input directory containing the git repository"
    echo "  -o: Output directory where files will be extracted"
    exit 1
}

# Parse command line arguments
while getopts "i:o:h" opt; do
    case $opt in
        i)
            INPUT_DIR="$OPTARG"
            ;;
        o)
            OUTPUT_DIR="$OPTARG"
            ;;
        h)
            usage
            ;;
        \?)
            echo "Invalid option: -$OPTARG" >&2
            usage
            ;;
    esac
done

# Check if required arguments are provided
if [ -z "$INPUT_DIR" ] || [ -z "$OUTPUT_DIR" ]; then
    echo "Error: Both input and output directories are required."
    usage
fi

# Check if input directory exists and is a git repository
if [ ! -d "$INPUT_DIR" ]; then
    echo "Error: Input directory '$INPUT_DIR' does not exist."
    exit 1
fi

if [ ! -d "$INPUT_DIR/.git" ]; then
    echo "Error: '$INPUT_DIR' is not a git repository."
    exit 1
fi

# Create output directory if it doesn't exist (relative to script location)
OUTPUT_DIR="$SCRIPT_DIR/$OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR"

# Navigate to the git repository
cd "$INPUT_DIR" || exit 1

echo "Fetching all branches..."
git fetch --all

echo "Processing CS50 branches..."

# Get all remote branches that match the CS50 pattern
git branch -r | grep "origin/cs50/" | while read -r branch; do
    # Remove leading/trailing whitespace
    branch=$(echo "$branch" | xargs)
    
    # Skip if branch is empty
    [ -z "$branch" ] && continue
    
    echo "Processing branch: $branch"
    
    # Extract the path after "origin/" to create directory structure
    dir_path=$(echo "$branch" | sed 's|^origin/||')
    target_dir="$OUTPUT_DIR/$dir_path"
    
    # Create target directory
    mkdir -p "$target_dir"
    
    # Extract files from the branch
    echo "Extracting files to: $target_dir"
    git archive "$branch" | tar -x -C "$target_dir"
    
    if [ $? -eq 0 ]; then
        echo "✓ Successfully extracted files from $branch"
    else
        echo "✗ Failed to extract files from $branch"
    fi
    echo ""
done

echo "Extraction complete!"
echo "Files have been extracted to: $OUTPUT_DIR"
