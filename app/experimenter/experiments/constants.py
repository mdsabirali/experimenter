class ExperimentConstants(object):
    # Status stuff
    STATUS_CREATED = 'Created'
    STATUS_PENDING = 'Pending'
    STATUS_ACCEPTED = 'Accepted'
    STATUS_LAUNCHED = 'Launched'
    STATUS_COMPLETE = 'Complete'
    STATUS_REJECTED = 'Rejected'

    STATUS_CHOICES = (
        (STATUS_CREATED, STATUS_CREATED),
        (STATUS_PENDING, STATUS_PENDING),
        (STATUS_ACCEPTED, STATUS_ACCEPTED),
        (STATUS_LAUNCHED, STATUS_LAUNCHED),
        (STATUS_COMPLETE, STATUS_COMPLETE),
        (STATUS_REJECTED, STATUS_REJECTED),
    )

    STATUS_TRANSITIONS = {
        STATUS_CREATED: [
            STATUS_PENDING,
            STATUS_REJECTED,
        ],
        STATUS_PENDING: [
            STATUS_ACCEPTED,
            STATUS_REJECTED,
        ],
        STATUS_ACCEPTED: [
            STATUS_LAUNCHED,
            STATUS_REJECTED,
        ],
        STATUS_LAUNCHED: [
            STATUS_COMPLETE,
        ],
        STATUS_COMPLETE: [
        ],
        STATUS_REJECTED: [
        ],
    }

    # Version stuff
    VERSION_CHOICES = (
        (None, 'Firefox Version'),
        ('55.0', '55.0'),
        ('56.0', '56.0'),
        ('57.0', '57.0'),
        ('58.0', '58.0'),
        ('59.0', '59.0'),
        ('60.0', '60.0'),
        ('61.0', '61.0'),
        ('62.0', '62.0'),
        ('63.0', '63.0'),
        ('64.0', '64.0'),
    )

    # Channel stuff
    CHANNEL_NIGHTLY = 'Nightly'
    CHANNEL_BETA = 'Beta'
    CHANNEL_RELEASE = 'Release'

    CHANNEL_CHOICES = (
        (None, 'Firefox Channel'),
        (CHANNEL_NIGHTLY, CHANNEL_NIGHTLY),
        (CHANNEL_BETA, CHANNEL_BETA),
        (CHANNEL_RELEASE, CHANNEL_RELEASE),
    )

    # Pref stuff
    PREF_TYPE_BOOL = 'boolean'
    PREF_TYPE_INT = 'integer'
    PREF_TYPE_STR = 'string'

    PREF_TYPE_CHOICES = (
        (PREF_TYPE_BOOL, PREF_TYPE_BOOL),
        (PREF_TYPE_INT, PREF_TYPE_INT),
        (PREF_TYPE_STR, PREF_TYPE_STR),
    )

    PREF_BRANCH_USER = 'user'
    PREF_BRANCH_DEFAULT = 'default'
    PREF_BRANCH_CHOICES = (
        (PREF_BRANCH_DEFAULT, PREF_BRANCH_DEFAULT),
        (PREF_BRANCH_USER, PREF_BRANCH_USER),
    )

    # Help texts
    NAME_HELP_TEXT = """
      <p>
        Choose a name for your experiment that describes what it is trying to study, such as the effect of
        a new feature, a performance improvement, a UI change, a bug fix, etc.
      <p>
      <p><strong>Example:</strong> Larger Sign In Button
    """

    SHORT_DESCRIPTION_HELP_TEXT = """
      <p>Describe the purpose of your experiment in 1-2 sentences.</p>
      <p><strong>Example:</strong> We believe increasing the size of the sign in button will increase its click through rate.</p>
    """

    POPULATION_PERCENT_HELP_TEXT = """
      <p>Describe the Firefox population that will receive this experiment.<p>
      <p><strong>Example:</strong> 10% of Firefox 60.0 Nightly<p>
    """

    CLIENT_MATCHING_HELP_TEXT = """
      <p>
        Describe the criteria a client must meet to participate in the study in addition to the version and channel filtering specified above.
        Explain in natural language how you would like clients to be filtered and the Shield team will implement the filtering for you, you do not need to express the filter in code.
        Each filter may be inclusive or exclusive, ie "Please include users from locales A, B, C and exclude those from X, Y, Z".
      </p>
      <ul>
        <li>
          <p><strong>Locales</strong> A list of <a href="https://wiki.mozilla.org/L10n:Locale_Codes">Firefox Locale Codes</a></p>
          <p><strong>Example:</strong> en-US, fr-FR, de-DE</p>
        </li>
        <li>
          <p><strong>Geographic regions</strong> A list of <a href="http://www.geonames.org/countries/">Country Geo Codes</a></p>
          <p><strong>Example:</strong> US, FR, DE</p>
        </li>
        <li>
          <p><strong>Prefs</strong> Pref and value pairs to match against.</p>
          <p><strong>Example:</strong> browser.search.region=CA</p>
        </li>
        <li>
          <p><strong>Studies</strong> Other Shield Studies to match against.</p>
          <p><strong>Example:</strong> Exclude clients in pref-flip-other-study</p>
        </li>
      </ul>
    """

    # Text defaults
    CLIENT_MATCHING_DEFAULT = (
"""Locales:
Geographic regions:
Prefs:
Studies:
""")
