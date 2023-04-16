#!/usr/bin/env python3

import re
import os
import zlib
import binascii
from typing import List
from models.git_blob import GitBlob


class GitTree:
    __sha1_pattern = '[0-9a-f]{40}'

    def __init__(self, tree_hash: str, git_root_directory: str):
        if not tree_hash:
            raise TypeError(f'{tree_hash} is not a valid string')

        if not re.match(self.__sha1_pattern, tree_hash):
            raise ValueError(f'{tree_hash} is not a valid hash')

        self.tree_hash = tree_hash
        self.git_root_directory = git_root_directory
        self.filename = self.__get_tree_object_filename()
        if not os.path.exists(self.filename):
            raise FileNotFoundError(f'Git tree {self.filename} not found')

    def __get_tree_object_filename(self) -> str:
        return f'{self.git_root_directory}/.git/objects/'\
                + f'{self.tree_hash[:2]}/{self.tree_hash[2:]}'

    def get_blobs(self) -> List[GitBlob]:
        # https://gist.github.com/leonidessaguisagjr/594cd8fbbc9b18a1dde5084d981b8028
        content = b''
        with open(self.filename, 'rb') as file:
            content = file.read()
        content = zlib.decompress(content)
        blobs = list()
        content = content.split(b'\x00', maxsplit=1)[1]
        while content != b'':
            filemode, content = content.split(b' ', maxsplit=1)
            filename, content = content.split(b'\x00', maxsplit=1)
            sha1, content = content[:20], content[20:]
            filemode = filemode.decode()
            filename = filename.decode()
            sha1 = binascii.hexlify(sha1).decode()
            blob: GitBlob = GitBlob(filemode, filename, sha1,
                                    self.git_root_directory)
            if blob not in blobs:
                blobs.append(blob)
        return blobs
