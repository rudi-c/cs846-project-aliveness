# All features should have the arguments (project, revisions, cutoff_date)

# People

def number_of_contributors(project, revisions, cutoff_date):
    contributors_list = []
    contributors_list = [revision.author for revision in revisions if revision.author not in contributors_list]
    return len(contributors_list)


# Revisions / Commits

def number_of_commits(project, revisions, cutoff_date):
    return len(revisions)

def percentage_of_founder_revisions(project, revisions, cutoff_date):
    founder = revisions[0].author
    founder_revisions = 0
    for i in reversed(range(len(revisions))):
        if(revisions[i].author == founder):
            founder_revisions += 1
    return float(founder_revisions)/len(revisions) #in Python3, no need for float()

def date_before_last_revision(project, revisions, cutoff_date):
    return (cutoff_date - revisions[-1].date).days

def date_before_last_revision_by_founder(project, revisions, cutoff_date):
    founder = revisions[0].author
    for i in reversed(range(len(revisions))):
        if(revisions[i].author == founder):
            return (cutoff_date - revisions[i].date).days
def number_of_fixing_revisions(project, revisions, cutoff_date):
    pass

def density_of_revisions(project, revisions, cutoff_date):
    days = (cutoff_date - revisions[0].date).days
    if(days > 0):
        return len(revisions) / float(days)
    return 0

def largest_gap_between_two_consecutive_revisions(project, revisions, cutoff_date):
    largest_gap = 0
    previous_revision = revisions[0]
    for revision in revisions:
        if((revision.date - previous_revision.date).days > largest_gap):
            largest_gap = (revision.date - previous_revision.date).days
        previous_revision = revision
    return largest_gap


# Documentation




# Others