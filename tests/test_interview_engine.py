import ast
import json
import random
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
import difficulty
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

    def test_challenge_qid_ignores_difficulty_tag(self):
        token = uuid.uuid4().hex
        basic_file = RUNTIME_DIR / (token + "-basic.md")
        advanced_file = RUNTIME_DIR / (token + "-advanced.md")
        try:
            basic_file.write_text(
                "# Test\n\n1. [Algorithms][basic] Build a queue.\n", encoding="utf-8"
            )
            advanced_file.write_text(
                "# Test\n\n1. [Algorithms][advanced] Build a queue.\n", encoding="utf-8"
            )
            basic = build_index.parse_challenges(basic_file, "test")[0]
            advanced = build_index.parse_challenges(advanced_file, "test")[0]
        finally:
            for path in (basic_file, advanced_file):
                if path.exists():
                    path.unlink()

        self.assertEqual(basic["qid"], advanced["qid"])
        self.assertNotEqual(basic["tags"], advanced["tags"])

    def test_mobile_crosscutting_questions_are_shared(self):
        data = json.loads(project_paths.INDEX_FILE.read_text(encoding="utf-8"))
        question = next(
            item
            for item in data["八股"]
            if item["text"] == "ReAct Agent 的核心思想是什么？"
        )
        self.assertEqual(set(question["profiles"]), {"android-native", "flutter"})

    def test_common_questions_are_shared_by_all_profiles(self):
        data = json.loads(project_paths.INDEX_FILE.read_text(encoding="utf-8"))
        expected_profiles = set(profiles.load_profiles()["profiles"])
        algorithm = next(
            item
            for item in data["八股"]
            if item["text"] == "时间复杂度和空间复杂度分别衡量什么？"
        )
        networking = next(
            item
            for item in data["八股"]
            if item["text"] == "TCP 和 UDP 的主要区别是什么？"
        )
        challenge = next(
            item
            for item in data["手撕"]
            if item["text"] == "实现二分查找，并说明循环边界如何确定"
        )
        self.assertEqual(set(algorithm["profiles"]), expected_profiles)
        self.assertEqual(set(networking["profiles"]), expected_profiles)
        self.assertEqual(set(challenge["profiles"]), expected_profiles)

    def test_every_profile_can_pick_common_domains(self):
        data = json.loads(project_paths.INDEX_FILE.read_text(encoding="utf-8"))
        for profile_id in profiles.load_profiles()["profiles"]:
            fundamentals = [
                item
                for item in data["八股"]
                if profile_id in item["profiles"]
            ]
            challenges = [
                item
                for item in data["手撕"]
                if profile_id in item["profiles"]
            ]
            self.assertTrue(
                any("Algorithms" in item["tags"] for item in fundamentals), profile_id
            )
            self.assertTrue(
                any("ComputerNetworking" in item["tags"] for item in fundamentals),
                profile_id,
            )
            self.assertTrue(
                any("Algorithms" in item["tags"] for item in challenges), profile_id
            )


class ProfileDetectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = profiles.load_profiles()

    def test_configured_profiles(self):
        self.assertEqual(
            set(self.config["profiles"]),
            {"unity-client", "backend", "frontend", "desktop-client", "android-native", "flutter"},
        )

    def assert_profile(self, text, expected):
        result = profiles.detect_profile(text, self.config)
        self.assertEqual(result.get("profile"), expected, result)

    def test_backend_resume(self):
        self.assert_profile("## 基本信息\n- **期望岗位**：后端开发\n## 技术栈\nJava Spring MySQL Redis", "backend")

    def test_expected_position_alone_has_priority(self):
        self.assert_profile("- **期望岗位**：后端开发", "backend")

    def test_frontend_resume(self):
        self.assert_profile("## 基本信息\n- **期望岗位**：Web 前端\n## 技术栈\nTypeScript React Vite", "frontend")

    def test_desktop_client_resume(self):
        self.assert_profile("## 基本信息\n- **期望岗位**：桌面客户端开发\n## 技术栈\nC# WPF WinUI", "desktop-client")

    def test_android_native_resume(self):
        self.assert_profile("## 基本信息\n- **期望岗位**：Android 原生开发\n## 技术栈\nKotlin Jetpack Compose", "android-native")

    def test_flutter_resume(self):
        self.assert_profile("## 基本信息\n- **期望岗位**：Flutter 开发\n## 技术栈\nDart Flutter Riverpod", "flutter")

    def test_generic_client_resume_requires_selection(self):
        result = profiles.detect_profile("- **期望岗位**：客户端开发", self.config)
        self.assertTrue(result["needs_profile"])

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


class DifficultyPolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = profiles.load_profiles()

    def test_chinese_aliases_resolve_to_canonical_context(self):
        context = difficulty.resolve_difficulty_context(
            self.config, "大厂", "正职"
        )
        self.assertEqual(context["company_size"], "large")
        self.assertEqual(context["position_level"], "full-time")
        self.assertEqual(context["weights"]["advanced"], 55.0)

    def test_seed_makes_policy_selection_reproducible(self):
        first = pick.resolve_requested_difficulty(
            self.config, "medium", "intern", "", random.Random(17)
        )
        second = pick.resolve_requested_difficulty(
            self.config, "medium", "intern", "", random.Random(17)
        )
        self.assertEqual(first["level"], second["level"])
        self.assertEqual(first["source"], "policy")

    def test_explicit_level_overrides_policy(self):
        context = pick.resolve_requested_difficulty(
            self.config, "small", "intern", "advanced", random.Random(1)
        )
        self.assertEqual(context["level"], "advanced")
        self.assertEqual(context["source"], "explicit")

    def test_incomplete_context_is_rejected(self):
        result = pick.resolve_requested_difficulty(
            self.config, "large", "", "", random.Random(1)
        )
        self.assertEqual(result["error"], "incomplete_difficulty_context")

    def test_mobile_networking_is_capped_at_intermediate(self):
        profile = self.config["profiles"]["android-native"]
        result = difficulty.apply_tag_difficulty_cap(
            "advanced", ["ComputerNetworking"], profile
        )
        self.assertEqual(result["level"], "intermediate")
        self.assertEqual(result["requested_level"], "advanced")
        self.assertEqual(result["capped_by"], "ComputerNetworking")

    def test_backend_networking_keeps_advanced_level(self):
        profile = self.config["profiles"]["backend"]
        result = difficulty.apply_tag_difficulty_cap(
            "advanced", ["ComputerNetworking"], profile
        )
        self.assertEqual(result, {"level": "advanced"})

    def test_cli_applies_profile_tag_cap(self):
        completed = subprocess.run(
            [
                sys.executable,
                str(SRC / "pick.py"),
                "--profile", "android-native",
                "--source", "八股",
                "--tag", "ComputerNetworking",
                "--level", "advanced",
                "--no-history",
                "--seed", "3",
                "--fallback",
            ],
            cwd=str(RUNTIME_DIR),
            text=True,
            encoding="utf-8",
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        result = json.loads(completed.stdout)
        self.assertEqual(result["difficulty"]["level"], "intermediate")
        self.assertEqual(result["difficulty"]["requested_level"], "advanced")
        self.assertIn("intermediate", {tag.lower() for tag in result["tags"]})

    def test_cli_uses_policy_for_coding_challenge(self):
        completed = subprocess.run(
            [
                sys.executable,
                str(SRC / "pick.py"),
                "--profile", "backend",
                "--source", "手撕",
                "--company-size", "大厂",
                "--position-level", "正职",
                "--no-history",
                "--seed", "9",
                "--fallback",
            ],
            cwd=str(RUNTIME_DIR),
            text=True,
            encoding="utf-8",
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        result = json.loads(completed.stdout)
        selected_level = result["difficulty"]["level"]
        self.assertIn(selected_level, {tag.lower() for tag in result["tags"]})
        self.assertEqual(result["difficulty"]["company_size"], "large")
        self.assertEqual(result["difficulty"]["position_level"], "full-time")


class PythonCompatibilityTests(unittest.TestCase):
    def test_source_uses_python_38_grammar(self):
        for path in SRC.glob("*.py"):
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path), feature_version=(3, 8))


if __name__ == "__main__":
    unittest.main()
