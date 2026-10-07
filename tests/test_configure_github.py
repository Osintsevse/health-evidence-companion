"""Offline administrative-script tests; never contact GitHub or handle secrets."""
import json
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import configure_github


class ConfigureGitHubTests(unittest.TestCase):
    def test_protection_request_is_closed_readable_and_cleaned_up(self):
        request_path = None

        def command(args):
            nonlocal request_path
            if '--input' in args:
                request_path = Path(args[args.index('--input') + 1])
                result = subprocess.run(
                    [sys.executable, '-c',
                     'import pathlib,sys; print(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))',
                     str(request_path)], check=True, capture_output=True, text=True)
                protection = json.loads(result.stdout)
                self.assertEqual(protection['required_status_checks']['contexts'], ['validate-and-build'])
                self.assertTrue(protection['required_pull_request_reviews']['require_code_owner_reviews'])

        with patch.object(sys, 'argv', ['configure_github.py', '--execute', '--protect-only']), \
                patch('configure_github.shutil.which', return_value='synthetic-gh'), \
                patch('configure_github.run', side_effect=command) as commands, \
                patch('builtins.print'):
            configure_github.main()
        self.assertIsNotNone(request_path)
        self.assertFalse(request_path.exists())
        self.assertFalse(request_path.parent.exists())
        self.assertEqual(len(commands.call_args_list), 3)

    def test_failed_protection_command_cleans_up_request(self):
        request_path = None

        def command(args):
            nonlocal request_path
            if '--input' in args:
                request_path = Path(args[args.index('--input') + 1])
                self.assertTrue(request_path.is_file())
                raise RuntimeError('Synthetic command failure')

        with patch.object(sys, 'argv', ['configure_github.py', '--execute', '--protect-only']), \
                patch('configure_github.shutil.which', return_value='synthetic-gh'), \
                patch('configure_github.run', side_effect=command), patch('builtins.print'):
            with self.assertRaisesRegex(RuntimeError, 'Synthetic command failure'):
                configure_github.main()
        self.assertIsNotNone(request_path)
        self.assertFalse(request_path.exists())

    def test_dry_run_does_not_run_external_commands(self):
        with patch.object(sys, 'argv', ['configure_github.py']), \
                patch('configure_github.run') as commands, patch('builtins.print'):
            configure_github.main()
        commands.assert_not_called()


if __name__ == '__main__':
    unittest.main()
