import unittest
from pagecheck import inspect


class SourceChecks(unittest.TestCase):
    def test_sample_before_and_after(self):
        from pathlib import Path
        sample = Path(__file__).resolve().parents[1] / "sample"
        self.assertEqual(len(inspect((sample / "before.html").read_text())), 4)
        self.assertEqual(inspect((sample / "after.html").read_text()), [])

    def test_legacy_and_encoded_fragment_targets(self):
        findings = inspect('<a href="#hello%20world">Go</a><a name="hello world"></a>')
        self.assertFalse(any("Fragment" in item["issue"] for item in findings))

    def test_external_and_placeholder_links_are_not_called_broken(self):
        findings = inspect('<a href="https://example.com/#elsewhere">Go</a><a href="#">Top</a>')
        self.assertFalse(any("Fragment" in item["issue"] for item in findings))

    def test_blank_metadata_is_reported(self):
        findings = inspect('<title> </title><meta name="description" content=" "><meta name="viewport">')
        self.assertEqual(len(findings), 3)


if __name__ == "__main__":
    unittest.main()
