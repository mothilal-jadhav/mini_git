import os

GIT_DIR = ".mini_git"
HEAD_FILE = os.path.join(GIT_DIR, "HEAD")
REFS_DIR = os.path.join(GIT_DIR, "refs")

# helper for current branch

def get_current_branch():

    with open(HEAD_FILE, "r") as f:
        return f.read().strip()
    
# create branch 

def create_branch(branch_name):

    current_branch = get_current_branch()

    current_ref = os.path.join(
        REFS_DIR,
        current_branch
    )

    with open(current_ref, "r") as f:
        latest_commit = f.read().strip()

    new_branch = os.path.join(
        REFS_DIR,
        branch_name
    )

    if os.path.exists(new_branch):
        print("Branch already exists")
        return

    with open(new_branch, "w") as f:
        f.write(latest_commit)

    print(f"Created branch {branch_name}")
    
# list branches

def list_branches():

    current = get_current_branch()

    for branch in os.listdir(REFS_DIR):

        if branch == current:
            print(f"* {branch}")
        else:
            print(f"  {branch}")
