#!/usr/bin/env python3

import zlib
import mmap


class ZlibSearch():
    def __get_mapped_file(self, filename: str) -> None:
        with open(filename, 'rb') as file:
            decompressed_data: bytes = zlib.decompress(file.read())
            mapped_file = mmap.mmap(-1, len(decompressed_data),
                                    access=mmap.ACCESS_WRITE)
            mapped_file.write(decompressed_data)
            mapped_file.seek(0)
            return mapped_file

    def search(self, filename: str, search_pattern: str) -> int:
        mapped_file = self.__get_mapped_file(filename)
        offset: int = mapped_file.find(search_pattern.encode())
        mapped_file.close()
        return offset
