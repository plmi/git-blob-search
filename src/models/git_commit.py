#!/usr/bin/env python3

import os
import re
import zlib
from models.git_tree import GitTree


class GitCommit:
    __sha1_pattern = '[0-9a-f]{40}'
    __tree_pattern = 'tree [0-9a-f]{40}'

    def __init__(self, commit_hash: str, git_root_directory: str):
        if not commit_hash:
            raise TypeError(f'{commit_hash} is not a valid string')

        if not re.match(self.__sha1_pattern, commit_hash):
            raise ValueError(f'{commit_hash} is not a valid commit hash')

        self.commit_hash = commit_hash
        self.git_root_directory = git_root_directory
        self.filename = self.__get_filename(self.git_root_directory,
                                            self.commit_hash)

    def __get_filename(self, git_root_directory: str, commit_hash: str) -> str:
        return os.path.join(git_root_directory,
                            '.git', 'objects',
                            f'{commit_hash[:2]}/{commit_hash[2:]}')

    def __get_tree_object_decompressed(self) -> str:
        with open(self.filename, 'rb') as file:
            return zlib.decompress(file.read()).decode()

    def get_tree_object(self) -> GitTree:
        tree_content: str = self.__get_tree_object_decompressed()
        match = re.search(self.__tree_pattern, tree_content)
        if match:
            tree_hash = match.group()[5:]
            return GitTree(tree_hash, self.git_root_directory)
        else:
            raise ValueError("tree object not found")
