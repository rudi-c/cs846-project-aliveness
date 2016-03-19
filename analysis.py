#!/usr/bin/python

import argparse
import math
import os
import sys

import matplotlib.pyplot as plt
import numpy as np

from analysis_tools import *
#from lowess import lowess
from statsmodels.nonparametric.smoothers_lowess import lowess

import feature_functions

BACKTESTING_DAYS = 30
PLOTS_DIR = "plots/"

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

    skipped_counts = 0

    for i, project in enumerate(projects):
        revisions = get_revisions_for_project(db_connection, project.id)
        revisions = get_revisions_before_cutoff(revisions, DATA_END_DATE)

        if len(revisions) > 0:
            print "Processing", str(i), project.name
        else:
            print "Skipping", str(i), project.name
            skipped_counts += 1
            continue

        backtest_cutoff_date = DATA_END_DATE

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

    print "Skipped %d/%d projects for having no revisions" % (skipped_counts, len(projects))

    return feature_vector, label_vector

def plot_binary_vs_continuous(name, continuous, binary, log):
    points_in_order = sorted(zip(continuous, binary))
    average_points = []
    chunk_size = len(points_in_order) / 10
    for i in xrange(0, len(points_in_order), chunk_size):
        chunk_continuous, chunk_binary = zip(*points_in_order[i:i+chunk_size])
        density = float(sum(chunk_binary)) / chunk_size
        average_points.append((min(chunk_continuous), density))
        average_points.append((max(chunk_continuous), density))

    # Begin new plot (needed since plt is stateful)
    fig = plt.figure()
    # Plot data points with some jittering to see the overlapping ones
    plt.plot(continuous, binary, 'ro', alpha=0.05)
    # Locally weighted scatterplot smoothing
    try:
        xs, ys = zip(*average_points)
        #yest = lowess(ys, xs, frac=0.04, return_sorted=False)
        plt.plot(xs, ys)
    except:
        pass
    # Plot slighly above 1.0 to see things better.
    plt.ylim(-0.1, 1.1)

    if log:
        plt.xscale('log')
        # Save to file
        plt.savefig(PLOTS_DIR + "_log_" + name + ".png")
    else:
        # Save to file
        plt.savefig(PLOTS_DIR + name + ".png")
    plt.close(fig)

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
    feature_names = [f.__name__ for f in feature_functions_array]

    features, labels = compute_feature_vectors(db_connection,
                        feature_functions_array, args.nobt)

    print "Got %d feature vectors" % len(features)

    # Transpose the feature vector list to index by
    # feature (column) rather than row.
    features_as_columns = zip(*features)

    features_by_name = {name: feature for name, feature in zip(feature_names, features_as_columns)}

    if not os.path.exists(PLOTS_DIR):
        os.makedirs(PLOTS_DIR)

    for feature_name, feature_column in features_by_name.items():
        print "Plotting %s - range [%f, %f]" % (feature_name, min(feature_column), max(feature_column))
        feature_range = max(feature_column) - min(feature_column)
        features_jitter = (np.random.rand(len(labels)) - 0.5) * feature_range / 100
        jittered_features = np.array(feature_column) + features_jitter
        jittered_labels = np.array(labels) + (np.random.rand(len(labels)) - 0.5) * 0.05

        plot_binary_vs_continuous(feature_name, jittered_features, jittered_labels, False)

        # Not point in doing a log plot for data in [0, 1]
        if max(feature_column) > 1:
            # It's common to plot log(x + 1) to deal with x = 0
            adjusted_features = jittered_features + np.ones(len(jittered_features))
            plot_binary_vs_continuous(feature_name, adjusted_features, jittered_labels, True)


if __name__ == "__main__":
    main()
