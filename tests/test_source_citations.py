"""Citation validation with wholly fictional, independent source registers."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from validate import check_source_citations


class SourceCitationTests(unittest.TestCase):
    # S01 intentionally collides; S02 and S03 belong to different registers.
    MEDICAL_IDS = {'S01', 'S02'}
    PSYCHOLOGY_IDS = {'S01', 'S03'}
    MEDICAL_PATH = 'knowledge/FICTIONAL_FOUNDATIONS.md'
    PSYCHOLOGY_PATH = 'knowledge/psychology/FICTIONAL_FOUNDATIONS.md'

    def check(self, text, path):
        check_source_citations(text, path, self.MEDICAL_IDS, self.PSYCHOLOGY_IDS)

    def test_bare_medical_ids_use_file_domain(self):
        self.check('Fictional claim [S01, S02].', self.MEDICAL_PATH)
        with self.assertRaisesRegex(ValueError, 'Unknown source ID S03'):
            self.check('Fictional claim [S03].', self.MEDICAL_PATH)

    def test_bare_psychology_ids_preserve_domain_paths(self):
        paths = [self.PSYCHOLOGY_PATH, 'docs/psychology/fictional.md',
                 'evals/psychology/fictional.md',
                 r'skills\synthetic\references\psychology\fictional.md']
        for path in paths:
            with self.subTest(path=path):
                self.check('Fictional claim [S01, S03].', path)
                with self.assertRaisesRegex(ValueError, 'Unknown source ID S02'):
                    self.check('Fictional claim [S02].', path)

    def test_explicit_psychology_reference_from_medical_file(self):
        self.check('Fictional claim [psychology:S03].', self.MEDICAL_PATH)

    def test_explicit_medical_reference_from_psychology_file(self):
        self.check('Fictional claim [medical:S02].', self.PSYCHOLOGY_PATH)

    def test_colliding_ids_are_valid_in_their_explicit_registers(self):
        for path in (self.MEDICAL_PATH, self.PSYCHOLOGY_PATH):
            with self.subTest(path=path):
                self.check('Fictional comparison [medical:S01; psychology:S01].', path)

    def test_medical_reference_cannot_use_psychology_only_id(self):
        with self.assertRaisesRegex(ValueError, 'Unknown source ID medical:S03'):
            self.check('Fictional claim [medical:S03].', self.PSYCHOLOGY_PATH)

    def test_psychology_reference_cannot_use_medical_only_id(self):
        with self.assertRaisesRegex(ValueError, 'Unknown source ID psychology:S02'):
            self.check('Fictional claim [psychology:S02].', self.MEDICAL_PATH)

    def test_unknown_explicit_id_is_rejected(self):
        for namespace in ('medical', 'psychology'):
            with self.subTest(namespace=namespace):
                with self.assertRaisesRegex(ValueError, 'Unknown source ID ' + namespace + ':S999'):
                    self.check('Fictional claim [' + namespace + ':S999].', self.MEDICAL_PATH)

    def test_unknown_namespace_cannot_fall_back_to_colliding_id(self):
        for namespace in ('fictional', 'Medical', 'fictional.medical', 'fictional:medical'):
            with self.subTest(namespace=namespace):
                with self.assertRaisesRegex(ValueError, 'Unknown source namespace'):
                    self.check('Fictional claim [' + namespace + ':S01].', self.MEDICAL_PATH)

    def test_mixed_bare_and_explicit_ids_keep_independent_domains(self):
        self.check('Fictional claim [S02; psychology:S03; medical:S01].', self.MEDICAL_PATH)
        self.check('Fictional claim [S03; medical:S02; psychology:S01].', self.PSYCHOLOGY_PATH)

    def test_source_like_tokens_inside_urls_remain_ignored(self):
        self.check('Fictional claim [S02](https://example.invalid/S999?ref=fictional:S999).',
                   self.MEDICAL_PATH)


if __name__ == '__main__':
    unittest.main()
