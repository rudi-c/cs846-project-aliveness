#!/usr/bin/python

# Computes all features on the dataset
# Outputs a json file

import argparse
import json
import math
import random
import sys

from analysis_tools import *

import feature_functions

BACKTESTING_DAYS = 30

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
    parser.add_argument('--out', type=str, required=True)
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

    data = { "feature_names": feature_names, "features": features, "labels": labels }
    with open(args.out, 'w') as f:
        json.dump(data, f)


if __name__ == "__main__":
    main()
