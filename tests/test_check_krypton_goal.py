import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check-krypton-goal.py"


class CheckKryptonGoalTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp_dir.name)
        self.run_cmd(["git", "init", "-q", "-b", "main"])
        self.run_cmd(["git", "config", "user.email", "test@example.com"])
        self.run_cmd(["git", "config", "user.name", "Test User"])
        self.write("README.md", "# fixture\n")
        self.run_cmd(["git", "add", "README.md"])
        self.run_cmd(["git", "commit", "-q", "-m", "baseline"])

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def run_cmd(self, args: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            args,
            cwd=self.repo,
            text=True,
            capture_output=True,
            check=check,
        )

    def write(self, relative_path: str, content: str) -> None:
        path = self.repo / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def commit(self, message: str = "change") -> None:
        self.run_cmd(["git", "add", "."])
        self.run_cmd(["git", "commit", "-q", "-m", message])

    def check_goal(self) -> subprocess.CompletedProcess[str]:
        return self.run_cmd(
            ["python3", str(SCRIPT), "--base-ref", "HEAD~1"],
            check=False,
        )

    def add_complete_goal_package(self) -> None:
        self.write(
            "docs/goals/add-feature/PLAN.md",
            textwrap.dedent(
                """
                # Add Feature

                ## Truth Owner
                `src/app.py` owns this behavior.

                ## Deletion / Cutover
                This slice deletes nothing because it introduces the first path.

                ## Evidence Gate
                Run the focused regression test and inspect the changed output.
                """
            ).strip()
            + "\n",
        )
        self.write(
            "docs/goals/add-feature/GOAL.md",
            textwrap.dedent(
                """
                # Goal

                Preserve the truth owner, cut over to the intended path, and do
                not call the change complete until the evidence gate passes.
                """
            ).strip()
            + "\n",
        )
        self.write(
            "docs/goals/add-feature/EVIDENCE.md",
            textwrap.dedent(
                """
                # Evidence

                ## Acceptance Evidence
                Capture the actual command output or artifact.

                ## Verification
                Record the focused check that passed.
                """
            ).strip()
            + "\n",
        )

    def test_code_change_without_goal_package_fails(self) -> None:
        self.write("src/app.py", "print('hello')\n")
        self.commit()

        result = self.check_goal()

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("No Krypton goal package", result.stderr)

    def test_code_change_with_complete_goal_package_passes(self) -> None:
        self.write("src/app.py", "print('hello')\n")
        self.add_complete_goal_package()
        self.commit()

        result = self.check_goal()

        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

    def test_docs_only_change_passes_without_goal_package(self) -> None:
        self.write("docs/notes.md", "docs only\n")
        self.commit()

        result = self.check_goal()

        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

    def test_incomplete_goal_package_fails(self) -> None:
        self.write("src/app.py", "print('hello')\n")
        self.write(
            "docs/goals/add-feature/PLAN.md",
            "# Plan\n\n## Truth Owner\nsrc/app.py\n",
        )
        self.commit()

        result = self.check_goal()

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing GOAL.md", result.stderr)
        self.assertIn("missing EVIDENCE.md", result.stderr)


if __name__ == "__main__":
    unittest.main()
