#!/bin/bash

set -e

if [ $# -ne 1 ]; then
    echo "Usage: $0 <git_repo_url>"
    exit 1
fi

REPO_URL="$1"
REPO_NAME=$(basename -s .git "$REPO_URL")
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Clone repo if not already present
if [ ! -d "$SCRIPT_DIR/$REPO_NAME" ]; then
    git clone "$REPO_URL" "$SCRIPT_DIR/$REPO_NAME"
fi

cd "$SCRIPT_DIR/$REPO_NAME"

git fetch --all

EXTRACTED_DIR="$SCRIPT_DIR/$REPO_NAME/extracted"

# Get all remote branches matching origin/cs50/
git branch -r | grep "^  origin/cs50/" | while read -r branch; do
    branch=$(echo "$branch" | xargs)
    dir_path=$(echo "$branch" | sed 's|^origin/||')
    target_dir="$EXTRACTED_DIR/$dir_path"
    mkdir -p "$target_dir"
    echo "Extracting $branch to $target_dir"
    git archive "$branch" | tar -x -C "$target_dir"
done

echo "Extraction complete! Files are in $EXTRACTED_DIR"
