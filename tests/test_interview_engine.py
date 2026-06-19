import ast
import json
import subprocess
import sys
import unittest
import uuid
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
RUNTIME_DIR = ROOT / "tests" / "runtime"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import build_index
import pick
import profiles
import project_paths


class ProjectPathTests(unittest.TestCase):
    def test_project_root_is_stable(self):
        self.assertEqual(project_paths.PROJECT_ROOT, ROOT)

    def test_pick_runs_from_arbitrary_working_directory(self):
        completed = subprocess.run(
            [
                sys.executable,
                str(SRC / "pick.py"),
                "--profile", "backend",
                "--source", "八股",
                "--tag", "Java",
                "--no-history",
                "--seed", "7",
            ],
            cwd=str(RUNTIME_DIR),
            text=True,
            encoding="utf-8",
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        result = json.loads(completed.stdout)
        self.assertEqual(result["profile"], "backend")
        self.assertIn("Java", result["tags"])


class IndexTests(unittest.TestCase):
    def test_arbitrary_tags_are_preserved(self):
        token = uuid.uuid4().hex
        fundamentals = RUNTIME_DIR / (token + "-fundamentals.md")
        challenges = RUNTIME_DIR / (token + "-challenges.md")
        config_path = RUNTIME_DIR / (token + "-profiles.json")
        try:
            fundamentals.write_text(
                "# Test\n\n## Rust\n\n### Ownership\n- [Rust][basic] Explain ownership.\n",
                encoding="utf-8",
            )
            challenges.write_text("# Test\n\n1. [Rust] Build a queue.\n", encoding="utf-8")
            config_path.write_text(json.dumps({
                "schema_version": 1,
                "profiles": {
                    "rust": {
                        "fundamentals": [str(fundamentals)],
                        "coding_challenges": [str(challenges)],
                    }
                },
            }), encoding="utf-8")
            index = build_index.build_index(config_path)
        finally:
            for path in (fundamentals, challenges, config_path):
                if path.exists():
                    path.unlink()

        self.assertEqual(index["八股"][0]["tags"], ["Rust", "basic"])
        self.assertEqual(index["八股"][0]["profiles"], ["rust"])
        self.assertEqual(len(index["八股"][0]["qid"]), 16)

    def test_all_profiles_have_usable_question_counts(self):
        data = json.loads(project_paths.INDEX_FILE.read_text(encoding="utf-8"))
        config = profiles.load_profiles()
        for profile_id in config["profiles"]:
            fundamentals = [q for q in data["八股"] if profile_id in q["profiles"]]
            challenges = [q for q in data["手撕"] if profile_id in q["profiles"]]
            self.assertGreaterEqual(len(fundamentals), 25, profile_id)
            self.assertGreaterEqual(len(challenges), 5, profile_id)


class ProfileDetectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = profiles.load_profiles()

    def assert_profile(self, text, expected):
        result = profiles.detect_profile(text, self.config)
        self.assertEqual(result.get("profile"), expected, result)

    def test_backend_resume(self):
        self.assert_profile("## 基本信息\n- **期望岗位**：后端开发\n## 技术栈\nJava Spring MySQL Redis", "backend")

    def test_expected_position_alone_has_priority(self):
        self.assert_profile("- **期望岗位**：后端开发", "backend")

    def test_frontend_resume(self):
        self.assert_profile("## 基本信息\n- **期望岗位**：Web 前端\n## 技术栈\nTypeScript React Vite", "frontend")

    def test_client_resume(self):
        self.assert_profile("## 基本信息\n- **期望岗位**：Flutter 客户端\n## 技术栈\nDart Flutter Android", "client")

    def test_unity_resume(self):
        self.assert_profile("## 基本信息\n- **期望岗位**：Unity 客户端\n## 技术栈\nUnity UGUI Shader", "unity-client")

    def test_empty_resume_requires_selection(self):
        result = profiles.detect_profile("", self.config)
        self.assertTrue(result["needs_profile"])
        self.assertEqual(result["reason"], "no_match")

    def test_tie_requires_selection(self):
        result = profiles.detect_profile(
            "## 技术栈\nJava Spring JavaScript React", self.config
        )
        self.assertTrue(result["needs_profile"])


class WeightedHistoryTests(unittest.TestCase):
    def test_weight_rules(self):
        now = 40 * 24 * 60 * 60
        self.assertEqual(pick.question_weight(None, now), 1.5)
        self.assertAlmostEqual(
            pick.question_weight({"count": 1, "last_asked": now - 60}, now), 0.05
        )
        self.assertAlmostEqual(
            pick.question_weight({"count": 1, "last_asked": now - 3 * 24 * 60 * 60}, now),
            0.175,
        )
        self.assertAlmostEqual(
            pick.question_weight({"count": 1, "last_asked": now - 10 * 24 * 60 * 60}, now),
            0.35,
        )

    def test_history_is_isolated_by_profile(self):
        history = {"schema_version": 1, "profiles": {}}
        question = {"qid": "abc"}
        pick.record_exposure(history, "backend", question, now=100)
        self.assertIn("abc", history["profiles"]["backend"])
        self.assertNotIn("frontend", history["profiles"])

    def test_corrupt_history_falls_back(self):
        path = RUNTIME_DIR / (uuid.uuid4().hex + "-history.json")
        try:
            path.write_text("not-json", encoding="utf-8")
            history = pick.load_history(path)
        finally:
            if path.exists():
                path.unlink()
        self.assertEqual(history, {"schema_version": 1, "profiles": {}})

    def test_history_write_is_atomic_and_readable(self):
        path = RUNTIME_DIR / (uuid.uuid4().hex + "-history.json")
        try:
            history = {"schema_version": 1, "profiles": {"backend": {}}}
            self.assertTrue(pick.save_history(path, history))
            self.assertEqual(json.loads(path.read_text(encoding="utf-8")), history)
        finally:
            if path.exists():
                path.unlink()


class PythonCompatibilityTests(unittest.TestCase):
    def test_source_uses_python_38_grammar(self):
        for path in SRC.glob("*.py"):
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path), feature_version=(3, 8))


if __name__ == "__main__":
    unittest.main()
