## Setup

Before using the tool, create a virtual environment and install the required packages:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

# no-link-pdf - PDF Link Remover

A simple tool to remove all links from PDF files.

## Usage

```bash
python3 main.py input output [options]
python3 main.py --dir input_directory output_directory [options]
```

### Positional Arguments

- `input`  
    Path to the input PDF file or directory.

- `output`  
    Path to the output PDF file or directory.

### Options

- `-h`, `--help`  
    Show help message and exit.

- `--dir`  
    Process all PDFs in a directory.

- `-v`, `--verbose`  
    Enable verbose output.

## Example

Remove links from a single PDF:

```bash
python3 main.py input.pdf output.pdf
```

Remove links from all PDFs in a directory:

```bash
python3 main.py --dir input_dir output_dir
```