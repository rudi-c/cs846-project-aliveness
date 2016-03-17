# All features should have the arguments (project, revisions, cutoff_date)

def date_before_last_revision(project, revisions, cutoff_date):
    return (cutoff_date - revisions[-1].date).days
