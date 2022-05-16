"""
    :copyleft: 2020 by the reversion-compare-tests team, see AUTHORS for more details.
    :created: 2020 by Jens Diemer
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""


from pathlib import Path
from unittest import TestCase as UnitTestCase

from django.conf import settings
from django.core.management import call_command
from django.test import SimpleTestCase, TestCase
from django_tools.unittest_utils.django_command import DjangoCommandMixin
from django_tools.unittest_utils.stdout_redirect import StdoutStderrBuffer

import reversion_compare_tests


MANAGE_DIR = Path(reversion_compare_tests.__file__).parent


class SimpleCallCommandTestCase(SimpleTestCase):

    def test_settings_module(self):
        self.assertIn('reversion_compare_tests.settings', settings.SETTINGS_MODULE)

    def test_diffsettings(self):
        """
        Check some settings
        """
        with StdoutStderrBuffer() as buff:
            call_command('diffsettings')
        output = buff.get_output()
        print(output)
        self.assertIn('reversion_compare_tests.settings', output)  # SETTINGS_MODULE

    def test_django_check(self):
        """
        call './manage.py check' directly via 'call_command'
        """
        with StdoutStderrBuffer() as buff:
            call_command('check')
        output = buff.get_output()
        self.assertIn('System check identified no issues (0 silenced).', output)


class ManageCommandTests(DjangoCommandMixin, UnitTestCase):

    def test_help(self):
        """
        Run './manage.py --help' via subprocess and check output.
        """
        output = self.call_manage_py(['--help'], manage_dir=MANAGE_DIR)

        self.assertNotIn('ERROR', output)
        self.assertIn('[django]', output)
        self.assertIn('Type \'manage.py help <subcommand>\' for help on a specific subcommand.', output)


class CallCommandTestCase(TestCase):
    def test_missing_migrations(self):
        with StdoutStderrBuffer() as buff:
            call_command("makemigrations", dry_run=True)
        output = buff.get_output()
        print(output)
        self.assertIn("No changes detected", output)
        self.assertNotIn("Migrations for", output)  # output like: """Migrations for 'appname':"""
        self.assertNotIn("SystemCheckError", output)
        self.assertNotIn("ERRORS", output)
