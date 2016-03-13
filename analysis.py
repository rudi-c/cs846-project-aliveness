#!/usr/bin/python

import argparse
import sys

from analysis_tools import *

def main():
    # Command-line arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument('--full', action="store_true")
    args = parser.parse_args()

    db_connection = open_db(args.full)

    # Example, print the founder of project 10267115
    revisions = get_revisions_for_project(db_connection, 10267115)
    for rev in revisions:
        print rev
    print get_founder(revisions)


if __name__ == "__main__":
    main()
