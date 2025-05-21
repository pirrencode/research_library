# Research Library

This repository provides a simple command line application for managing local PDF research papers. You can add papers, list them, view the stored PDFs and generate citations in Harvard format.

## Requirements

The application only uses Python standard library modules, so no additional dependencies are required.
A `requirements.txt` file is included for completeness.

## Usage

Initialize the database and run commands using `library.py`:

```bash
python library.py add /path/to/file.pdf --title "Paper Title" --authors "A. Author; B. Author" --year 2023
python library.py list
python library.py view 1
python library.py cite 1
```

PDF files are copied into the `papers/` directory and stored with metadata in `library.db`.
