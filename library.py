import argparse
import json
import os
import shutil
import sqlite3
import sys
import webbrowser

DB_PATH = 'library.db'
PAPERS_DIR = 'papers'


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS papers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    authors TEXT NOT NULL,
                    year INTEGER NOT NULL,
                    filename TEXT NOT NULL
                )''')
    conn.commit()
    conn.close()


def add_paper(args):
    src = args.file
    if not os.path.isfile(src):
        print(f'File not found: {src}')
        return
    os.makedirs(PAPERS_DIR, exist_ok=True)
    # create unique filename
    base = os.path.basename(src)
    dest = os.path.join(PAPERS_DIR, base)
    counter = 1
    name, ext = os.path.splitext(base)
    while os.path.exists(dest):
        dest = os.path.join(PAPERS_DIR, f"{name}_{counter}{ext}")
        counter += 1
    shutil.copy2(src, dest)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO papers (title, authors, year, filename) VALUES (?,?,?,?)',
              (args.title, args.authors, args.year, dest))
    conn.commit()
    conn.close()
    print('Paper added.')


def list_papers(args):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for row in c.execute('SELECT id, title, authors, year FROM papers'):
        print(f"{row[0]}: {row[1]} ({row[3]}) - {row[2]}")
    conn.close()


def view_paper(args):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT filename FROM papers WHERE id=?', (args.id,))
    row = c.fetchone()
    conn.close()
    if row:
        path = os.path.abspath(row[0])
        webbrowser.open(f'file://{path}')
    else:
        print('Paper not found.')


def cite_paper(args):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT authors, year, title FROM papers WHERE id=?', (args.id,))
    row = c.fetchone()
    conn.close()
    if row:
        authors, year, title = row
        citation = f"{authors} ({year}) {title}."
        print(citation)
    else:
        print('Paper not found.')


def main():
    parser = argparse.ArgumentParser(description='Local research paper library')
    subparsers = parser.add_subparsers(dest='command')

    add = subparsers.add_parser('add', help='Add a PDF to the library')
    add.add_argument('file', help='Path to PDF file')
    add.add_argument('--title', required=True, help='Title of the paper')
    add.add_argument('--authors', required=True, help='Authors of the paper')
    add.add_argument('--year', type=int, required=True, help='Publication year')
    add.set_defaults(func=add_paper)

    list_p = subparsers.add_parser('list', help='List papers')
    list_p.set_defaults(func=list_papers)

    view = subparsers.add_parser('view', help='Open a paper')
    view.add_argument('id', type=int, help='ID of the paper')
    view.set_defaults(func=view_paper)

    cite = subparsers.add_parser('cite', help='Generate citation')
    cite.add_argument('id', type=int, help='ID of the paper')
    cite.set_defaults(func=cite_paper)

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(1)

    init_db()
    args.func(args)


if __name__ == '__main__':
    main()
