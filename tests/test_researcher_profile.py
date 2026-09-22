import sys
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from research_workspace.profile import (  # noqa: E402
    CANONICAL_KNOWLEDGE_DIMENSIONS,
    PROVENANCE_REVIEW_STATUSES,
    PROVENANCE_TYPES,
    load_researcher_profile,
    validate_researcher_profile,
)
from research_workspace.validator import validate_workspace  # noqa: E402
from research_workspace.workspace import init_workspace  # noqa: E402


VALID_PROFILE = """profile_version: 0.1
researcher:
  id: USER-0001
  stage: ""
  background: []
  research_interests: []
  research_goals: []
learning_progress:
  sources: []
knowledge_state:
  Transformer:
    conceptual: 2
    implementation: 0
    mathematical: null
provenance:
  type: human
  review_status: accepted
  source_refs: []
"""


class ResearcherProfileTests(unittest.TestCase):
    def write_profile(self, root: Path, text: str = VALID_PROFILE) -> Path:
        path = root / "researcher-profile.yaml"
        path.write_text(text, encoding="utf-8")
        return path

    def test_valid_researcher_profile(self):
        with TemporaryDirectory() as tmp:
            path = self.write_profile(Path(tmp))
            self.assertEqual(validate_researcher_profile(path), [])

    def test_valid_personalized_example(self):
        path = ROOT / "examples/personalized/researcher-profile-current.yaml"
        self.assertEqual(validate_researcher_profile(path), [])

    def test_value_5_fails(self):
        with TemporaryDirectory() as tmp:
            path = self.write_profile(Path(tmp), VALID_PROFILE.replace("conceptual: 2", "conceptual: 5"))
            errors = validate_researcher_profile(path)
            self.assertTrue(any("must be null or integer 0..4" in error for error in errors))

    def test_negative_value_fails(self):
        with TemporaryDirectory() as tmp:
            path = self.write_profile(Path(tmp), VALID_PROFILE.replace("conceptual: 2", "conceptual: -1"))
            errors = validate_researcher_profile(path)
            self.assertTrue(any("must be null or integer 0..4" in error for error in errors))

    def test_unknown_dimension_fails(self):
        with TemporaryDirectory() as tmp:
            path = self.write_profile(Path(tmp), VALID_PROFILE.replace("mathematical: null", "overall: 3"))
            errors = validate_researcher_profile(path)
            self.assertTrue(any("overall is not a canonical dimension" in error for error in errors))

    def test_missing_provenance_fails(self):
        with TemporaryDirectory() as tmp:
            text = VALID_PROFILE.split("provenance:", 1)[0]
            path = self.write_profile(Path(tmp), text)
            errors = validate_researcher_profile(path)
            self.assertTrue(any("missing field provenance" in error for error in errors))

    def test_missing_review_status_fails(self):
        with TemporaryDirectory() as tmp:
            path = self.write_profile(
                Path(tmp),
                VALID_PROFILE.replace("  review_status: accepted\n", ""),
            )
            errors = validate_researcher_profile(path)
            self.assertTrue(any("provenance.review_status is required" in error for error in errors))

    def test_missing_researcher_id_fails(self):
        with TemporaryDirectory() as tmp:
            path = self.write_profile(Path(tmp), VALID_PROFILE.replace("  id: USER-0001\n", ""))
            errors = validate_researcher_profile(path)
            self.assertTrue(any("researcher.id is required" in error for error in errors))

    def test_missing_researcher_stage_fails(self):
        with TemporaryDirectory() as tmp:
            path = self.write_profile(Path(tmp), VALID_PROFILE.replace('  stage: ""\n', ""))
            errors = validate_researcher_profile(path)
            self.assertTrue(any("researcher.stage is required" in error for error in errors))

    def test_non_list_background_fails(self):
        with TemporaryDirectory() as tmp:
            path = self.write_profile(Path(tmp), VALID_PROFILE.replace("  background: []", "  background: Computer Science"))
            errors = validate_researcher_profile(path)
            self.assertTrue(any("researcher.background must be a list" in error for error in errors))

    def test_non_list_research_interests_fails(self):
        with TemporaryDirectory() as tmp:
            path = self.write_profile(
                Path(tmp),
                VALID_PROFILE.replace("  research_interests: []", "  research_interests: Remote Sensing"),
            )
            errors = validate_researcher_profile(path)
            self.assertTrue(any("researcher.research_interests must be a list" in error for error in errors))

    def test_non_list_research_goals_fails(self):
        with TemporaryDirectory() as tmp:
            path = self.write_profile(Path(tmp), VALID_PROFILE.replace("  research_goals: []", "  research_goals: Paper reading"))
            errors = validate_researcher_profile(path)
            self.assertTrue(any("researcher.research_goals must be a list" in error for error in errors))

    def test_missing_provenance_type_fails(self):
        with TemporaryDirectory() as tmp:
            path = self.write_profile(Path(tmp), VALID_PROFILE.replace("  type: human\n", ""))
            errors = validate_researcher_profile(path)
            self.assertTrue(any("provenance.type is required" in error for error in errors))

    def test_invalid_provenance_type_fails(self):
        with TemporaryDirectory() as tmp:
            path = self.write_profile(Path(tmp), VALID_PROFILE.replace("  type: human", "  type: robot"))
            errors = validate_researcher_profile(path)
            self.assertTrue(any("provenance.type must be one of" in error for error in errors))

    def test_invalid_review_status_fails(self):
        with TemporaryDirectory() as tmp:
            path = self.write_profile(Path(tmp), VALID_PROFILE.replace("  review_status: accepted", "  review_status: approved"))
            errors = validate_researcher_profile(path)
            self.assertTrue(any("provenance.review_status must be one of" in error for error in errors))

    def test_valid_provenance_passes(self):
        self.assertEqual(PROVENANCE_TYPES, ("source", "generated", "human"))
        self.assertEqual(PROVENANCE_REVIEW_STATUSES, ("pending", "accepted", "edited", "rejected"))
        with TemporaryDirectory() as tmp:
            path = self.write_profile(Path(tmp))
            self.assertEqual(validate_researcher_profile(path), [])

    def test_null_is_accepted_and_preserved(self):
        with TemporaryDirectory() as tmp:
            path = self.write_profile(Path(tmp))
            self.assertEqual(validate_researcher_profile(path), [])
            profile = load_researcher_profile(path)
            self.assertIsNone(profile.knowledge_state["Transformer"]["mathematical"])

    def test_transformer_conceptual_2_and_implementation_0_is_accepted(self):
        with TemporaryDirectory() as tmp:
            path = self.write_profile(Path(tmp))
            self.assertEqual(validate_researcher_profile(path), [])

    def test_implementation_does_not_get_inferred_from_conceptual(self):
        with TemporaryDirectory() as tmp:
            path = self.write_profile(Path(tmp))
            profile = load_researcher_profile(path)
            transformer = profile.knowledge_state["Transformer"]
            self.assertEqual(transformer["conceptual"], 2)
            self.assertEqual(transformer["implementation"], 0)

    def test_exposes_six_canonical_dimensions(self):
        self.assertEqual(
            CANONICAL_KNOWLEDGE_DIMENSIONS,
            ("awareness", "conceptual", "mathematical", "implementation", "application", "research"),
        )

    def test_preserves_knowledge_state_history_when_present(self):
        with TemporaryDirectory() as tmp:
            path = self.write_profile(
                Path(tmp),
                VALID_PROFILE
                + "knowledge_state_history:\n"
                + "  - concept: Transformer\n"
                + "    dimension: conceptual\n"
                + "    from: 1\n"
                + "    to: 2\n",
            )
            profile = load_researcher_profile(path)
            self.assertEqual(profile.knowledge_state_history[0]["concept"], "Transformer")

    def test_workspace_init_creates_profile(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_workspace(root)
            self.assertTrue((root / ".research/config/researcher-profile.yaml").exists())

    def test_validate_profile_reports_missing_file(self):
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "missing.yaml"
            errors = validate_researcher_profile(path)
            self.assertTrue(any("unable to read researcher profile" in error for error in errors))

    def test_workspace_init_does_not_overwrite_existing_profile(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "templates").mkdir()
            (root / "templates" / "researcher-profile.yaml").write_text(VALID_PROFILE, encoding="utf-8")
            existing = root / ".research/config/researcher-profile.yaml"
            existing.parent.mkdir(parents=True)
            existing.write_text("custom: true\n", encoding="utf-8")
            init_workspace(root)
            self.assertEqual(existing.read_text(encoding="utf-8"), "custom: true\n")

    def test_workspace_validation_detects_invalid_profile(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            profile = root / ".research/config/researcher-profile.yaml"
            profile.parent.mkdir(parents=True)
            profile.write_text(VALID_PROFILE.replace("implementation: 0", "implementation: 9"), encoding="utf-8")
            errors = validate_workspace(root)
            self.assertTrue(any("implementation must be null or integer 0..4" in error for error in errors))

    def test_workspace_validation_accepts_valid_profile(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            profile = root / ".research/config/researcher-profile.yaml"
            profile.parent.mkdir(parents=True)
            profile.write_text(VALID_PROFILE, encoding="utf-8")
            self.assertEqual(validate_workspace(root), [])


if __name__ == "__main__":
    unittest.main()
