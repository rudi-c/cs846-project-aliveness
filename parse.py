#!/usr/bin/python

import math
import os
import re
import sqlite3
import sys

def parse_projects(c):
    """
    Expect lines of the format:
    o[project id] = name|revision count|has docs

    (Output of project-repository.boa)
    """
    with open("projects-small.txt") as f:
        for line in f.readlines():
            matches = re.match(r'o\[(.*)\] = (.*)\|(.*)|(.*)', line)
            project_id = int(matches.group(1))
            name = matches.group(2)
            rev_count = int(matches.group(3))
            has_docs = bool(matches.group(4))

            fields = ",".join('"' + str(v) + '"'
                              for v in (project_id, name, rev_count, has_docs))
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

def parse_span():
    """
    Except lines of the format:
    counts[span] = #

    (Output of activity-span.boa)
    """
    print "Project lifespans in days"

    results = []
    with open("activity-span.txt") as f:
        for line in f.readlines():
            matches = re.match(r'counts\[(.*)\] = (.*)', line)
            span = int(matches.group(1))
            count = int(matches.group(2))
            results.append((span, count))

    log_bins = {}
    invalid_count = 0
    for span, count in results:
        if span < 0:
            invalid_count = count
        else:
            index = int(math.log(span + 1, 2))
            if index in log_bins:
                log_bins[index] += count
            else:
                log_bins[index] = count
    print "Invalid (no commits?): %d" % invalid_count

    non_log_bins = []
    for index, count in log_bins.iteritems():
        non_log_bins.append((int(pow(2.0, index)) - 1, count))
    non_log_bins = sorted(non_log_bins)
    for start, count in non_log_bins:
        print ("[%d, %d]: " % (start, start * 2)).ljust(16) + str(count)


def main(args):
    os.remove('repos.db')

    conn = sqlite3.connect('repos.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE repos
                 (id, name, revision_count, has_docs)''')
    c.execute('''CREATE TABLE revisions
                 (id, project, date, author)''')

    parse_span()
    parse_projects(c)
    parse_revisions(c)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    main(sys.argv[1:])
