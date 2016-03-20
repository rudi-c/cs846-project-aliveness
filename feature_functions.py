import inspect

from collections import Counter

def percentage_contribution_for_top(contributor_commit_counts,
                                    number_of_contributors,
                                    number_of_revisions):
    sorted_by_count = sorted(contributor_commit_counts.itervalues(), reverse=True)
    return float(sum(sorted_by_count[0:number_of_contributors])) / number_of_revisions

def number_of_contributors_days_sticking(people_commit_dates, n):
    """Number of people whose earliest and latest commit spans more than n day"""
    return sum((latest - earliest).days >= n
               for (earliest, latest)
               in people_commit_dates.itervalues())

class FeaturesFunctions(object):
    # All features should have the arguments (project, revisions, cutoff_date)

    def __init__(self, project, revisions, cutoff_date):
        self.project = project
        self.revisions = revisions
        self.cutoff_date = cutoff_date
        # Precompute some stuff expensive stuff that's needed over multiple
        # features for performance.

        # { contributor name: number of commits by contributor }
        self.contributor_commit_counts = Counter(revision.author for revision
                                                 in revisions)
        # { contributor name: (date of first commit, date of last commit) }
        people_commit_dates = {}
        for revision in revisions:
            author = revision.author
            if author in people_commit_dates:
                previous_earliest, previous_latest = people_commit_dates[author]
                people_commit_dates[author] = (min(previous_earliest, revision.date),
                                               max(previous_latest, revision.date))
            else:
                people_commit_dates[author] = (revision.date, revision.date)
        self.contributor_commit_dates = people_commit_dates


    # People
    def number_of_contributors(self):
        return len(self.contributor_commit_counts)

    # Revisions / Commits
    def number_of_contributors_multiple_commits(self):
        """Number of people who've made more than one commit"""
        return sum(count > 1 for count in self.contributor_commit_counts.itervalues())

    def number_of_contributors_over_day(self):
        return number_of_contributors_days_sticking(self.contributor_commit_dates, 1)

    def number_of_contributors_over_week(self):
        return number_of_contributors_days_sticking(self.contributor_commit_dates, 7)

    def number_of_commits(self):
        return len(self.revisions)

    def percentage_of_founder_revisions(self):
        founder = self.revisions[0].author
        return float(self.contributor_commit_counts[founder]) / len(self.revisions)

    def percentage_of_top2_contributors_revisions(self):
        return percentage_contribution_for_top(
            self.contributor_commit_counts, 2, len(self.revisions))

    def percentage_of_top3_contributors_revisions(self):
        return percentage_contribution_for_top(
            self.contributor_commit_counts, 3, len(self.revisions))

    def percentage_of_top5_contributors_revisions(self):
        return percentage_contribution_for_top(
            self.contributor_commit_counts, 5, len(self.revisions))

    def date_before_last_revision(self):
        return (self.cutoff_date - self.revisions[-1].date).days

    def date_before_last_revision_by_founder(self):
        founder = self.revisions[0].author
        first, last = self.contributor_commit_dates[founder]
        return (self.cutoff_date - last).days

    def density_of_revisions(self):
        days = (self.cutoff_date - self.revisions[0].date).days
        if days > 0:
            return len(self.revisions) / float(days)
        return 0

    def largest_gap_between_two_consecutive_revisions(self):
        largest_gap = 0
        previous_revision = self.revisions[0]
        for revision in self.revisions:
            if (revision.date - previous_revision.date).days > largest_gap:
                largest_gap = (revision.date - previous_revision.date).days
            previous_revision = revision
        return largest_gap

    # Documentation
    def has_docs(self):
        return self.project.has_docs

    # Others
    def project_age(self):
        return (self.cutoff_date - self.revisions[0].date).days

    def description_size(self):
        return self.project.description_size

    def number_of_programming_languages(self):
        return self.project.number_of_programming_languages

def feature_functions():
    return sorted([method for name, method
                          in inspect.getmembers(FeaturesFunctions)
                          if not name.startswith('_')],
                  key=lambda method: method.__name__)
