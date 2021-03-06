#!/usr/bin/python

import argparse
import math
import os
import re
import sqlite3
import sys

from datetime import datetime

def parse_projects(cursor, filename):
    """
    Expect lines of the format:
    o[project id] = name|revision count|has docs

    (Output of project-repository.boa)
    """
    if not os.path.isfile(filename):
        raise Exception("Expected file %s" % filename)

    print "Parsing projects..."

    with open(filename) as f:
        for i, line in enumerate(f):
            matches = re.match(r'o\[(.*)\] = (.*)\|(.*)\|(.*)\|(.*)\|(.*)\|(.*)', line)
            project_id = int(matches.group(1))
            name = matches.group(2)
            rev_count = int(matches.group(3))
            docs = int(matches.group(4))
            created_date = matches.group(5)
            descr_size = int(matches.group(6))
            num_languages = int(matches.group(7))
            is_original = True # we don't know otherwise yet, need to run fork detection script

            data = (project_id, is_original, name, rev_count, docs,
                    created_date, descr_size, num_languages)

            try:
                cursor.execute("INSERT INTO repos (id, is_original, name, revision_count, "
                               "docs, created_date, descr_size, num_languages) "
                               "VALUES (?, ?, ?, ?, ?, ?, ?, ?)", data)
            except Exception as e:
                print data
                raise e

            if i % 100 == 0:
                # Using a carriage return allows the terminal to override
                # the previous line, making it more like a progress effect.
                print "%d lines read\r" % i,

    print ""

def parse_revisions(cursor, filename):
    """
    Expect lines of the format:
    o[project id][revision hash] = date|author

    (Output of revisions.boa)
    """
    if not os.path.isfile(filename):
        raise Exception("Expected file %s" % filename)

    print "Parsing revisions..."

    with open(filename) as f:
        for i, line in enumerate(f):
            # Warning: author names can have vertical |, could screw up parsing
            # if not careful!
            matches = re.match(r'o\[(.*)\]\[(.*)\] = ([^\|]*)\|(.*)', line)
            project_id = int(matches.group(1))
            revision_hash = matches.group(2)
            date = matches.group(3)
            author = matches.group(4)

            # Make sure we can parse the date.
            try:
                datetime.strptime(date, "%d/%m/%y %H:%M:%S")
            except ValueError:
                print "Problem reading : " + line
                raise Exception()

            data = (revision_hash, project_id, date, author)
            try:
                cursor.execute("INSERT INTO revisions VALUES (?, ?, ?, ?)", data)
            except Exception as e:
                print data
                raise e

            if i % 100 == 0:
                # Using a carriage return allows the terminal to override
                # the previous line, making it more like a progress effect.
                print "%d lines read\r" % i,

    print ""

def parse_span(filename):
    """
    Except lines of the format:
    counts[span] = #

    (Output of activity-span.boa)
    """
    if not os.path.isfile(filename):
        raise Exception("Expected file %s" % filename)

    print "Project lifespans in days"

    results = []
    with open(filename) as f:
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


def main():
    # Command-line arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument('--full', action="store_true")
    args = parser.parse_args()

    if args.full:
        database_name = "repos.db"
    else:
        database_name = "repos_test.db"

    # Recreate from scratch.
    try:
        os.remove(database_name)
    except OSError:
        pass

    conn = sqlite3.connect(database_name)
    conn.text_factory = str     # easiest way to deal with encodings right now
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE repos
                      (id, is_original, name, revision_count, docs,
                       created_date, descr_size, num_languages)''')
    cursor.execute('''CREATE TABLE revisions
                      (id, project, date, author)''')

    parse_span("activity-span.txt")
    if args.full:
        parse_projects(cursor, "projects.txt")
        parse_revisions(cursor, "revisions.txt")
    else:
        parse_projects(cursor, "projects-small.txt")
        parse_revisions(cursor, "revisions-small.txt")

    # Need to create index to select rows based on project id.
    # Otherwise it would read the whole table everytime we query revisions
    # for a project.
    cursor.execute('''CREATE INDEX rev_project_index ON revisions (project)''')

    # Sometimes useful to index by project name, should be unique.
    cursor.execute('''CREATE INDEX project_name_index ON repos (name)''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()
