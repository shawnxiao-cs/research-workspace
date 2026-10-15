import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from research_workspace.onboarding import LABELS, onboard, parse_topics, render_profile  # noqa: E402
from research_workspace.profile import load_plain_yaml, validate_researcher_profile  # noqa: E402

GENERIC_PROFILE = """profile_version: 0.1
researcher:
  id: USER-0001
  stage: doctoral
  background:
    - Computer Science
  research_interests:
    - Image Reconstruction
  research_goals:
    - Compare reconstruction methods
learning_progress:
  sources:
    - Technical papers
knowledge_state:
  CNN:
    conceptual: 2
    implementation: 1
    mathematical: null
    application: null
    research: null
  RNN:
    conceptual: 1
    implementation: null
  Self-Attention:
    conceptual: 2
    implementation: 2
  Transformer:
    conceptual: 2
    implementation: 4
    mathematical: 1
    application: 3
    research: 2
provenance:
  type: human
  review_status: accepted
  source_refs: []
"""


class OnboardingTests(unittest.TestCase):
    def setUp(self):
        self.tmp = TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.outputs = []

    def run_flow(self, answers, language="en"):
        values = iter(answers)
        def read(prompt):
            try:
                return next(values)
            except StopIteration as exc:
                raise AssertionError(f"unexpected prompt: {prompt}") from exc
        result = onboard(self.root, language, read, self.outputs.append)
        return result

    def write_existing(self, text=None):
        path = self.root / ".research/config/researcher-profile.yaml"
        path.parent.mkdir(parents=True, exist_ok=True)
        if text is None:
            text = GENERIC_PROFILE
        path.write_text(text, encoding="utf-8")
        return path

    def test_stage_topics_are_rejected_and_reprompted(self):
        answers = ["CNN, RNN", "3", "", "", "", "", "", "y"]
        self.run_flow(answers)
        self.assertIn("not a stage", " ".join(self.outputs))
        saved = load_plain_yaml(self.root / ".research/config/researcher-profile.yaml")
        self.assertEqual(saved["researcher"]["stage"], "doctoral")

    def test_stage_other_choice_accepts_a_single_custom_stage(self):
        answers = ["8", "Research engineer", "", "", "", "", "", "y"]
        self.run_flow(answers)
        data = load_plain_yaml(self.root / ".research/config/researcher-profile.yaml")
        self.assertEqual(data["researcher"]["stage"], "Research engineer")

    def test_topic_parser_trims_removes_empty_and_deduplicates_case_insensitively(self):
        self.assertEqual(parse_topics(" CNN, , RNN, cnn , Self-Attention, Transformer "), ["CNN", "RNN", "Self-Attention", "Transformer"])
        self.assertEqual(parse_topics(" , , "), [])
        self.assertIsNone(parse_topics("CNN, 2, RNN"))

    def test_topic_list_is_confirmed_and_can_be_reentered(self):
        answers = ["3", "", "", "", "", "CNN, RNN", "r", "Transformer", "y", "", "3", "1", "y"]
        self.run_flow(answers)
        output = "\n".join(self.outputs)
        self.assertIn("CNN, RNN", output)
        self.assertIn("Transformer", output)
        data = load_plain_yaml(self.root / ".research/config/researcher-profile.yaml")
        self.assertEqual(list(data["knowledge_state"]), ["Transformer"])

    def test_quick_assessment_keeps_conceptual_two_implementation_zero_and_other_dimensions_null(self):
        answers = ["3", "", "", "", "Papers", "Transformer", "y", "", "3", "1", "y"]
        self.run_flow(answers)
        path = self.root / ".research/config/researcher-profile.yaml"
        data = load_plain_yaml(path)
        self.assertEqual(validate_researcher_profile(path), [])
        self.assertEqual(data["knowledge_state"]["Transformer"], {
            "awareness": None, "conceptual": 2, "mathematical": None,
            "implementation": 0, "application": None, "research": None,
        })

    def test_invalid_menu_input_is_rejected_without_shifting_later_answers(self):
        answers = ["3", "", "", "", "", "Transformer", "y", "", "CNN, RNN", "3", "1", "y"]
        self.run_flow(answers)
        data = load_plain_yaml(self.root / ".research/config/researcher-profile.yaml")
        state = data["knowledge_state"]["Transformer"]
        self.assertEqual(state["conceptual"], 2)
        self.assertEqual(state["implementation"], 0)
        self.assertIn("Enter a menu choice from 1–6", " ".join(self.outputs))

    def test_detailed_mode_assesses_all_dimensions_independently(self):
        answers = ["3", "", "", "", "", "Transformer", "y", "2", "6", "3", "6", "1", "6", "6", "y"]
        self.run_flow(answers)
        state = load_plain_yaml(self.root / ".research/config/researcher-profile.yaml")["knowledge_state"]["Transformer"]
        self.assertEqual(state["conceptual"], 2)
        self.assertIsNone(state["mathematical"])
        self.assertEqual(state["implementation"], 0)
        self.assertIsNone(state["application"])
        self.assertIsNone(state["research"])

    def test_reading_source_never_increases_implementation(self):
        answers = ["3", "", "", "", "Read Transformer papers", "Transformer", "y", "", "3", "1", "y"]
        self.run_flow(answers)
        state = load_plain_yaml(self.root / ".research/config/researcher-profile.yaml")["knowledge_state"]["Transformer"]
        self.assertEqual((state["conceptual"], state["implementation"]), (2, 0))

    def test_cancellation_leaves_existing_profile_unchanged(self):
        path = self.write_existing()
        original = path.read_bytes()
        self.run_flow(["2", "", "c"])
        self.assertEqual(path.read_bytes(), original)
        self.assertIn("Cancelled; profile was not changed", " ".join(self.outputs))

    def test_empty_topic_input_preserves_existing_topics_and_assessments(self):
        path = self.write_existing()
        original_data = load_plain_yaml(path)
        self.run_flow(["2", "", "y"])
        result = load_plain_yaml(path)
        self.assertEqual(result["knowledge_state"], original_data["knowledge_state"])
        output = " ".join(self.outputs)
        self.assertIn("existing topics and assessments will be preserved", output)
        self.assertIn("nothing will be reassessed", output)

    def test_quick_reassessment_updates_existing_transformer_facts_after_confirmation(self):
        path = self.write_existing()
        answers = ["2", "Transformer", "y", "1", "3", "1", "y", "correcting test data"]
        self.run_flow(answers)
        state = load_plain_yaml(path)["knowledge_state"]["Transformer"]
        self.assertEqual(state["conceptual"], 2)
        self.assertEqual(state["implementation"], 0)
        self.assertIsNone(state["mathematical"])
        self.assertIsNone(state["application"])
        self.assertIsNone(state["research"])
        self.assertIn("Quick Reassessment", " ".join(self.outputs))

    def test_quick_reassessment_reset_is_only_written_after_confirmation(self):
        path = self.write_existing()
        original = path.read_bytes()
        answers = ["2", "Transformer", "y", "1", "3", "1", "c"]
        self.run_flow(answers)
        self.assertEqual(path.read_bytes(), original)
        preview = "\n".join(self.outputs)
        self.assertIn("Mathematical understanding: Seen related notation or equations → Not assessed", preview)
        self.assertIn("Cancelled; profile was not changed", preview)

    def test_confirmation_saves_validated_profile(self):
        self.run_flow(["3", "", "", "", "", "Transformer", "y", "", "3", "1", "y"])
        path = self.root / ".research/config/researcher-profile.yaml"
        self.assertTrue(path.exists())
        self.assertEqual(validate_researcher_profile(path), [])

    def test_update_preserves_unrelated_fields_and_existing_history(self):
        path = self.write_existing()
        with path.open("a", encoding="utf-8") as stream:
            stream.write("knowledge_state_history:\n  - concept: CNN\n    dimension: conceptual\n    from: 1\n    to: 2\n")
        answers = ["2", "Transformer", "y", "1", "", "1", "y", "review"]
        # Only Transformer is reassessed; unrelated fields and previous history remain.
        self.run_flow(answers)
        data = load_plain_yaml(path)
        self.assertEqual(data["researcher"]["research_interests"][0], "Image Reconstruction")
        self.assertEqual(data["knowledge_state"]["Transformer"]["conceptual"], 2)
        self.assertEqual(data["knowledge_state"]["Transformer"]["implementation"], 0)
        self.assertEqual(data["knowledge_state_history"][0]["concept"], "CNN")

    def test_edit_mode_changes_only_selected_section(self):
        path = self.write_existing()
        before = load_plain_yaml(path)
        answers = ["2", "", "e", "2", "Satellite Imaging", "Study Mamba", "y"]
        self.run_flow(answers)
        after = load_plain_yaml(path)
        self.assertEqual(after["researcher"]["research_interests"], ["Satellite Imaging"])
        self.assertEqual(after["researcher"]["research_goals"], ["Study Mamba"])
        self.assertEqual(after["researcher"]["stage"], before["researcher"]["stage"])
        self.assertEqual(after["researcher"]["background"], before["researcher"]["background"])
        self.assertEqual(after["learning_progress"], before["learning_progress"])
        self.assertEqual(after["knowledge_state"], before["knowledge_state"])

    def test_changed_known_value_has_default_provenance_and_optional_reason(self):
        path = self.write_existing()
        answers = ["2", "Transformer", "y", "1", "4", "1", "y", "updated after review"]
        self.run_flow(answers)
        data = load_plain_yaml(path)
        record = next(item for item in data["knowledge_state_history"] if item["dimension"] == "conceptual")
        self.assertEqual(record["provenance"], "user_self_report")
        self.assertEqual(record["reason"], "updated after review")
        self.assertEqual((record["from"], record["to"]), (2, 3))

    def test_previously_unassessed_value_does_not_create_history(self):
        template = GENERIC_PROFILE.replace("provenance:\n", "  Mamba:\n    conceptual: null\n    implementation: null\nprovenance:\n")
        self.write_existing(template)
        answers = ["2", "Mamba", "y", "1", "3", "1", "y"]
        self.run_flow(answers)
        path = self.root / ".research/config/researcher-profile.yaml"
        data = load_plain_yaml(path)
        self.assertNotIn("knowledge_state_history", data)

    def test_unchanged_values_do_not_create_history(self):
        profile = GENERIC_PROFILE.replace("implementation: 4", "implementation: 0").replace(
            "    mathematical: 1\n    application: 3\n    research: 2",
            "    mathematical: null\n    application: null\n    research: null",
        )
        path = self.write_existing(profile)
        answers = ["2", "Transformer", "y", "1", "3", "1", "y"]
        self.run_flow(answers)
        data = load_plain_yaml(path)
        self.assertNotIn("knowledge_state_history", data)

    def test_keyboard_interrupt_is_localized_and_leaves_profile_untouched(self):
        path = self.write_existing()
        original = path.read_bytes()
        outputs = []
        calls = 0
        def interrupted(_prompt):
            nonlocal calls
            calls += 1
            if calls == 2:
                raise KeyboardInterrupt
            return "2"
        self.assertEqual(onboard(self.root, "zh", interrupted, outputs.append), 0)
        self.assertEqual(path.read_bytes(), original)
        self.assertIn("已取消", " ".join(outputs))
        self.assertNotIn("Traceback", " ".join(outputs))

    def test_chinese_and_english_labels_and_verbose_output(self):
        self.assertEqual(LABELS["zh"]["not_assessed"], "尚未评估")
        self.assertEqual(LABELS["en"]["not_assessed"], "Not assessed")
        data = {"knowledge_state": {"Transformer": {"conceptual": 2, "implementation": 0, "mathematical": None}}}
        self.assertIn("已理解", render_profile(data, "zh"))
        self.assertIn("Never implemented", render_profile(data, "en"))
        self.assertIn("(0)", render_profile(data, "en", verbose=True))

    def test_live_profile_is_git_ignored(self):
        result = subprocess.run(
            ["git", "check-ignore", ".research/config/researcher-profile.yaml"],
            cwd=ROOT, capture_output=True, text=True, check=False,
        )
        self.assertEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
