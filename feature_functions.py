import inspect

from collections import Counter

def percentage_contribution_for_top(revisions, number_of_contributors):
    counts = Counter(revision.author for revision in revisions)
    sorted_by_count = sorted((count for count in counts.itervalues()), reverse=True)
    return float(sum(sorted_by_count[0:number_of_contributors])) / len(revisions)

def number_of_contributors_days_sticking(revisions, n):
    """Number of people whose earliest and latest commit spans more than n day"""
    people_commit_dates = {}
    for revision in revisions:
        author = revision.author
        if author in people_commit_dates:
            previous_earliest, previous_latest = people_commit_dates[author]
            people_commit_dates[author] = (min(previous_earliest, revision.date),
                                           max(previous_latest, revision.date))
        else:
            people_commit_dates[author] = (revision.date, revision.date)
    return sum((latest - earliest).days >= n
               for (earliest, latest)
               in people_commit_dates.itervalues())

class FeaturesFunctions(object):
    # All features should have the arguments (project, revisions, cutoff_date)

    # People
    @staticmethod
    def number_of_contributors(project, revisions, cutoff_date):
        unique_contributors = set(revision.author for revision in revisions)
        return len(unique_contributors)

    # Revisions / Commits
    @staticmethod
    def number_of_contributors_multiple_commits(project, revisions, cutoff_date):
        """Number of people who've made more than one commit"""
        counts = Counter(revision.author for revision in revisions)
        return sum(count > 1 for count in counts.itervalues())

    @staticmethod
    def number_of_contributors_over_day(project, revisions, cutoff_date):
        return number_of_contributors_days_sticking(revisions, 1)

    @staticmethod
    def number_of_contributors_over_week(project, revisions, cutoff_date):
        return number_of_contributors_days_sticking(revisions, 7)

    @staticmethod
    def number_of_commits(project, revisions, cutoff_date):
        return len(revisions)

    @staticmethod
    def percentage_of_founder_revisions(project, revisions, cutoff_date):
        founder = revisions[0].author
        founder_revisions = 0
        for i in reversed(range(len(revisions))):
            if revisions[i].author == founder:
                founder_revisions += 1
        return float(founder_revisions)/len(revisions) #in Python3, no need of float()

    @staticmethod
    def percentage_of_top2_contributors_revisions(project, revisions, cutoff_date):
        return percentage_contribution_for_top(revisions, 2)

    @staticmethod
    def percentage_of_top3_contributors_revisions(project, revisions, cutoff_date):
        return percentage_contribution_for_top(revisions, 3)

    @staticmethod
    def percentage_of_top5_contributors_revisions(project, revisions, cutoff_date):
        return percentage_contribution_for_top(revisions, 5)

    @staticmethod
    def date_before_last_revision(project, revisions, cutoff_date):
        return (cutoff_date - revisions[-1].date).days

    @staticmethod
    def date_before_last_revision_by_founder(project, revisions, cutoff_date):
        founder = revisions[0].author
        for i in reversed(range(len(revisions))):
            if revisions[i].author == founder:
                return (cutoff_date - revisions[i].date).days

    @staticmethod
    def density_of_revisions(project, revisions, cutoff_date):
        days = (cutoff_date - revisions[0].date).days
        if days > 0:
            return len(revisions) / float(days)
        return 0

    @staticmethod
    def largest_gap_between_two_consecutive_revisions(project, revisions, cutoff_date):
        largest_gap = 0
        previous_revision = revisions[0]
        for revision in revisions:
            if (revision.date - previous_revision.date).days > largest_gap:
                largest_gap = (revision.date - previous_revision.date).days
            previous_revision = revision
        return largest_gap


    # Documentation
    @staticmethod
    def has_docs(project, revisions, cutoff_date):
        return project.has_docs

    # Others
    @staticmethod
    def project_age(project, revisions, cutoff_date):
        return (cutoff_date - revisions[0].date).days

    @staticmethod
    def description_size(project, revisions, cutoff_date):
        return project.description_size

    @staticmethod
    def number_of_programming_languages(project, revisions, cutoff_date):
        return project.number_of_programming_languages

def feature_functions():
    return sorted([method for name, method
                          in inspect.getmembers(FeaturesFunctions)
                          if not name.startswith('_')],
                  key=lambda method: method.__name__)
