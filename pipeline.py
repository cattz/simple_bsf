"""Pipeline classes"""

import os
import sys


class Pipeline(object):
    """Base pipeline class, in charge of the minimal configuration
    """
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
    def __init__(self, source):
        super(ReleaseWorker, self).__init__(source)

    def publish(self, path):
        print 'ReleaseWorker: Publishing to %s' % path

    def promote(self, repo):
        print 'ReleaseWorker: Promoting to %s' % repo

    def send_email(self, recipient):
        print 'Sending email to %s' % recipient
