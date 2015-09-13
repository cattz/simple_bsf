"""Pipeline classes
We have a basic pipeline class with the minimum config.
Additional classes extend the functionality and initialize different parts as needed
This allows to use the required functionality and group related methods together
"""

import os
import sys


class Pipeline(object):
    """Base pipeline class, in charge of the minimal configuration
    """

    name = None

    def __init__(self, source):
        self.source = source  #: Source code folder
        self.build_number = os.environ.get('bamboo_buildNumber')
        self.vcs = None  #: Version control manager
        self.binary_repo = None  #: Binary repository manager, ie: Artifactory
        self.confluence_client = None  #: Confluence API client

        self._build_version = None

    def init_vcs(self):
        """Initialize VCS manager from environment and/or info from source folder
        """
        self.vcs = 'Foo'

    @ property
    def build_version(self):
        if self._build_version is None:
            self._build_version = os.environ.get('bamboo_build_version')
            if self._build_version is None:
                """Ideally will try to get the version by other means"""
                print "ERROR: Can't determine the build version"
                sys.exit(-1)
        return self._build_version


class ReleaseWorker(Pipeline):
    """Extends the Pipeline with release tasks
    """

    name = 'release'

    def __init__(self, source):
        super(ReleaseWorker, self).__init__(source)

    def publish(self, path, repo):
        print 'ReleaseWorker: Publishing to %s in %s' % (path, repo)
        # self.pipeline.binary_repo.publish(path, repo)

    def promote(self, repo):
        print 'ReleaseWorker: Promoting to %s' % repo
        # self.pipeline.binary_repo.promote(repo)

    def send_email(self, recipient):
        print 'Sending email to %s' % recipient
