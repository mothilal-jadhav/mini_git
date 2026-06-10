# cli.py

import sys
from mini_git.repository import init_repo

command = sys.argv[1]

if command == "init":
    init_repo()