# cli.py

import sys

from mini_git.repository import init_repo
from mini_git.repository import add_file
from mini_git.commit import create_commit

command = sys.argv[1]

if command == "init":
    init_repo()

elif command == "add":
    filepath = sys.argv[2]
    add_file(filepath)

elif command == "commit":

    message = sys.argv[2]

    create_commit(message)