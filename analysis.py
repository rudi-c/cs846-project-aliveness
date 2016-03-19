#!/usr/bin/python

import argparse
import math
import sys

import matplotlib.pyplot as plt

from analysis_tools import *
import feature_functions

BACKTESTING_DAYS = 30


def time_since_last_commit_distribution(db_connection):
    print """Distribution of projects according to time of last commit in
          days before cutoff date"""
    projects = get_projects(db_connection)

    print "Total number of projects: %d" % len(projects)

    days_before_cutoff = []
    for i, project in enumerate(projects):
        revisions = get_revisions_for_project(db_connection, project.id)
        revisions = get_revisions_before_cutoff(revisions, CUTOFF_DATE)

        # Make sure we have revisions at all
        if len(revisions) > 0:
            last_date = revisions[-1].date
            assert last_date < CUTOFF_DATE
            difference = (CUTOFF_DATE - last_date).days
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

def compute_feature_vectors(db_connection, feature_functions, nobt):

    projects = get_projects(db_connection)

    feature_vector = []
    label_vector = []

    for i, project in enumerate(projects):

        print "Processing", str(i), project.name

        revisions = get_revisions_for_project(db_connection, project.id)
        #revisions = get_revisions_before_cutoff(revisions, CUTOFF_DATE)

        backtest_cutoff_date = CUTOFF_DATE

        # Keep backtesting further back in time until there's no more revision
        # history.
        while True:
            # Backtesting
            backtest_cutoff_date = backtest_cutoff_date - timedelta(days=BACKTESTING_DAYS)

            backtest_revision_history = get_revisions_before_cutoff(revisions, backtest_cutoff_date)
            backtest_revision_future = get_revisions_after_cutoff(revisions, backtest_cutoff_date)

            if len(backtest_revision_history) == 0:
                break

            # Features
            features = [feature_function(project, backtest_revision_history, backtest_cutoff_date)
                        for feature_function in feature_functions]
            feature_vector.append(features)


            # Label
            alive = len(backtest_revision_future) > 0
            label_vector.append(alive)


            # in the case of no backtesting
            if nobt:
                break

    return feature_vector, label_vector

def main():
    # Command-line arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument('--full', action="store_true")
    parser.add_argument('--nobt', action="store_true")
    args = parser.parse_args()

    db_connection = open_db(args.full)

    projects = get_projects(db_connection)

    # Keep only projects
    # Print a few projects
    #for i in range(0, 10):
    #    print projects[i]

    # Example, print the founder of project 10267115
    #revisions = get_revisions_for_project(db_connection, 10267115)
    #for rev in revisions:
    #    print rev
    #print get_founder(revisions)

    #time_since_last_commit_distribution(db_connection)

    # Obtains each feature function for some reason, the values come
    # in the alphabetical order according to the name of the function
    feature_functions_array = [getattr(feature_functions, feature_function)
                               for feature_function in dir(feature_functions)
                               if callable(getattr(feature_functions, feature_function))]

    features, labels = compute_feature_vectors(db_connection,
                        feature_functions_array, args.nobt)

    features = zip(*features)

    plt.plot(features[0], labels, 'ro')
    #plot.plot(features, labels, 'ro')
    #plt.axis([0, 6, 0, 20])
    plt.show()


if __name__ == "__main__":
    main()
