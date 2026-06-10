import json
import os
import hashlib
import time

GIT_DIR = ".mini_git"

# merge helper

def current_branch():

    with open(os.path.join(GIT_DIR, "HEAD")) as f:
        return f.read().strip()
    

# reading commit 

def read_commit(commit_hash):

    path = os.path.join(
        GIT_DIR,
        "commits",
        commit_hash
    )

    with open(path) as f:
        return json.load(f)
    

# merge function

def merge_branch(source_branch):

    target_branch = current_branch()

    with open(
        os.path.join(
            GIT_DIR,
            "refs",
            target_branch
        )
    ) as f:
        target_commit = f.read().strip()

    with open(
        os.path.join(
            GIT_DIR,
            "refs",
            source_branch
        )
    ) as f:
        source_commit = f.read().strip()

    target_data = read_commit(
        target_commit
    )

    source_data = read_commit(
        source_commit
    )

    merged_files = {
        **target_data["files"],
        **source_data["files"]
    }

    commit_data = {
        "message":
            f"Merge branch '{source_branch}'",
        "timestamp":
            time.time(),
        "parents":
            [
                target_commit,
                source_commit
            ],
        "files":
            merged_files
    }

    merge_hash = hashlib.sha256(
        json.dumps(
            commit_data,
            sort_keys=True
        ).encode()
    ).hexdigest()

    path = os.path.join(
        GIT_DIR,
        "commits",
        merge_hash
    )

    with open(path, "w") as f:
        json.dump(
            commit_data,
            f,
            indent=4
        )

    with open(
        os.path.join(
            GIT_DIR,
            "refs",
            target_branch
        ),
        "w"
    ) as f:
        f.write(merge_hash)

    print(
        f"Merged {source_branch}"
    )

