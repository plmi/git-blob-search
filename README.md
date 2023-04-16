# git-blob-search

Searches for a keyword in the git blobs of a git repository.

## Usage

```bash
$ python src/git-blob-search.py <git root directory> SECRET_KEY
found in <git root directory>/.git/objects/7d/d5fd9a7e8bc0f3b5ba93dc4db561bca7dcd9e6

# manually inspect blob content
$ cd <git root directory>
$ git cat-file -p 7dd5fd9a7e8bc0f3b5ba93dc4db561bca7dcd9e6
```
