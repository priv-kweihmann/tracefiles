# SPDX-FileCopyrightText: 2022 Konrad Weihmann
# SPDX-License-Identifier: BSD-2-Clause

import argparse
import hashlib
import logging
import os
import subprocess  # noqa: S404
import sys
from typing import Dict
from typing import List
from typing import Set


class PathWithScanningDepth:

    def __init__(self, path: str) -> None:
        self.depth: int = sys.maxsize
        chunks = path.split(':')
        self.path: str = chunks[0]
        if len(chunks) > 1:
            try:  # pragma: no cover
                self.depth = int(chunks[1])  # pragma: no cover
            except ValueError:  # pragma: no cover
                raise argparse.ArgumentError(
                    'Depth information must be a digit')

    def __repr__(self) -> str:
        return self.path  # pragma: no cover


def create_argparser():
    parser = argparse.ArgumentParser(prog='tracefiles',  # pragma: no cover
                                     description='A utility to find used sources from a binary')  # pragma: no cover
    parser.add_argument('--debugpaths', nargs='+', default=[], action='extend',  # pragma: no cover
                        help='Potential paths where to look for debug info')  # pragma: no cover
    parser.add_argument('--addsourcedirs', type=PathWithScanningDepth, nargs='+', default=[], action='extend',  # pragma: no cover
                        help='Additional paths to scan for sources')  # pragma: no cover
    parser.add_argument('sourcedir', type=PathWithScanningDepth,  # pragma: no cover
                        help='Directory with the source code')  # pragma: no cover
    parser.add_argument('binaries', nargs='+', help='The binaries to inspect')  # pragma: no cover
    return parser.parse_args()  # pragma: no cover


def get_debug_paths(binary: str, paths: List[str]) -> List[str]:
    _cleaninpath = binary.lstrip('/')
    res = []
    for path in paths:
        res.append(os.path.join(path, os.path.basename(_cleaninpath)))
    res.append(binary)
    return res


def md5hash(filepath: str) -> str:
    hash_md5 = hashlib.md5()  # noqa: S303, S324, DUO130
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def find_and_translate(hash_map: Dict, sources: List[str]) -> Set[str]:
    result = set()
    for sfile in sources:
        found = False
        # get matching objects by name
        chunks = sfile.split('/')
        while chunks:
            if '/'.join(chunks) in hash_map:
                result.add('/'.join(chunks))
                found = True
                break
            chunks = chunks[1:]
        if not found:
            _globs = [k for k in hash_map.keys(
            ) if os.path.basename(k) == sfile]
            if _globs:
                result.update(_globs)  # pragma: no cover
                found = True  # pragma: no cover
        if not found:
            try:
                _hash = md5hash(sfile)
                for k, v in hash_map.items():
                    if v == _hash:
                        result.add(k)
            except (FileNotFoundError, IsADirectoryError):  # pragma: no cover
                pass  # pragma: no cover
    return result


def hash_sources(sourcedirs: List[PathWithScanningDepth]) -> Dict:
    res = {}
    for sdir in sourcedirs:
        for root, _, files in os.walk(sdir.path):
            for f in files:
                filepath = os.path.join(root, f)
                relpath = os.path.relpath(filepath, sdir.path)
                if relpath.count(os.path.sep) > sdir.depth:
                    continue  # pragma: no cover
                res[relpath] = md5hash(filepath)
    return res


def get_sources(sourcedirs: List[PathWithScanningDepth], binaries: List[str], debugpaths: List[str]) -> List[str]:
    res = set()
    hash_map = hash_sources(sourcedirs)
    for binary in binaries:
        for inpath in get_debug_paths(binary, debugpaths):
            logging.info(f'Analyzing {inpath}')  # noqa: G004
            if os.path.exists(inpath) and os.path.isfile(inpath):
                _src_files = []
                _cmdline = f'readelf -wi {inpath} | grep -B1 DW_AT_comp_dir | awk \'/DW_AT_name/{{name = $NF; getline; print name}}\''  # noqa: E702
                try:
                    _src_files = subprocess.check_output(_cmdline,  # noqa: DUO116
                                                            universal_newlines=True,
                                                            shell=True,  # noqa: S602,
                                                            stderr=subprocess.DEVNULL)
                    _src_files = [x for x in _src_files.split('\n') if x]
                    if not _src_files:
                        raise Exception()
                    _cmdline = f'readelf -w {inpath} | grep "indirect line string, offset"'
                    try:
                        _src_files += [x.split(':')[-1].strip()
                                        for x in subprocess.check_output(_cmdline,  # noqa: DUO116
                                                                        universal_newlines=True,
                                                                        shell=True,  # noqa: S602
                                                                        stderr=subprocess.DEVNULL).split('\n')
                                        if x]
                    except Exception:  # pragma: no cover
                        logging.info(  # pragma: no cover
                            f'Problems getting full DWARF info for {inpath}')  # noqa: G004
                    _src_files = {x.replace('../', '')  # pragma: no cover
                                  for x in _src_files if x}
                    _src_files = find_and_translate(hash_map, _src_files)
                except Exception:
                    logging.info(f'{inpath} is not a binary')  # noqa: G004
                    # find a plain file copy
                    _src_files = find_and_translate(hash_map, [inpath])
                res.update(_src_files)
    return sorted(res)


def main():
    args = create_argparser()  # pragma: no cover
    for file_ in get_sources([args.sourcedir] + args.addsourcedirs,  # pragma: no cover
                             args.binaries, args.debugpaths):
        print(file_)  # pragma: no cover


if __name__ == '__main__':
    main()  # pragma: no cover
