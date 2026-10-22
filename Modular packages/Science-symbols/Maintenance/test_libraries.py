"""Regression checks for libraries read by Inkscape's line-based title scanner."""
import html
import json
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET
import zipfile


PACKAGE = Path(__file__).resolve().parent.parent
CATALOG = json.loads((PACKAGE / 'Maintenance/catalog.json').read_text(encoding='utf-8'))
SVG = '{http://www.w3.org/2000/svg}'


class LibraryCompatibilityTests(unittest.TestCase):
    def test_single_repository_entry_points(self):
        root = PACKAGE.parents[1]
        for name in ('Install.cmd', 'index.html'):
            self.assertTrue((root / name).is_file())
            self.assertFalse((PACKAGE / name).exists())

    def test_authored_examples_are_complete_svg_documents(self):
        for row in CATALOG['examples']:
            with self.subTest(example=row['file']):
                root = ET.parse(PACKAGE / row['file']).getroot()
                self.assertEqual(root.tag, SVG + 'svg')

    def test_title_is_on_a_short_separate_line_before_artwork(self):
        # The old single-line files crashed scan_all_symbol_sets in Inkscape
        # 1.4.4 on Windows, even though they were valid SVG and XML.
        for category in CATALOG['categories']:
            with self.subTest(library=category['library']):
                lines = (PACKAGE / category['library']).read_text(encoding='utf-8').splitlines()
                title = '<title>' + html.escape(category['name'], quote=False) + '</title>'
                title_index = next(i for i, line in enumerate(lines) if '<title>' in line)
                self.assertEqual(lines[title_index].strip(), title)
                self.assertTrue(all(len(line) <= 4096 for line in lines[:title_index + 1]))
                self.assertFalse(any('<defs' in line or '<symbol' in line for line in lines[:title_index]))

    def test_all_catalogued_symbols_are_present(self):
        for category in CATALOG['categories']:
            with self.subTest(library=category['library']):
                root = ET.parse(PACKAGE / category['library']).getroot()
                symbols = root.find(SVG + 'defs').findall(SVG + 'symbol')
                expected = {row['id'] for row in CATALOG['components'] if row['category'] == category['id']}
                self.assertEqual({s.get('id') for s in symbols}, expected)
                self.assertEqual(len(symbols), len(expected))

    def test_download_contains_current_libraries_and_installer(self):
        with zipfile.ZipFile(PACKAGE.parents[1] / 'downloads/Science-symbols.zip') as archive:
            expected = {c['library'] for c in CATALOG['categories']}
            expected.update(('Install.cmd', 'Maintenance/install.ps1', 'Maintenance/catalog.json'))
            self.assertEqual(set(archive.namelist()), expected)
            self.assertIsNone(archive.testzip())
            launcher = archive.read('Install.cmd')
            self.assertIn(b'\r\n', launcher)
            self.assertNotIn(b'\r', launcher.replace(b'\r\n', b''))
            self.assertNotIn(b'\n', launcher.replace(b'\r\n', b''))
            for name in expected - {'Maintenance/catalog.json'}:
                source = PACKAGE.parents[1] / name if name == 'Install.cmd' else PACKAGE / name
                self.assertEqual(archive.read(name), source.read_bytes())


if __name__ == '__main__':
    unittest.main()
