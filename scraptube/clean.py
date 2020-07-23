#!/usr/bin/env python
# if running in py3, change the shebang, drop the next import for readability (it does no harm in py3)
from __future__ import print_function   # py2 compatibility
from collections import defaultdict
import hashlib
import os
import sys


def chunk_reader(fobj, chunk_size=1024):
    """Generator that reads a file in chunks of bytes"""
    while True:
        chunk = fobj.read(chunk_size)
        if not chunk:
            return
        yield chunk


def get_hash(filename, first_chunk_only=False, hash=hashlib.sha1):
    hashobj = hash()
    file_object = open(filename, 'rb')

    if first_chunk_only:
        hashobj.update(file_object.read(1024))
    else:
        for chunk in chunk_reader(file_object):
            hashobj.update(chunk)
    hashed = hashobj.digest()

    file_object.close()
    return hashed


def check_for_duplicates(paths, hash=hashlib.sha1):
    # dict of size_in_bytes: [full_path_to_file1, full_path_to_file2, ]
    hashes_by_size = defaultdict(list)
    # dict of (hash1k, size_in_bytes): [full_path_to_file1, full_path_to_file2, ]
    hashes_on_1k = defaultdict(list)
    hashes_full = {}   # dict of full_file_hash: full_path_to_file_string

    for path in paths:
        for dirpath, dirnames, filenames in os.walk(path):
            # get all files that have the same size - they are the collision candidates
            for filename in filenames:
                full_path = os.path.join(dirpath, filename)
                try:
                    # if the target is a symlink (soft one), this will
                    # dereference it - change the value to the actual target file
                    full_path = os.path.realpath(full_path)
                    file_size = os.path.getsize(full_path)
                    hashes_by_size[file_size].append(full_path)
                except (OSError,):
                    # not accessible (permissions, etc) - pass on
                    continue
