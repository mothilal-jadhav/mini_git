# Mini Git

A lightweight Git-inspired Version Control System built from scratch in Python.

This project was created to understand the internal architecture of Git rather than simply using Git commands. The implementation recreates the core concepts behind version control systems, including content-addressable storage, staging areas, commits, commit history traversal, branching, and commit graph management.

---

## Project Goal

The objective of Mini Git is to learn how modern version control systems work internally by implementing their core components from scratch.

Instead of relying on Git's built-in functionality, this project builds:

* Repository initialization
* SHA-256 object storage
* Staging area (index)
* Commit creation
* Commit history traversal
* Branch creation
* Branch checkout
* Directed Acyclic Graph (DAG) based commit relationships

---

## Features Implemented

### Repository Initialization

Command:

```bash
python cli.py init
```

Creates the repository structure:

```text
.mini_git/
├── HEAD
├── index
├── objects/
├── commits/
└── refs/
```

Purpose:

* Initializes the repository metadata
* Creates storage directories
* Creates the default branch (`main`)
* Prepares the object database

Example Output:

```text
Initialized empty mini_git repository
```

---

### Content Addressable Storage (SHA-256)

Git stores files based on content rather than filename.

Mini Git follows the same principle.

Workflow:

```text
File
 ↓
SHA-256 Hash
 ↓
Object Store
```

Example:

File:

```text
Hello Mini Git
```

Generated Hash:

```text
0e20a32b6ca13e1605f41cd842a9994123e5ab6415d5d85042f45aae141075e5
```

Stored as:

```text
.mini_git/objects/
└── 0e20a32b6ca13e1605f41cd842a9994123e5ab6415d5d85042f45aae141075e5
```

Verification:

```python
read_blob(hash)
```

Output:

```text
b'Hello Mini Git\n'
```

Result:

* Same content → Same hash
* Different content → Different hash
* Enables deduplication

---

### Staging Area (Index)

Implemented equivalent of:

```bash
git add
```

Command:

```bash
python cli.py add notes.txt
```

Workflow:

```text
Working Directory
       ↓
    add()
       ↓
    index
```

Index Structure:

```json
{
    "notes.txt": "7e1d24bc9640..."
}
```

Testing:

Version 1:

```text
Version 1
```

Hash:

```text
fe95a2...
```

Version 2:

```text
Version 2
```

Hash:

```text
7e1d24...
```

Result:

* Index always tracks latest file state
* Previous blobs remain preserved in object storage

---

### Commit Objects

Implemented equivalent of:

```bash
git commit
```

Command:

```bash
python cli.py commit "Initial commit"
```

Commit Structure:

```json
{
    "message": "Initial commit",
    "timestamp": 1781103297,
    "parent": null,
    "files": {
        "notes.txt": "7e1d24..."
    }
}
```

Stored inside:

```text
.mini_git/commits/
```

Each commit is hashed and uniquely identified.

Example:

```text
e7d907bef3eaccbefcceaa2c80246289e83d5ed5d4abca5e0071c880282d18ed
```

---

### Commit Chain

Each commit stores its parent.

Example:

```text
C3
 |
C2
 |
C1
```

Actual Project Example:

```text
ac3e90ea
    |
e7d907be
```

This creates a linked history similar to Git.

---

### Commit Log

Implemented equivalent of:

```bash
git log
```

Command:

```bash
python cli.py log
```

Sample Output:

```text
commit 9b75ceb43030ef30512a00d84c0d0264069f35a08413507da518ca5298e1e316
Date: 2026-06-10 21:48:44

    Added feature work

--------------------------------

commit ac3e90ea8594f47bbaf25becd85f45416c239a4d818b583f87f5e2f3079120aa
Date: 2026-06-10 20:24:57

    Updated notes

--------------------------------

commit e7d907bef3eaccbefcceaa2c80246289e83d5ed5d4abca5e0071c880282d18ed
Date: 2026-06-10 20:19:54

    Initial commit
```

Logic:

```text
HEAD
 ↓
Latest Commit
 ↓
Parent
 ↓
Parent
 ↓
NULL
```

---

### Branch Creation

Implemented equivalent of:

```bash
git branch feature-auth
```

Command:

```bash
python cli.py branch feature-auth
```

Result:

```text
refs/
├── main
└── feature-auth
```

Both initially point to the same commit.

Example:

```text
main --------┐
             │
             ▼
        ac3e90ea
             ▲
             │
feature-auth ┘
```

Important Insight:

A branch is simply a pointer to a commit.

No files are copied.

No commits are duplicated.

---

### Branch Listing

Command:

```bash
python cli.py branch
```

Output:

```text
* main
  feature-auth
```

Current branch is marked with `*`.

---

### Branch Checkout

Implemented equivalent of:

```bash
git checkout
```

Command:

```bash
python cli.py checkout feature-auth
```

Updates:

```text
HEAD
```

Before:

```text
main
```

After:

```text
feature-auth
```

Output:

```text
Switched to branch 'feature-auth'
```

---

### Branch Divergence

After switching branches:

```bash
python cli.py checkout feature-auth
```

New work:

```bash
echo "Feature branch work" > feature.txt
python cli.py add feature.txt
python cli.py commit "Added feature work"
```

Result:

```text
feature-auth
     |
     v
9b75ceb
     |
     v
ac3e90e

main
 |
 v
ac3e90e
```

Now both branches point to different commits.

This is the foundation of a DAG-based version control system.

---

## Internal Architecture

```text
Working Directory
        │
        ▼
    git add
        │
        ▼
      Index
        │
        ▼
     Commit
        │
        ▼
 Commit Database
        │
        ▼
     Branches
        │
        ▼
       HEAD
```

---

## Data Structures Used

### Hashing

Used for:

* Blob identification
* Commit identification

Algorithm:

```text
SHA-256
```

Time Complexity:

```text
O(n)
```

Where n is content size.

---

### Hash Maps

Used in:

```python
index = {
    filepath: blob_hash
}
```

Complexity:

```text
Insert : O(1)
Lookup : O(1)
Update : O(1)
```

---

### Linked Commit Chain

Each commit references its parent.

```text
Commit
   ↓
Parent
   ↓
Parent
```

Complexity:

```text
Traversal = O(number_of_commits)
```

---

### Directed Acyclic Graph (DAG)

Current branch structure already forms a DAG.

```text
feature-auth
     |
     C3
     |
main-C2
     |
     C1
```

Future merge commits will create multi-parent DAG nodes.

---

## Current Commands

```bash
python cli.py init

python cli.py add <file>

python cli.py commit "<message>"

python cli.py log

python cli.py branch

python cli.py branch <name>

python cli.py checkout <branch>

python cli.py status
```

---

## Future Enhancements

* Merge commits
* Three-way merge strategy
* File restoration during checkout
* Diff engine
* Delta compression
* Garbage collection
* Remote repository support
* FastAPI API layer
* Docker deployment
* CI/CD pipelines

---
