#!/usr/bin/python

import os
import re
import sqlite3
import sys

def parse_projects(c):
    """
    Expect lines of the format:
    o[project id] = name|revision count

    (Output of project-repository.boa)
    """
    with open("projects-small.txt") as f:
        for line in f.readlines():
            matches = re.match(r'o\[(.*)\] = (.*)\|(.*)', line)
            project_id = int(matches.group(1))
            name = matches.group(2)
            rev_count = int(matches.group(3))

            fields = ",".join('"' + str(v) + '"'
                              for v in (project_id, name, rev_count))
            c.execute("INSERT INTO repos VALUES (%s)" % fields)


def parse_revisions(c):
    """
    Expect lines of the format:
    o[project id][revision hash] = date|author

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
                 (id, name, revision_count)''')
    c.execute('''CREATE TABLE revisions
                 (id, project, date, author)''')

    parse_projects(c)
    parse_revisions(c)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    main(sys.argv[1:])
