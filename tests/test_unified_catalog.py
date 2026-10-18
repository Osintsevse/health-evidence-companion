"""Synthetic domain/citation isolation and canonical-source preservation checks."""
import copy
import datetime as dt
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from source_catalog import catalog, validate_import_amendments
from source_review import combined_review_queue
from validate import check_psychology_blank, check_source_citations, PSYCHOLOGY_BLANK_FORMS

class CatalogTests(unittest.TestCase):
    def fixture(self, folder):
        (folder/'knowledge/psychology').mkdir(parents=True)
        (folder/'knowledge/clinical').mkdir()
        (folder/'knowledge/clinical/source-use-policy.json').write_text(json.dumps({'rules':[]}),encoding='utf-8')
        medical={'id':'S01','title':'Synthetic medical source','url':'https://example.org/shared','checked_on':'2026-01-01','retrieval_status':'selected section read','region':'Synthetic','use':'Synthetic medical question'}
        psychological={'id':'S01','title':'Synthetic psychological source','url':medical['url'],'checked_at':'2026-02-01','access':'indexed_excerpt','limitations':'Full text not read','use':'Synthetic psychological question'}
        (folder/'knowledge/sources.json').write_text(json.dumps([medical]),encoding='utf-8')
        (folder/'knowledge/psychology/sources.json').write_text(json.dumps({'sources':[psychological]}),encoding='utf-8')
        return medical,psychological

    def test_overlapping_ids_and_urls_do_not_merge_reading_histories(self):
        with tempfile.TemporaryDirectory() as temp:
            folder=Path(temp);medical,psychological=self.fixture(folder)
            before={p:p.read_bytes() for p in folder.rglob('*.json')}
            result=catalog(folder)
            self.assertEqual(result['record_count'],2)
            self.assertTrue(all(x['active_use']=='not_determined' and not x['permission_inferred'] for x in result['records']))
            self.assertEqual(result['unique_url_count'],1)
            self.assertEqual([r['qualified_id'] for r in result['records']],['medical:S01','psychology:S01'])
            self.assertEqual(result['records'][1]['limitations'],psychological['limitations'])
            self.assertEqual([r['checked_on'] for r in result['records']],['2026-01-01','2026-02-01'])
            self.assertEqual(before,{p:p.read_bytes() for p in folder.rglob('*.json')})
            queue=combined_review_queue(result,dt.date(2026,3,1),30)
            self.assertEqual(len(queue),2)
            self.assertEqual({r['qualified_id'] for r in queue},{'medical:S01','psychology:S01'})
            self.assertEqual(len(combined_review_queue(result,dt.date(2026,3,1),30,'psychology')),1)

    def test_citation_namespace_is_checked_before_acceptance(self):
        check_source_citations('S150','knowledge/02_PRIMARY_CARE.md',{'S150'},{'S01'})
        with self.assertRaises(ValueError):
            check_source_citations('S150','knowledge/psychology/02_ETHICS_AND_DIALOGUE.md',{'S150'},{'S01'})
        with self.assertRaises(ValueError):
            check_source_citations('S150','skills/psyops-dialogue/references/psychology/02_ETHICS_AND_DIALOGUE.md',{'S150'},{'S01'})

    def test_filled_psychological_forms_are_rejected(self):
        for name,blank in PSYCHOLOGY_BLANK_FORMS.items():
            check_psychology_blank(blank,name)
            changed=copy.deepcopy(blank);changed['recording_authorization']='Synthetic filled field'
            with self.assertRaises(ValueError):check_psychology_blank(changed,name)
            changed=copy.deepcopy(blank);changed['unexpected']='Synthetic extra field'
            with self.assertRaises(ValueError):check_psychology_blank(changed,name)

    def test_imported_changes_preserve_original_pins_and_have_exact_amendments(self):
        root = Path(__file__).resolve().parents[1]
        path = root / 'docs/psychology/import-provenance.json'
        before = path.read_bytes()
        report = validate_import_amendments(root)
        ledger = json.loads((root / 'docs/psychology/post-import-amendments.json').read_text(encoding='utf-8'))
        self.assertEqual(report['amended_files'], len(ledger['amendments']))
        self.assertEqual(path.read_bytes(), before)


class ImportAmendmentTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.path = 'knowledge/psychology/fictional.md'
        self.other = 'knowledge/psychology/another-fictional.md'
        self.review = 'docs/synthetic-review.md'
        for name, body in [(self.path, 'Synthetic original concept.\n'),
                           (self.other, 'Another synthetic original.\n'),
                           (self.review, '# Synthetic amendment review\n')]:
            target = self.root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(body, encoding='utf-8')
        self.provenance = self.root / 'docs/psychology/import-provenance.json'
        self.provenance.parent.mkdir(parents=True)
        self.originals = {name: self.sha(name) for name in (self.path, self.other)}
        self.provenance.write_text(json.dumps({'files': [
            {'destination_path': name, 'sha256': digest} for name, digest in self.originals.items()
        ]}), encoding='utf-8')
        self.ledger = self.provenance.with_name('post-import-amendments.json')

    def sha(self, path):
        return hashlib.sha256((self.root / path).read_bytes()).hexdigest()

    def amendment(self):
        (self.root / self.path).write_text('Synthetic clarified concept.\n', encoding='utf-8')
        return {'path': self.path, 'original_import_sha256': self.originals[self.path],
                'current_sha256': self.sha(self.path), 'date': '2026-10-17',
                'reason': 'Clarify a wholly fictional inference example.', 'review_document': self.review}

    def write_ledger(self, entries):
        self.ledger.write_text(json.dumps({'schema': 'psychology-post-import-amendments-v1',
                                          'amendments': entries}), encoding='utf-8')

    def test_unchanged_import_needs_no_amendment(self):
        self.assertEqual(validate_import_amendments(self.root)['amended_files'], 0)

    def test_exact_amendment_preserves_original_provenance(self):
        before = self.provenance.read_bytes()
        self.write_ledger([self.amendment()])
        self.assertEqual(validate_import_amendments(self.root),
                         {'imported_files': 2, 'amended_files': 1, 'unchanged_files': 1})
        self.assertEqual(self.provenance.read_bytes(), before)

    def test_unrecorded_import_change_is_rejected(self):
        self.amendment()
        with self.assertRaisesRegex(ValueError, 'Undocumented imported source change'):
            validate_import_amendments(self.root)

    def test_original_hash_must_match_initial_pin(self):
        entry = self.amendment()
        entry['original_import_sha256'] = '0' * 64
        self.write_ledger([entry])
        with self.assertRaisesRegex(ValueError, 'Original import hash mismatch'):
            validate_import_amendments(self.root)

    def test_duplicate_and_unknown_paths_are_rejected(self):
        entry = self.amendment()
        self.write_ledger([entry, dict(entry)])
        with self.assertRaisesRegex(ValueError, 'Duplicate amendment path'):
            validate_import_amendments(self.root)
        entry['path'] = 'knowledge/psychology/not-imported.md'
        self.write_ledger([entry])
        with self.assertRaisesRegex(ValueError, 'Unknown amendment path'):
            validate_import_amendments(self.root)

    def test_later_tampering_with_amended_bytes_is_rejected(self):
        self.write_ledger([self.amendment()])
        (self.root / self.path).write_text('Synthetic unreviewed replacement.\n', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'Current amendment hash mismatch'):
            validate_import_amendments(self.root)

    def test_unamended_file_stays_protected_when_another_is_amended(self):
        self.write_ledger([self.amendment()])
        (self.root / self.other).write_text('Synthetic hidden change.\n', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'Undocumented imported source change'):
            validate_import_amendments(self.root)

    def test_review_metadata_and_paths_are_required(self):
        mutations = [
            {'date': 'not-a-date'}, {'reason': ' '},
            {'review_document': 'docs/missing-review.md'},
            {'review_document': '../outside.md'}, {'path': '../outside.md'},
            {'unexpected_allowance': True}
        ]
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                entry = self.amendment()
                entry.update(mutation)
                self.write_ledger([entry])
                with self.assertRaises(ValueError):
                    validate_import_amendments(self.root)

if __name__=='__main__':unittest.main()
