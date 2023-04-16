#!/usr/bin/env python3

import zlib
from services.zlib_search import ZlibSearch


class GitBlob:
    def __init__(self, filemode: str, filename: str, hash: str,
                 git_root_directory: str):
        self.filemode = filemode
        self.filename = filename
        self.hash = hash
        self.git_root_directory = git_root_directory

    def __hash__(self):
        return hash(self.hash)

    # TODO: refactor into helper function
    def __get_blob_object_filename(self) -> str:
        return f'{self.git_root_directory}/.git/objects/'\
                + f'{self.hash[:2]}/{self.hash[2:]}'

    def __eq__(self, blob):
        if isinstance(blob, GitBlob):
            return self.hash == blob.hash

        return False

    def __str__(self):
        return self.__get_blob_object_filename()

    def search(self, search_pattern: str) -> int:
        return ZlibSearch().search(self.__str__(), search_pattern)

    def get_decompressed(self) -> bytes:
        with open(str(self), 'rb') as file:
            return zlib.decompress(file.read())
