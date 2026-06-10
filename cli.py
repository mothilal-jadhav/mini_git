# cli.py

import sys

from mini_git.repository import init_repo
from mini_git.repository import add_file
from mini_git.repository import status
from mini_git.commit import create_commit
from mini_git.commit import show_log
from mini_git.branch import (
    create_branch,
    list_branches
)
from mini_git.branch import checkout_branch
from mini_git.merge import merge_branch

command = sys.argv[1]

if command == "init":
    init_repo()

elif command == "add":
    filepath = sys.argv[2]
    add_file(filepath)

elif command == "commit":

    message = sys.argv[2]

    create_commit(message)

elif command == "log":
    show_log()

elif command == "branch":

    if len(sys.argv) == 2:
        list_branches()

    else:
        create_branch(sys.argv[2])

elif command == "checkout":

    branch_name = sys.argv[2]

    checkout_branch(branch_name)

elif command == "status":
    status()

elif command == "merge":

    merge_branch(
        sys.argv[2]
    )

