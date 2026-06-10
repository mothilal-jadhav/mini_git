# mini_git/repository.py
from mini_git.objects import store_blob
import json
import os

GIT_DIR = ".mini_git"
INDEX_FILE = os.path.join(GIT_DIR, "index")

def add_file(filepath):

    sha = store_blob(filepath)

    if os.path.exists(INDEX_FILE):
        with open(INDEX_FILE, "r") as f:
            content = f.read()

            if content:
                index = json.loads(content)
            else:
                index = {}
    else:
        index = {}

    index[filepath] = sha

    with open(INDEX_FILE, "w") as f:
        json.dump(index, f, indent=4)

    print(f"Added {filepath}")

def init_repo():
    if os.path.exists(GIT_DIR):
        print("Repository already initialized")
        return

    os.makedirs(f"{GIT_DIR}/objects")
    os.makedirs(f"{GIT_DIR}/refs")

    with open(f"{GIT_DIR}/HEAD", "w") as f:
        pass

    print("Initialized empty mini_git repository")