import sqlite3

from datetime import datetime

class Revision(object):
    def __init__(self, row):
        id_raw, date_raw, name_raw = row
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

# Returns revisions for a given project, sorted from earliest to latest.
def get_revisions_for_project(db_connection, project_id):
    cursor = db_connection.cursor()
    cursor.execute('''SELECT id, date, author FROM revisions
                      WHERE project = ?
                   ''', (project_id,))

    revisions = [Revision(row) for row in cursor]
    return sorted(revisions, key=lambda revision: revision.date)

# Get the project founder from a list of revisions.
def get_founder(revisions):
    return revisions[0].name
