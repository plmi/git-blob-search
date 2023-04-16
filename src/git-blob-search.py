#!/usr/bin/env python3

import argparse
from typing import List
from os.path import abspath
from models.git_commit import GitCommit
from models.git_root_directory import GitRootDirectory
from models.git_tree import GitTree
from models.git_blob import GitBlob


def main():
    parser = argparse.ArgumentParser(description='Parse git objects')
    parser.add_argument('git_root_directory', type=str, help='git root dir')
    parser.add_argument('keyword', type=str, help='keyword to search for')
    args = parser.parse_args()

    root: GitRootDirectory = GitRootDirectory(abspath(args.git_root_directory))
    commits: List[GitCommit] = root.get_commits()
    unique_blobs: List[GitBlob] = list()
    for commit in commits:
        tree: GitTree = commit.get_tree_object()
        blobs: List[GitBlob] = tree.get_blobs()
        for blob in blobs:
            if blob not in unique_blobs:
                unique_blobs.append(blob)

    for blob in unique_blobs:
        if blob.search(args.keyword) != -1:
            print(f'found in {blob}')


if __name__ == '__main__':
    main()
