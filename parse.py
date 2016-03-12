#!/usr/bin/python

import os
import re
import sqlite3
import sys

def parse_revision_dates(c):
    """
    Expect lines of the format:
    o[project id][revision hash] = date

    (Output of revisions.boa)
    """
    with open("revisions-small.txt") as f:
        for line in f.readlines():
            matches = re.match(r'o\[(.*)\]\[(.*)\] = (.*)\|(.*)', line)
            project_id = int(matches.group(1))
            revision_hash = matches.group(2)
            date = matches.group(3)
            author = matches.group(4)

            fields = ",".join('"' + str(v) + '"'
                              for v in (revision_hash, project_id, date, author))
            c.execute("INSERT INTO revisions VALUES (%s)" % fields)

def main(args):
    os.remove('repos.db')

    conn = sqlite3.connect('repos.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE repos
                 (id)''')
    c.execute('''CREATE TABLE revisions
                 (id, project, date, author)''')

    parse_revision_dates(c)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    main(sys.argv[1:])
