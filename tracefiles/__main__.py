# SPDX-FileCopyrightText: 2022 Konrad Weihmann
# SPDX-License-Identifier: BSD-2-Clause

import argparse
import glob
import logging
import os
import subprocess
from typing import List
from typing import Set


def create_argparser():
    parser = argparse.ArgumentParser(prog='tracefiles',
                                     description='A utility to find used sources from a binary')
    parser.add_argument('--debugpaths', nargs='+', default=[], action='extend',
                        help='Potential paths where to look for debug info')
    parser.add_argument('binary', help='The binary to inspect')
    parser.add_argument('sourcedir', help='Directory with the source code')
    return parser.parse_args()


def get_debug_paths(args: argparse.Namespace) -> List[str]:
    _cleaninpath = args.binary.lstrip('/')
    res = []
    for path in args.debugpaths:
        res.append(os.path.join(path, os.path.basename(_cleaninpath)))
    res.append(args.binary)
    return res


def find_and_translate(args: argparse.Namespace, sources: List[str]) -> Set[str]:
    result = set()
    for root, _, files in os.walk(args.sourcedir):
        for f in files:
            _fullpath = os.path.join(root, f)
            result.update([os.path.relpath(_fullpath, args.sourcedir)
                          for x in sources if _fullpath.endswith(x)])
    return result


def get_sources(args: argparse.Namespace) -> Set[str]:
    res = set()
    for inpath in get_debug_paths(args):
        logging.info(f'Analyzing {inpath}')
        if os.path.exists(inpath):
            _src_files = []
            _cmdline = f'readelf -wi {inpath} | grep -B1 DW_AT_comp_dir | awk \'/DW_AT_name/{{name = $NF; getline; print name}}\''
            try:
                _src_files = subprocess.check_output(_cmdline,
                                                        universal_newlines=True,
                                                        shell=True,  # noqa: S602
                                                        stderr=subprocess.DEVNULL)
            except:
                _src_files = []
            _src_files = [x.replace('../', '')
                          for x in _src_files.split('\n') if x]
            _cmdline = f'readelf -w {inpath} | grep "indirect line string, offset"'
            try:
                _src_files += [x.split(':')[-1].strip()
                                for x in subprocess.check_output(_cmdline,
                                                                universal_newlines=True,
                                                                shell=True,  # noqa: S602
                                                                stderr=subprocess.DEVNULL).split('\n')
                                if x]
            except:
                logging.warning("Problems getting full DWARF info")
            _src_files = [x.replace('../', '') for x in _src_files if x]
            res.update(find_and_translate(args, _src_files))
    return res


def main():
    args = create_argparser()
    for file in sorted(get_sources(args)):
        print(file)


if __name__ == '__main__':
    main()
