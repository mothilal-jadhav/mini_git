# cli.py

import sys

from mini_git.repository import init_repo
from mini_git.repository import add_file

command = sys.argv[1]

if command == "init":
    init_repo()

elif command == "add":
    filepath = sys.argv[2]
    add_file(filepath)