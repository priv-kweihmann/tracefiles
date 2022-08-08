# tracefiles

A utility to find used sources from a binary using DWARF info and more

## Usage

```text
usage: tracefiles [-h] [--debugpaths DEBUGPATHS [DEBUGPATHS ...]] sourcedir binaries [binaries ...]

A utility to find used sources from a binary

positional arguments:
  sourcedir             Directory with the source code
  binaries              The binaries to inspect

options:
  -h, --help            show this help message and exit
  --debugpaths DEBUGPATHS [DEBUGPATHS ...]
                        Potential paths where to look for debug info
```

## Output

Returns the found filenames to **stdout**

## Requirements

All you need is are following utilities installed

- `readelf`
- `awk`
- `grep`

and of course some debug symbols will come in handy ;-)

## License

This tool is licensed under `BSD-2-Clause`
