#!/usr/bin/python

import argparse
import math
import sys

from analysis_tools import *

def time_since_last_commit_distribution(db_connection):
    print """Distribution of projects according to time of last commit in
          days before cutoff date"""
    projects = get_projects(db_connection)

    days_before_cutoff = []
    for project in projects:
        revisions = get_revisions_for_project(db_connection, project.id)

        # Make sure we have revisions at all
        if len(revisions) > 0:
            last_date = revisions[-1].date
            if last_date < CUTOFF_DATE:
                difference = (CUTOFF_DATE - last_date).days
                days_before_cutoff.append(difference)
    bins = log_bin(days_before_cutoff)
    for (start, end), count in bins:
        print ("[%d, %d]:" % (start, end)).ljust(16) + str(count)


def main():
    # Command-line arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument('--full', action="store_true")
    args = parser.parse_args()

    db_connection = open_db(args.full)

    projects = get_projects(db_connection)

    # Keep only projects
    # Print a few projects
    for i in range(0, 10):
        print projects[i]

    # Example, print the founder of project 10267115
    revisions = get_revisions_for_project(db_connection, 10267115)
    for rev in revisions:
        print rev
    print get_founder(revisions)

    time_since_last_commit_distribution(db_connection)


if __name__ == "__main__":
    main()
