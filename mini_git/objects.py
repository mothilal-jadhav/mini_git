import hashlib
import os

GIT_DIR = ".mini_git"
OBJECTS_DIR = os.path.join(GIT_DIR, "objects")


def hash_content(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def store_blob(filepath: str) -> str:

    with open(filepath, "rb") as f:
        content = f.read()

    sha = hash_content(content)

    object_path = os.path.join(OBJECTS_DIR, sha)

    if not os.path.exists(object_path):
        with open(object_path, "wb") as obj:
            obj.write(content)

    return sha


def read_blob(sha: str):

    object_path = os.path.join(OBJECTS_DIR, sha)

    with open(object_path, "rb") as f:
        return f.read()