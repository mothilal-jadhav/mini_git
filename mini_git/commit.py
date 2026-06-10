import json
import hashlib
import os
import time
from datetime import datetime

GIT_DIR = ".mini_git"
INDEX_FILE = os.path.join(GIT_DIR, "index")
COMMITS_DIR = os.path.join(GIT_DIR, "commits")
HEAD_FILE = os.path.join(GIT_DIR, "HEAD")


# read current branch
def get_current_branch():

    with open(HEAD_FILE, "r") as f:
        return f.read().strip()
    
# get latest commit

def get_latest_commit():

    branch = get_current_branch()

    ref_file = os.path.join(GIT_DIR, "refs", branch)

    if not os.path.exists(ref_file):
        return None

    with open(ref_file, "r") as f:
        commit_id = f.read().strip()

    return commit_id if commit_id else None

# create commit 

def create_commit(message):

    with open(INDEX_FILE, "r") as f:
        index = json.load(f)

    parent = get_latest_commit()

    commit_data = {
        "message": message,
        "timestamp": time.time(),
        "parent": parent,
        "files": index
    }

    commit_hash = hashlib.sha256(
        json.dumps(commit_data, sort_keys=True).encode()
    ).hexdigest()

    path = os.path.join(COMMITS_DIR, commit_hash)

    with open(path, "w") as f:
        json.dump(commit_data, f, indent=4)

    branch = get_current_branch()

    with open(os.path.join(GIT_DIR, "refs", branch), "w") as f:
        f.write(commit_hash)

    print(f"Commit created: {commit_hash[:8]}")

# read commit 

def read_commit(commit_hash):

    path = os.path.join(COMMITS_DIR, commit_hash)

    with open(path, "r") as f:
        return json.load(f)
    
# log traversal

def show_log():

    current = get_latest_commit()

    while current:

        commit = read_commit(current)

        print(f"\ncommit {current}")
        date = datetime.fromtimestamp(commit['timestamp'])
        print(f"Date: {date.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"\n    {commit['message']}")
        print("\n--------------------------------")

        if "parents" in commit:
            current = commit["parents"][0]
        else:
            current = commit["parent"]

            