# mini_git/repository.py

import os

GIT_DIR = ".mini_git"

def init_repo():
    if os.path.exists(GIT_DIR):
        print("Repository already initialized")
        return

    os.makedirs(f"{GIT_DIR}/objects")
    os.makedirs(f"{GIT_DIR}/refs")

    with open(f"{GIT_DIR}/HEAD", "w") as f:
        pass

    print("Initialized empty mini_git repository")