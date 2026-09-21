import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class KnowledgeStateContractTests(unittest.TestCase):
    def test_transformer_example_keeps_concept_and_implementation_separate(self):
        text = (ROOT / "examples/personalized/researcher-profile-current.yaml").read_text(encoding="utf-8")
        self.assertIn("Transformer:\n    conceptual: 2", text)
        self.assertIn("    implementation: 0", text)

    def test_agent_rules_prohibit_collapsing_learning_into_one_score(self):
        text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("Never collapse learning into a single score.", text)
        self.assertIn("Transformer conceptual      = 2", text)
        self.assertIn("Transformer implementation  = 0", text)


if __name__ == "__main__":
    unittest.main()
