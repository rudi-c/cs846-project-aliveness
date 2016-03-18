# All features should have the arguments (project, revisions, cutoff_date)

def date_before_last_revision(project, revisions, cutoff_date):
    return (cutoff_date - revisions[-1].date).days

def date_before_last_revision_by_founder(project, revisions, cutoff_date):
    founder = revisions[0].author
    for i in range(len(revisions)-1, 0,-1):
        if(revisions[i].author == founder):
            print (cutoff_date - revisions[i].date).days
            return (cutoff_date - revisions[i].date).days
