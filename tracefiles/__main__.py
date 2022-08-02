# SPDX-FileCopyrightText: 2022 Konrad Weihmann
# SPDX-License-Identifier: BSD-2-Clause

import argparse
import glob
import hashlib
import logging
import os
import subprocess
from typing import Dict
from typing import List
from typing import Set


def create_argparser():
    parser = argparse.ArgumentParser(prog='tracefiles',
                                     description='A utility to find used sources from a binary')
    parser.add_argument('--debugpaths', nargs='+', default=[], action='extend',
                        help='Potential paths where to look for debug info')
    parser.add_argument('sourcedir', help='Directory with the source code')
    parser.add_argument('binaries', nargs='+', help='The binaries to inspect')
    return parser.parse_args()


def get_debug_paths(binary: str, paths: List[str]) -> List[str]:
    _cleaninpath = binary.lstrip('/')
    res = []
    for path in paths:
        res.append(os.path.join(path, os.path.basename(_cleaninpath)))
    res.append(binary)
    return res


def md5hash(filepath: str) -> str:
    hash_md5 = hashlib.md5()
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
                result.update(_globs)
                found = True
        if not found:
            try:
                _hash = md5hash(sfile)
                for k, v in hash_map.items():
                    if v == _hash:
                        result.add(k)
            except (FileNotFoundError, IsADirectoryError):
                pass
    return result


def hash_sources(sourcedir) -> Dict:
    res = {}
    for root, _, files in os.walk(sourcedir):
        for f in files:
            filepath = os.path.join(root, f)
            relpath = os.path.relpath(filepath, sourcedir)
            res[relpath] = md5hash(filepath)
    return res


def get_sources(sourcedir: str, binaries: List[str], debugpaths: List[str]) -> List[str]:
    res = set()
    hash_map = hash_sources(sourcedir)
    for binary in binaries:
        for inpath in get_debug_paths(binary, debugpaths):
            logging.info(f'Analyzing {inpath}')
            if os.path.exists(inpath):
                _src_files = []
                _cmdline = f'readelf -wi {inpath} | grep -B1 DW_AT_comp_dir | awk \'/DW_AT_name/{{name = $NF; getline; print name}}\''
                try:
                    _src_files = subprocess.check_output(_cmdline,
                                                            universal_newlines=True,
                                                            shell=True,  # noqa: S602
                                                            stderr=subprocess.DEVNULL)
                    _src_files = [x for x in _src_files.split('\n') if x]
                    if not _src_files:
                        raise Exception()
                    _cmdline = f'readelf -w {inpath} | grep "indirect line string, offset"'
                    try:
                        _src_files += [x.split(':')[-1].strip()
                                        for x in subprocess.check_output(_cmdline,
                                                                        universal_newlines=True,
                                                                        shell=True,  # noqa: S602
                                                                        stderr=subprocess.DEVNULL).split('\n')
                                        if x]
                    except:
                        logging.info(
                            f"Problems getting full DWARF info for {inpath}")
                    _src_files = set([x.replace('../', '')
                                      for x in _src_files if x])
                    _src_files = find_and_translate(hash_map, _src_files)
                except:
                    logging.info(f'{inpath} is not a binary')
                    # find a plain file copy
                    _src_files = find_and_translate(hash_map, [inpath])
                res.update(_src_files)
    return sorted(res)


def main():
    args = create_argparser()
    for file in get_sources(args.sourcedir, args.binaries, args.debugpaths):
        print(file)


if __name__ == '__main__':
    main()
