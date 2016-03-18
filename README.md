# How to use

## Installation

```
sudo apt-get install python-gtk
sudo apt-get install python-matplotlib
```

## Parsing mined data

See `parse.py`

The idea is to get all the data we need from Boa as a textfile, then read it
and store it into a local sqlite database. It will be easier to do queries on
a sqlite database, especially memory and performance-wise.

To make a test run, use either `./parse.py` or `pypy parse.py` (faster). This
will read the files `projects-small.txt`, `revisions-small.txt`,
`activity-span.txt`. It will create the local database `repos_test.db`.

To make create the database for the full GitHub 2015 dataset, use
the `--full` flag. The program will expect to see the files `projects.txt` and
`revisions-small.txt`. See download links below. This make take a few minutes
and create the local database `repos.db`.

## Full mining data

The full data is not included in repository due to file size.

### Full project information (14mb)

http://boa.cs.iastate.edu/boa/index.php?q=boa/job/public/33575

http://boa.cs.iastate.edu/boa/index.php?q=boa/job/public/34178

### Full revision history (947mb)

http://boa.cs.iastate.edu/boa/index.php?q=boa/job/public/33576
