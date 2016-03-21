#!/usr/bin/python

# Prints out a Weka ARFF file from a json file

import argparse
import json

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

    output_arff(feature_names, features, labels)

if __name__ == "__main__":
    main()
