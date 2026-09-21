import sys
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from research_workspace.validator import validate_workspace


class ValidatorTests(unittest.TestCase):
    def test_valid_entity(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "papers").mkdir()
            (root / "papers" / "paper.md").write_text(
                "---\n"
                "id: PAPER-0001\n"
                "type: Paper\n"
                "status: draft\n"
                "created_at: 2026-09-21\n"
                "updated_at: 2026-09-21\n"
                "provenance: pending\n"
                "---\n# Test\n",
                encoding="utf-8",
            )
            self.assertEqual(validate_workspace(root), [])


if __name__ == "__main__":
    unittest.main()
