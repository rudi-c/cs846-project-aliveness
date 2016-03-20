#!/usr/bin/python

# Computes all features on the dataset
# Prints out a Weka ARFF file and generates a bunch of plots

import argparse
import math
import os
import random
import sys

import matplotlib.pyplot as plt
import numpy as np

from analysis_tools import *
from statsmodels.nonparametric.smoothers_lowess import lowess

import feature_functions

BACKTESTING_DAYS = 30
PLOTS_DIR = "plots/"

def more_than_one_contributor(revisions):
    author = revisions[0].author
    for revision in revisions:
        if revision.author != author:
            return True
    return False

def compute_feature_vectors(db_connection, feature_functions_list, args):

    projects = get_projects(db_connection)

    feature_vector = []
    label_vector = []

    skipped_counts_empty = 0
    skipped_counts_single = 0
    skipped_counts_short = 0

    for i, project in enumerate(projects):
        revisions = get_revisions_for_project(db_connection, project.id)
        revisions = get_revisions_before_cutoff(revisions, DATA_END_DATE)

        if len(revisions) == 0:
            if not args.full:
                debug("Skipping (no commits)", str(i), project.name)
            skipped_counts_empty += 1
            continue
        if args.multionly and not more_than_one_contributor(revisions):
            if not args.full:
                debug("Skipping (single-owner)", str(i), project.name)
            skipped_counts_single += 1
            continue
        if (revisions[-1].date - revisions[0].date).days < args.mindays:
            if not args.full:
                debug("Skipping (less than min days)", str(i), project.name)
            skipped_counts_short += 1
            continue

        if not args.full:
            debug("Processing", str(i), project.name)

        backtest_cutoff_date = DATA_END_DATE

        # Keep backtesting further back in time until there's no more revision
        # history.
        while True:
            # Backtesting
            backtest_cutoff_date = backtest_cutoff_date - timedelta(days=BACKTESTING_DAYS)

            # Our full dataset is really large, we can afford to drop a large
            # portion of the rows.
            if args.full and random.random() > 0.1:
                continue

            backtest_revision_history = get_revisions_before_cutoff(revisions, backtest_cutoff_date)
            backtest_revision_future = get_revisions_after_cutoff(revisions, backtest_cutoff_date)

            # No history to look at!
            if len(backtest_revision_history) == 0:
                break

            # Even if the full revision history has more than one contributor,
            # it might not hold when backtesting.
            if args.multionly and not more_than_one_contributor(backtest_revision_history):
                break
            if (backtest_revision_history[-1].date - backtest_revision_history[0].date).days < args.mindays:
                break

            # Features
            feature_calculator = feature_functions.FeaturesFunctions(
                project, backtest_revision_history, backtest_cutoff_date)
            features = [feature_function(feature_calculator)
                        for feature_function in feature_functions_list]
            feature_vector.append(features)

            # Label
            alive = len(backtest_revision_future) > 0
            label_vector.append(alive)

            # in the case of no backtesting
            if args.nobt:
                break

        if i % 100 == 0 and args.full:
            # Using a carriage return allows the terminal to override
            # the previous line, making it more like a progress effect.
            print >> sys.stderr, ("%d percent of projects processed\r" %
                                   int(float(i) / len(projects) * 100)),

    debug("Skipped %d/%d projects for having no revisions"
          % (skipped_counts_empty, len(projects)))
    if args.multionly:
        debug("Skipped %d/%d projects for having being a single-owner repository"
              % (skipped_counts_single, len(projects)))
    if args.mindays > 0:
        debug("Skipped %d/%d projects for having being alive less "
              "than the minimum number of days"
              % (skipped_counts_short, len(projects)))
    debug("Skipped a total of %d/%d projects" %
          (skipped_counts_empty + skipped_counts_single + skipped_counts_short,
          len(projects)))

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

def plot_all(features_by_name, labels):
    if not os.path.exists(PLOTS_DIR):
        os.makedirs(PLOTS_DIR)

    for feature_name, feature_column in features_by_name:
        debug("Plotting %s - range [%f, %f]"
              % (feature_name, min(feature_column), max(feature_column)))
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

def output_arff(feature_names, features, labels):
    # Print header
    print "@relation aliveness"
    print ""

    # Attributes/feature vector columns
    for feature_name in feature_names:
        print "@attribute " + feature_name + " numeric"

    # Label attribute
    print "@attribute alive {alive, dead}"

    print ""
    print "@data"
    for feature_vector, label in zip(features, labels):
        print ",".join(str(feature) for feature in feature_vector),
        if label:
            print "alive"
        else:
            print "dead"

def balance_data(features, labels):
    alive_count = labels.count(True)
    dead_count = labels.count(False)
    debug("    %d alive" % alive_count)
    debug("    %d dead" % dead_count)

    to_remove = abs(dead_count - alive_count)
    if alive_count > dead_count:
        debug("Dropping %d alive feature vector rows" % to_remove)
    else:
        debug("Dropping %d dead feature vector rows" % to_remove)

    # Random undersampling
    to_remove_indices = set(random.sample(xrange(max(alive_count, dead_count)),
                                          to_remove))

    features_out = []
    labels_out = []
    alive_index = 0
    dead_index = 0
    for (feature_vector, label) in zip(features, labels):
        if label:
            # Keep all alive rows.
            if alive_count <= dead_count or alive_index not in to_remove_indices:
                features_out.append(feature_vector)
                labels_out.append(label)
            alive_index += 1
        else:
            # If dead
            if dead_count <= alive_count or dead_index not in to_remove_indices:
                features_out.append(feature_vector)
                labels_out.append(label)
            # Keep track of how many dead rows we've seen so far.
            dead_index += 1

    alive_count = labels_out.count(True)
    dead_count = labels_out.count(False)
    assert alive_count == dead_count

    return features_out, labels_out


def main():
    # Command-line arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument('--full', action="store_true")
    parser.add_argument('--nobt', action="store_true")
    # Look at multi-owner repositories only.
    parser.add_argument('--multionly', action="store_true")
    # Look at projects that have lasted more than 5 days only
    parser.add_argument('--mindays', type=int, default=0)
    args = parser.parse_args()

    db_connection = open_db(args.full)

    projects = get_projects(db_connection)

    feature_functions_list = feature_functions.feature_functions()
    feature_names = [f.__name__ for f in feature_functions_list]

    features, labels = compute_feature_vectors(db_connection,
                        feature_functions_list, args)

    debug("Got %d feature vectors" % len(features))

    # It is much prefered to have the same number of positive and negative samples.
    # Otherwise, it's easy to get 98% accuracy if the data is 98:2...
    features, labels = balance_data(features, labels)

    # Transpose the feature vector list to index by
    # feature (column) rather than row.
    features_as_columns = zip(*features)

    features_by_name = [(name, feature)
                        for name, feature
                        in zip(feature_names, features_as_columns)]
    plot_all(features_by_name, labels)
    output_arff(feature_names, features, labels)


if __name__ == "__main__":
    main()
