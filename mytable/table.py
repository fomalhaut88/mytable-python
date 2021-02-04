"""
Table implements a class that works with a binary file as a series of blocks
with fixed size.
"""

import os


class Table:
    def __init__(self, path, block_size):
        self.path = path
        self.block_size = block_size
        if not os.path.exists(self.path):
            open(self.path, 'wb').close()
        self.file = open(self.path, 'rb+')

    def __del__(self):
        self.file.close()

    def size(self):
        """
        Gets number of blocks.
        """
        return os.fstat(self.file.fileno()).st_size // self.block_size

    def empty(self):
        """
        Returns True if the file is empty, else False.
        """
        return self.size() == 0

    def get(self, idx):
        """
        Gets block by index (its place in the series).
        """
        self.file.seek(idx * self.block_size)
        return self.file.read(self.block_size)

    def append(self, block):
        """
        Adds a new block to the end of the file.
        """
        idx = self.size()
        self.file.seek(idx * self.block_size)
        self.file.write(block)
        return idx

    def update(self, block, idx):
        """
        Updates block by its index.
        """
        self.file.seek(idx * self.block_size)
        self.file.write(block)

    def iter(self):
        """
        Iterates all blocks.
        """
        yield from self.iter_between(0, self.size())

    def iter_between(self, idx_from, idx_to):
        """
        Iterates blocks between two indexes.
        """
        self.file.seek(idx_from * self.block_size)
        for _ in range(idx_from, idx_to):
            yield self.file.read(self.block_size)

    def find_sorted(self, value, get_value):
        """
        Finds the index of the block with the given value.
        get_value is the function over block that returns its value to compare.
        """
        idx = 0
        size = self.size()

        while size > 0:
            block = self.get(idx + size // 2)

            if value > get_value(block):
                idx += size // 2 + 1
                size = size // 2 + size % 2 - 1
            else:
                size = size // 2

        return idx
