#!/usr/bin/python

import argparse
import os
import sys

TEMP_DIR = "temp/"

def main():
    # Command-line arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument('--full', action="store_true")
    parser.add_argument('--featureselect', action="store_true")
    parser.add_argument("file", nargs=1)
    args = parser.parse_args()

    classpath = "$CLASSPATH:/usr/share/java/weka.jar"

    features_file = args.file[0]
    filtered_file = TEMP_DIR + "filtered.arff"
    input_file = features_file

    if args.full:
        min_instances_per_leaf = 2000
    else:
        min_instances_per_leaf = 50

    if args.featureselect:
        print "Performing feature selection..."

        if not os.path.exists(TEMP_DIR):
            os.makedirs(TEMP_DIR)

        # See https://weka.wikispaces.com/Performing+attribute+selection
        os.system("java -cp " + classpath +
                  "    weka.filters.supervised.attribute.AttributeSelection"
                  "    -E \"weka.attributeSelection.CfsSubsetEval -M\""
                  "    -S \"weka.attributeSelection.BestFirst -D 1 -N 5\""
                  "    -b"
                  "    -i " + features_file +
                  "    -o " + filtered_file +
                  "    -r " + features_file +
                  "    -s " + filtered_file)
        input_file = filtered_file

    print "Classifying..."
    os.system("java -cp " + classpath +
              "    weka.classifiers.trees.J48"
              "    -t " + input_file +
              "    -C 0.25"
              "    -M " + str(min_instances_per_leaf))


if __name__ == "__main__":
    main()
