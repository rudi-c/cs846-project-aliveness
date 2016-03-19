# All features should have the arguments (project, revisions, cutoff_date)

# People

def number_of_contributors(project, revisions, cutoff_date):
    unique_contributors = set(revision.author for revision in revisions)
    return len(unique_contributors)


# Revisions / Commits

def number_of_commits(project, revisions, cutoff_date):
    return len(revisions)

def percentage_of_founder_revisions(project, revisions, cutoff_date):
    founder = revisions[0].author
    founder_revisions = 0
    for i in reversed(range(len(revisions))):
        if revisions[i].author == founder:
            founder_revisions += 1
    return float(founder_revisions)/len(revisions) #in Python3, no need of float()

def date_before_last_revision(project, revisions, cutoff_date):
    return (cutoff_date - revisions[-1].date).days

def date_before_last_revision_by_founder(project, revisions, cutoff_date):
    founder = revisions[0].author
    for i in reversed(range(len(revisions))):
        if revisions[i].author == founder:
            return (cutoff_date - revisions[i].date).days

def density_of_revisions(project, revisions, cutoff_date):
    days = (cutoff_date - revisions[0].date).days
    if days > 0:
        return len(revisions) / float(days)
    return 0

def largest_gap_between_two_consecutive_revisions(project, revisions, cutoff_date):
    largest_gap = 0
    previous_revision = revisions[0]
    for revision in revisions:
        if (revision.date - previous_revision.date).days > largest_gap:
            largest_gap = (revision.date - previous_revision.date).days
        previous_revision = revision
    return largest_gap


# Documentation




# Others

def project_age(project, revisions, cutoff_date):
    return (cutoff_date - revisions[0].date).days

def description_size(project, revisions, cutoff_date):
    return project.description_size

def number_of_programming_languages(project, revisions, cutoff_date):
    return project.number_of_programming_languages
