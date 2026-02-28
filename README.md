# PDF N-Up

A CLI tool to combine multiple PDF pages into a single page (n-up format).

## Features

- Combine multiple pages into one sheet (2-up, 4-up, 9-up, etc.)
- Support for portrait and landscape orientations
- Configurable output file

## Installation

### Quick Install (macOS/Linux/Windows)

```bash
pipx install git+https://github.com/hemanthsingh003/pdf-nup.git
```

### Requirements

- Python 3.10 or higher
- [pipx](https://pipx.pypa.io/) (install via: `python -m pip install pipx`)

### Uninstall

```bash
pipx uninstall pdf-nup
```

## Usage

```bash
pdf-nup <input.pdf> [-n N] [-o output.pdf] [--landscape] [-v]
```

### Arguments

| Argument | Description |
|----------|-------------|
| `input` | Input PDF file |
| `-n, --pages-per-sheet` | Number of pages to combine into one (default: 4) |
| `-o, --output` | Output PDF file (default: input_nup.pdf) |
| `--landscape` | Use landscape orientation for output pages |
| `-v, --verbose` | Show detailed progress information |

### Examples

Default 4-up format:
```bash
pdf-nup input.pdf
```

2-up format (2 pages per sheet):
```bash
pdf-nup input.pdf -n 2
```

9-up format in landscape:
```bash
pdf-nup input.pdf -n 9 --landscape
```

Custom output with verbose output:
```bash
pdf-nup input.pdf -o output.pdf -v
```

## Project Structure

```
pdf-nup/
├── pyproject.toml          # Project metadata and dependencies
├── README.md               # This file
└── src/
    └── pdf_nup/
        ├── __init__.py     # Package entry point
        ├── cli.py          # CLI logic
        └── nup.py          # Core functionality
```

## License

MIT License
