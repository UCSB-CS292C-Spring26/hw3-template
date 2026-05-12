#!/usr/bin/env python3
"""
Basic test suite for the SKILL.md analyzer.
Run: python3 -m pytest tests/test_basic.py -v

These tests verify your analyzer runs correctly and produces expected results
on the example skills. The grading will use DIFFERENT hidden skills.
"""

import subprocess
import sys
import os

ANALYZER = os.path.join(os.path.dirname(__file__), '..', 'analyzer.py')
SKILLS_DIR = os.path.join(os.path.dirname(__file__), '..', 'skills')

ALL_SKILLS = ['farmos_weather.md', 'passwordstore_broker.md',
              'office_quotes.md', 'email_daily_summary.md']


def run_analyzer(skill_file):
    """Run the analyzer on a skill file and return (stdout, stderr, returncode)."""
    filepath = os.path.join(SKILLS_DIR, skill_file)
    result = subprocess.run(
        [sys.executable, ANALYZER, filepath],
        capture_output=True, text=True
    )
    return result.stdout, result.stderr, result.returncode


# --- Basic functionality ---

def test_analyzer_runs():
    """Analyzer should run without crashing on each skill."""
    for skill in ALL_SKILLS + ['safe_example.md', 'bad_example.md']:
        stdout, stderr, rc = run_analyzer(skill)
        assert rc == 0, f"Analyzer crashed on {skill}: {stderr}"


def test_analyzer_on_directory():
    """Analyzer should accept a directory and process all skills."""
    result = subprocess.run(
        [sys.executable, ANALYZER, SKILLS_DIR],
        capture_output=True, text=True
    )
    assert result.returncode == 0
    assert 'Total:' in result.stdout


# --- Output format ---

def test_finding_format():
    """Each finding should have the required fields."""
    stdout, _, _ = run_analyzer('bad_example.md')
    if '[FINDING]' in stdout:
        assert 'Severity:' in stdout, "Finding missing 'Severity:' field"
        assert 'Evidence:' in stdout, "Finding missing 'Evidence:' field"
        assert 'Description:' in stdout, "Finding missing 'Description:' field"


# --- Safe example: no false positives ---

def test_safe_example_clean():
    """The safe example should produce NO findings (or very few)."""
    stdout, _, _ = run_analyzer('safe_example.md')
    finding_count = stdout.count('[FINDING]')
    assert finding_count == 0, (
        f"safe_example.md should have no findings, but got {finding_count}. "
        f"Your analyzer may have false positives."
    )


# --- Bad example: should catch obvious issues ---

def test_bad_example_has_findings():
    """The bad example should produce at least 2 findings."""
    stdout, _, _ = run_analyzer('bad_example.md')
    finding_count = stdout.count('[FINDING]')
    assert finding_count >= 2, (
        f"bad_example.md should have at least 2 findings, but got {finding_count}. "
        f"Check your detection rules."
    )


# --- Real skills: each has at least one issue ---

def test_each_real_skill_has_findings():
    """Each of the four real skills should produce at least one finding."""
    for skill in ALL_SKILLS:
        stdout, _, _ = run_analyzer(skill)
        assert '[FINDING]' in stdout, (
            f"No findings for {skill} — each skill has at least one issue"
        )


if __name__ == '__main__':
    tests = [test_analyzer_runs, test_analyzer_on_directory,
             test_finding_format, test_safe_example_clean,
             test_bad_example_has_findings, test_each_real_skill_has_findings]
    passed = 0
    for test in tests:
        try:
            test()
            print(f"  PASS: {test.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"  FAIL: {test.__name__} — {e}")
    print(f"\n{passed}/{len(tests)} tests passed")
