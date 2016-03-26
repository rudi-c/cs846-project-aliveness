#!/usr/bin/python

# Misc data analysis

import argparse
import math
import os
import sys

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

def project_lifespan_distribution(db_connection):
    print """Distribution of projects according to time between first and
          last commit in days before"""
    projects = get_projects(db_connection)

    print "Total number of projects: %d" % len(projects)

    length_days = []
    for i, project in enumerate(projects):
        revisions = get_revisions_for_project(db_connection, project.id)
        revisions = get_revisions_before_cutoff(revisions, DATA_END_DATE)

        # Make sure we have revisions at all
        if len(revisions) > 0:
            length_days.append((revisions[-1].date - revisions[0].date).days)

        if i % 100 == 0:
            # Using a carriage return allows the terminal to override
            # the previous line, making it more like a progress effect.
            print ("%d percent of projects processed\r" %
                   int(float(i) / len(projects) * 100)),

    print "Finished"

    bins = log_bin(length_days)
    for (start, end), count in bins:
        print ("[%d, %d]:" % (start, end)).ljust(16) + str(count)

def documentation_count(db_connection, days):
    print """Likelihood of project being alive on cutoff date per documentation
          file type."""
    print "Here, alive => %d days since last revision" % days
    projects = get_projects(db_connection)

    readme_alive = 0
    readme_total = 0
    license_alive = 0
    license_total = 0
    todo_alive = 0
    todo_total = 0
    install_alive = 0
    install_total = 0
    contributing_alive = 0
    contributing_total = 0
    changelog_alive = 0
    changelog_total = 0
    at_least_one_alive = 0
    at_least_one_total = 0
    at_least_two_alive = 0
    at_least_two_total = 0

    total_projects = 0
    alive_projects = 0

    for i, project in enumerate(projects):
        revisions = get_revisions_for_project(db_connection, project.id)
        revisions = get_revisions_before_cutoff(revisions, DATA_END_DATE)

        # Make sure we have revisions at all
        if len(revisions) > 0:
            alive = (DATA_END_DATE - revisions[-1].date).days <= days
            different_docs = 0

            total_projects += 1
            if alive:
                alive_projects += 1

            if project.docs_readme:
                different_docs += 1
                readme_total += 1
                if alive:
                    readme_alive += 1

            if project.docs_license:
                different_docs += 1
                license_total += 1
                if alive:
                    license_alive += 1

            if project.docs_todo:
                different_docs += 1
                todo_total += 1
                if alive:
                    todo_alive += 1

            if project.docs_install:
                different_docs += 1
                install_total += 1
                if alive:
                    install_alive += 1

            if project.docs_contributing:
                different_docs += 1
                contributing_total += 1
                if alive:
                    contributing_alive += 1

            if project.docs_changelog:
                different_docs += 1
                changelog_total += 1
                if alive:
                    changelog_alive += 1

            if different_docs > 0:
                at_least_one_total += 1
                if alive:
                    at_least_one_alive += 1

            if different_docs > 1:
                at_least_one_total += 1
                if alive:
                    at_least_one_alive += 1

    def stuff(alive, total):
        if total > 0:
            return (alive, total, float(alive) / total * 100)
        else:
            return (alive, total, 0)

    print "All projects: (%d/%d), %.3f" % stuff(alive_projects, total_projects)
    print "readme: (%d/%d), %.3f" % stuff(readme_alive, readme_total)
    print "license: (%d/%d), %.3f" % stuff(license_alive, license_total)
    print "todo: (%d/%d), %.3f" % stuff(todo_alive, todo_total)
    print "install: (%d/%d), %.3f" % stuff(install_alive, install_total)
    print "contributing: (%d/%d), %.3f" % stuff(contributing_alive, contributing_total)
    print "changelog: (%d/%d), %.3f" % stuff(changelog_alive, changelog_total)
    print "at_least_one: (%d/%d), %.3f" % stuff(at_least_one_alive, at_least_one_total)
    print "at_least_two: (%d/%d), %.3f" % stuff(at_least_two_alive, at_least_two_total)

def main():
    # Command-line arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument('--full', action="store_true")
    args = parser.parse_args()

    db_connection = open_db(args.full)

    projects = get_projects(db_connection)

    documentation_count(db_connection, 7)
    documentation_count(db_connection, 30)
    time_since_last_commit_distribution(db_connection)
    project_lifespan_distribution(db_connection)

if __name__ == "__main__":
    main()
