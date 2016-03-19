#!/usr/bin/python

# Misc data analysis

import argparse
import math
import os
import sys

import matplotlib.pyplot as plt
import numpy as np

from analysis_tools import *


def time_since_last_commit_distribution(db_connection):
    print """Distribution of projects according to time of last commit in
          days before cutoff date"""
    projects = get_projects(db_connection)

    print "Total number of projects: %d" % len(projects)

    days_before_cutoff = []
    for i, project in enumerate(projects):
        revisions = get_revisions_for_project(db_connection, project.id)
        revisions = get_revisions_before_cutoff(revisions, DATA_END_DATE)

        # Make sure we have revisions at all
        if len(revisions) > 0:
            last_date = revisions[-1].date
            assert last_date < DATA_END_DATE
            difference = (DATA_END_DATE - last_date).days
            days_before_cutoff.append(difference)

        if i % 100 == 0:
            # Using a carriage return allows the terminal to override
            # the previous line, making it more like a progress effect.
            print ("%d percent of projects processed\r" %
                   int(float(i) / len(projects) * 100)),

    print "Finished"

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
