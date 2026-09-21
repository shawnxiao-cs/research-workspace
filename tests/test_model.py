import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from research_workspace.model import validate_knowledge_level, validate_typed_id


class ModelTests(unittest.TestCase):
    def test_levels(self):
        self.assertTrue(validate_knowledge_level(None))
        self.assertTrue(validate_knowledge_level(0))
        self.assertTrue(validate_knowledge_level(4))
        self.assertFalse(validate_knowledge_level(5))

    def test_ids(self):
        self.assertTrue(validate_typed_id("PAPER-0001"))
        self.assertTrue(validate_typed_id("RQ-0012"))
        self.assertTrue(validate_typed_id("EVD-0003"))
        self.assertFalse(validate_typed_id("RQ-12"))


if __name__ == "__main__":
    unittest.main()
