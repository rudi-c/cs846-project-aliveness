# All features should have the arguments (project, revisions, cutoff_date)

def date_before_last_revision(project, revisions, cutoff_date):
    return (cutoff_date - revisions[-1].date).days

def date_before_last_revision_by_founder(project, revisions, cutoff_date):
    founder = revisions[0].author
    for i in reversed(range(len(revisions))):
        if(revisions[i].author == founder):
            return (cutoff_date - revisions[i].date).days

def percentage_of_founder_revisions(project, revisions, cutoff_date):
    founder = revisions[0].author
    founder_revisions = 0
    for i in reversed(range(len(revisions))):
        if(revisions[i].author == founder):
            founder_revisions += 1
    return float(founder_revisions)/len(revisions) #in Python3, no need for float()

