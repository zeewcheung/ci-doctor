import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("ci_doctor", ROOT / "tools" / "ci_doctor.py")
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)

CLI_SPEC = importlib.util.spec_from_file_location(
    "classify_ci_failure", ROOT / "tools" / "classify_ci_failure.py"
)
CLASSIFIER_CLI = importlib.util.module_from_spec(CLI_SPEC)
assert CLI_SPEC.loader
CLI_SPEC.loader.exec_module(CLASSIFIER_CLI)


class ClassifierTests(unittest.TestCase):
    def test_synthetic_case_matrix(self):
        fixtures = ROOT / "tests" / "fixtures"
        cases = json.loads((fixtures / "cases.json").read_text())
        for name, expected in cases.items():
            with self.subTest(name=name):
                result = MODULE.classify((fixtures / f"{name}.log").read_text())
                self.assertEqual(expected["category"], result.category)
                self.assertEqual(expected["confidence"], result.confidence)
                self.assertGreater(result.line_number, 0)
                if expected["category"] == "unknown":
                    self.assertEqual("manual_review", result.disposition)
                    self.assertTrue(result.manual_review_required)

    def test_ignores_runner_epilogue(self):
        log = "AssertionError: values differ\nError: Process completed with exit code 1.\n"
        result = MODULE.classify(log)
        self.assertEqual("test", result.category)
        self.assertEqual(1, result.line_number)

    def test_conflicting_categories_abstain(self):
        log = "Resource not accessible by integration\nThe operation timed out after 10 minutes\n"
        result = MODULE.classify(log)
        self.assertEqual("unknown", result.category)
        self.assertEqual("low", result.confidence)
        self.assertEqual("manual_review", result.disposition)
        self.assertEqual(["permission", "timeout"], result.matched_categories)

    def test_free_classifier_writes_no_patch(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "classification.json"
            original = sys.argv
            try:
                sys.argv = [
                    "classify_ci_failure.py",
                    "--log",
                    str(ROOT / "tests" / "fixtures" / "permission.log"),
                    "--output",
                    str(output),
                ]
                self.assertEqual(0, CLASSIFIER_CLI.main())
            finally:
                sys.argv = original
            result = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual("permission", result["category"])
            self.assertEqual("classification_only", result["tool_scope"])
            self.assertFalse(result["candidate_fix_generated"])


if __name__ == "__main__":
    unittest.main()
