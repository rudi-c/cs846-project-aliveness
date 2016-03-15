import math
import random
import sqlite3

from datetime import datetime

# September 1st
CUTOFF_DATE = datetime(2013, 9, 1)

class Project(object):
    def __init__(self, db_row):
        id_raw, name_raw, revision_count_raw, has_docs_raw = db_row
        self.id = int(id_raw)
        self.name = name_raw
        self.revision_count = int(revision_count_raw)
        self.has_docs = bool(int(has_docs_raw))

    def __str__(self):
        return "%d, %s, %d, %r" % (self.id, self.name, self.revision_count, self.has_docs)

class Revision(object):
    def __init__(self, db_row):
        id_raw, date_raw, name_raw = db_row
        self.id = id_raw
        self.date = datetime.strptime(date_raw, "%d/%m/%y %H:%M:%S")
        self.name = name_raw

    def __str__(self):
        return "%s, %s, %s" % (self.id, str(self.date), self.name)

def open_db(full):
    if full:
        database_name = "repos.db"
    else:
        database_name = "repos_test.db"

    conn = sqlite3.connect(database_name)
    conn.text_factory = str     # easiest way to deal with encodings right now
    return conn

# Return all project objects in the database.
def get_projects(db_connection):
    cursor = db_connection.cursor()
    cursor.execute('''SELECT id, name, revision_count, has_docs FROM repos
                   ''')
    projects = [Project(db_row) for db_row in cursor]
    return projects


# Returns revisions objects for a given project, sorted from earliest to latest.
def get_revisions_for_project(db_connection, project_id):
    cursor = db_connection.cursor()
    cursor.execute('''SELECT id, date, author FROM revisions
                      WHERE project = ?
                   ''', (project_id,))

    revisions = [Revision(db_row) for db_row in cursor]
    return sorted(revisions, key=lambda revision: revision.date)

# Returns a new list of revisions that only contain the revisions before a
# cutoff date
def get_revisions_before_cutoff(revisions, date):
    return [revision for revision in revisions if revision.date < date]

# Get the project founder from a list of revisions.
def get_founder(revisions):
    return revisions[0].name

# Return a random sample from a list, maintaining the original order of the list
def get_random_sample(lst, n):
    return [lst[i] for i in sorted(random.sample(xrange(len(mylist)), n))]

# Given a list of integers, bin them logarithmically (base 2).
# Return a list of ((start, end), count)
def log_bin(lst):
    log_bins = {}
    for n in lst:
        assert n >= 0
        index = int(math.log(n + 1, 2))
        if index in log_bins:
            log_bins[index] += 1
        else:
            log_bins[index] = 1

    non_log_bins = []
    for index, count in log_bins.iteritems():
        non_log_bins.append((int(pow(2.0, index)) - 1, count))
    non_log_bins = sorted(non_log_bins)
    return [((start, start * 2), str(count)) for start, count in non_log_bins]
