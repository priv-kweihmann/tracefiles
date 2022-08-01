# tracefiles

A utility to find used sources from a binary using DWARF info

## Usage

```text
usage: tracefiles [-h] [--debugpaths DEBUGPATHS [DEBUGPATHS ...]] binary sourcedir

A utility to find used sources from a binary

positional arguments:
  binary                The binary to inspect
  sourcedir             Directory with the source code

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
