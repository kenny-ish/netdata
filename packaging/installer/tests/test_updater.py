#!/usr/bin/env python3
"""Exercise the updater's native package repository path mapping."""
from pathlib import Path
import subprocess
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'netdata-updater.sh'


class UpdaterRepoPathTests(unittest.TestCase):
    def repo_path(self, distro, version, arch='x86_64'):
        source = SCRIPT.read_text()
        start = source.index('get_repo_path() {')
        end = source.index('\n}\n', start) + 3
        command = source[start:end] + '\nget_repo_path "$1" "$2" "$3"\n'
        result = subprocess.run(
            ['sh', '-c', command, 'test', distro, version, arch],
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()

    def test_repo_paths_use_published_layout(self):
        cases = (
            ('amzn', '2', 'amazonlinux/2/x86_64'),
            ('centos-stream', '9', 'el/c9s/x86_64'),
            ('fedora', '41', 'fedora/41/x86_64'),
            ('ol', '8.10', 'ol/8/x86_64'),
            ('centos', '9.6', 'el/9/x86_64'),
        )
        for distro, version, expected in cases:
            with self.subTest(distro=distro, version=version):
                self.assertEqual(self.repo_path(distro, version), expected)


if __name__ == '__main__':
    unittest.main()
