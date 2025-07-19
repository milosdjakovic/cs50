# CS50

This repository contains all of my submissions for Harvard's CS50 courses.

## Extracting CS50 Branches

To extract all CS50 branches and their files from your remote repository, run:

```bash
./extract.sh git@github.com:me50/milosdjakovic.git
```

### Process Overview

- The script clones the given repository (if not already present).
- It fetches all remote branches.
- For each branch matching `origin/cs50/...`, it creates a corresponding directory structure under `extracted/` and extracts all files from the latest commit of that branch.
- After extraction, if there is a `cs50` directory inside `extracted/`, it moves it to the script directory, overwriting any existing `cs50` directory.
- At the end, you will see a prompt asking if you want to remove the cloned repository directory to save space. You can answer `y` (yes) or `n` (no).

This process ensures you always get the latest files from each CS50 branch, organized by branch name, and a clean `cs50` directory in your workspace.
