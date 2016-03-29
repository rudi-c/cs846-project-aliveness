#!/usr/bin/python

# Generates a bunch of plots from a json file

import argparse
import json
import os

import matplotlib.pyplot as plt
import numpy as np

from analysis_tools import *
from statsmodels.nonparametric.smoothers_lowess import lowess

PLOTS_DIR = "plots/"

def plot_binary_vs_continuous(name, boxplot_values, continuous, binary, log):
    points_in_order = sorted(zip(continuous, binary))
    average_points = []
    chunk_size = min(len(points_in_order) / 10, 200)
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

    # Add a boxplot
    plt.boxplot(boxplot_values, vert=False, positions=[0, 1])

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

    for feature_name, feature_column in features_by_name.iteritems():
        debug("Plotting %s - range [%f, %f]"
              % (feature_name, min(feature_column), max(feature_column)))
        feature_range = max(feature_column) - min(feature_column)
        features_jitter = (np.random.rand(len(labels)) - 0.5) * feature_range / 100
        jittered_features = np.array(feature_column) + features_jitter
        jittered_labels = np.array(labels) + (np.random.rand(len(labels)) - 0.5) * 0.05

        values_alive = [v for (v, label) in zip(feature_column, labels) if label]
        values_dead = [v for (v, label) in zip(feature_column, labels) if not label]

        plot_binary_vs_continuous(feature_name, [values_alive, values_dead],
                                  jittered_features, jittered_labels, False)

        # Not point in doing a log plot for data in [0, 1]
        if max(feature_column) > 1:
            # It's common to plot log(x + 1) to deal with x = 0
            adjusted_features = jittered_features + np.ones(len(jittered_features))
            plot_binary_vs_continuous(feature_name, [values_alive, values_dead],
                                      adjusted_features, jittered_labels, True)

def box_plot(title, feature_values, labels, log):
    print "Plotting " + title

    values_alive = [v for (v, label) in zip(feature_values, labels) if label]
    values_dead = [v for (v, label) in zip(feature_values, labels) if not label]

    print ("Alive: Median %f, Mean %f, stdev %f" %
           (np.median(values_alive), np.mean(values_alive), np.std(values_alive)))
    print ("Dead: Median %f, Mean %f, stdev %f" %
           (np.median(values_dead), np.mean(values_dead), np.std(values_dead)))

    if log:
        values_alive = [math.log10(value + 1) for value in values_alive]
        values_dead = [math.log10(value + 1) for value in values_dead]

    # Begin new plot (needed since plt is stateful)
    fig = plt.figure()

    ax = plt.subplot(1, 1, 1)

    plt.figure(figsize=(5,8))

    plt.title(title)

    # Add a boxplot
    plt.boxplot([values_alive, values_dead], vert=True, positions=[0, 1], widths=0.5)

    plt.xticks([0, 1], ["alive", "dead"])

    if log:
        plt.yticks([0, math.log10(2), 1, 2, 3, 4], [0, 1, 10, 100, 1000, 10000])
        plt.ylim(-0.1, 4.5)
    else:
        # Plot slighly above 1.0 to see things better.
        plt.ylim(-0.1, 1.1)

    # Save to file
    plt.savefig(PLOTS_DIR + "boxplot: " + title + ".png")
    plt.close(fig)

def main():
    # Command-line arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument("file", nargs=1)
    args = parser.parse_args()

    with open(args.file[0], 'r') as f:
        data = json.load(f)

    feature_names = data["feature_names"]
    features = data["features"]
    labels = data["labels"]

    # Transpose the feature vector list to index by
    # feature (column) rather than row.
    features_as_columns = zip(*features)

    features_by_name = {name: feature
                        for name, feature
                        in zip(feature_names, features_as_columns)}

    box_plot("Date before last commit (log)",
             features_by_name["date_before_last_revision"], labels, True)
    box_plot("Date before last commit by founder (log)",
             features_by_name["date_before_last_revision_by_founder"], labels, True)
    box_plot("Percentage of founder commit",
             features_by_name["percentage_of_founder_revisions"], labels, False)

    plot_all(features_by_name, labels)

if __name__ == "__main__":
    main()
