# How to use

## Installation

```
sudo apt-get install weka python-tk python-matplotlib python-scipy
sudo pip install statsmodel
```

## Parsing mined data

See `parse.py`

The idea is to get all the data we need from Boa as a textfile, then read it and store it into a local sqlite database. It will be easier to do queries on a sqlite database, especially memory and performance-wise.

To make a test run, use either `./parse.py` or `pypy parse.py` (faster). This will read the files `projects-small.txt`, `revisions-small.txt`, `activity-span.txt`. It will create the local database `repos_test.db`.

To make create the database for the full GitHub 2015 dataset, use the `--full` flag. The program will expect to see the files `projects.txt` and `revisions-small.txt`. See download links below. This make take a few minutes and create the local database `repos.db`.

It's useful to identify duplicate projects. To do so, run one of:

```
./forks.py [--full]
pypy forks.py [--full]
```

The script `./analysis.py` performs creates some miscellaneous stats from the data.

To use machine learning, first generate the feature file by running

```
./features.py [--full] [--nobt] [--multionly] [--mindays n] --out output.json
pypy features.py [--full] [--nobt] [--multionly] [--mindays n] --out output.json
```

`--nobt` disables backtesting

`--multionly` excludes single-contributor repositories from consideration.

`--mindays` excludes respositories whose activity period is less than the minimum number of days.

Convert the json into an arff file with:

```
./to_arff.py output.json > features.arff
```

Then run it through Weka, possibly with feature selection, with

```
./run_weka.py [--featureselect] features.arff
```

Make plots of the data with

```
./plot.py output.json
```

## Full mining data

The full data is not included in repository due to file size.

### Full project information (22mb)

http://boa.cs.iastate.edu/boa/index.php?q=boa/job/public/34317

### Full revision history (947mb)

http://boa.cs.iastate.edu/boa/index.php?q=boa/job/public/33576
