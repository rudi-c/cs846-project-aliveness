#!/usr/bin/python

# Find forks among projects.

import argparse
import math
import os
import sys

from analysis_tools import *
from collections import Counter

TEMP_DIR = "temp/"

def find_forks(db_connection):
    projects = get_projects(db_connection)

    projects_by_first_revision = {}

    for i, project in enumerate(projects):
        revisions = get_revisions_for_project(db_connection, project.id)
        if len(revisions) > 0:
            first_revision = revisions[0].id
            if first_revision in projects_by_first_revision:
                projects_by_first_revision[first_revision].append((project.name, len(revisions)))
            else:
                projects_by_first_revision[first_revision] = [(project.name, len(revisions))]

        if i % 100 == 0:
            # Using a carriage return allows the terminal to override
            # the previous line, making it more like a progress effect.
            print ("%d percent of projects processed\r" %
                   int(float(i) / len(projects) * 100)),

    # We don't need items that don't have duplicates.
    duplicates = { commit_hash: projects
                   for commit_hash, projects
                   in projects_by_first_revision.iteritems()
                   if len(projects) > 1 }

    return duplicates

def main():
    # Command-line arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument('--full', action="store_true")
    args = parser.parse_args()

    if not args.full:
        print "Note: you should probably use --full"
        print "A small data sample is less likely to have duplicates"

    db_connection = open_db(args.full)

    # { revision_id: [(project name, revision count), ...], ... }
    projects_by_first_revision = find_forks(db_connection)

    if len(projects_by_first_revision) > 0:

        if not os.path.exists(TEMP_DIR):
            os.makedirs(TEMP_DIR)

        # Group these by number of duplicates.
        # { count: [(revision_id, [(project name, revision count), ...]), ...], ... }
        grouped = {}
        for revision_id, project_list in projects_by_first_revision.iteritems():
            count = len(project_list)
            if count in grouped:
                grouped[count].append((revision_id, project_list))
            else:
                grouped[count] = [(revision_id, project_list)]

        for count in sorted(grouped.keys()):
            # Write to a file groups of duplicate projects.
            # Use one file per number of duplicate projects in a group.
            with open(TEMP_DIR + "forks_" + str(count), 'w') as f:
                for revision_id, project_list in grouped[count]:
                    f.write("Projects starting with revision " + revision_id + "\n")
                    for project_name, revision_count in project_list:
                        f.write(project_name + " " + str(revision_count) + "\n")
                    f.write("\n")
            print "There are %d projects with %d copies." % (len(grouped[count]), count)
    else:
        print "No duplicates."

if __name__ == "__main__":
    main()
