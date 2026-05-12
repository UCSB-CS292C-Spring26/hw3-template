#!/usr/bin/env python3
"""
Basic test suite for the SKILL.md analyzer.
Run: python3 -m pytest tests/test_basic.py -v

These tests verify your analyzer catches basic vulnerability patterns.
The grading will use DIFFERENT skills with SIMILAR patterns.
"""

import subprocess
import sys
import os

ANALYZER = os.path.join(os.path.dirname(__file__), '..', 'analyzer.py')
SKILLS_DIR = os.path.join(os.path.dirname(__file__), '..', 'skills')


def run_analyzer(skill_file):
    """Run the analyzer on a skill file and return (stdout, stderr, returncode)."""
    filepath = os.path.join(SKILLS_DIR, skill_file)
    result = subprocess.run(
        [sys.executable, ANALYZER, filepath],
        capture_output=True, text=True
    )
    return result.stdout, result.stderr, result.returncode


def test_analyzer_runs():
    """Analyzer should run without crashing on each skill."""
    for skill in ['farmos_weather.md', 'passwordstore_broker.md',
                   'office_quotes.md', 'email_daily_summary.md']:
        stdout, stderr, rc = run_analyzer(skill)
        assert rc == 0, f"Analyzer crashed on {skill}: {stderr}"


def test_analyzer_finds_something():
    """Analyzer should find at least one issue in each skill."""
    for skill in ['farmos_weather.md', 'passwordstore_broker.md',
                   'office_quotes.md', 'email_daily_summary.md']:
        stdout, _, _ = run_analyzer(skill)
        assert '[FINDING]' in stdout, f"No findings for {skill} — each skill has at least one vulnerability"


def test_finding_format():
    """Each finding should have the required fields."""
    stdout, _, _ = run_analyzer('farmos_weather.md')
    if '[FINDING]' in stdout:
        assert 'Class:' in stdout, "Finding missing 'Class:' field"
        assert 'Severity:' in stdout, "Finding missing 'Severity:' field"
        assert 'Evidence:' in stdout, "Finding missing 'Evidence:' field"


def test_v1_detects_raw_ip():
    """V1 should catch raw IP addresses in URLs."""
    stdout, _, _ = run_analyzer('farmos_weather.md')
    # farmos_weather has hardcoded IP 100.102.77.110
    assert 'V1' in stdout, "V1 (suspicious endpoints) should fire on farmos_weather"


def test_v2_detects_credentials():
    """V2 should catch credential exposure patterns."""
    stdout, _, _ = run_analyzer('passwordstore_broker.md')
    assert 'V2' in stdout, "V2 (credential exposure) should fire on passwordstore_broker"


def test_v3_detects_dangerous_exec():
    """V3 should catch dangerous execution primitives."""
    stdout, _, _ = run_analyzer('office_quotes.md')
    assert 'V3' in stdout, "V3 (dangerous execution) should fire on office_quotes"


def test_analyzer_on_directory():
    """Analyzer should accept a directory and process all skills."""
    result = subprocess.run(
        [sys.executable, ANALYZER, SKILLS_DIR],
        capture_output=True, text=True
    )
    assert result.returncode == 0
    assert 'Total:' in result.stdout


if __name__ == '__main__':
    # Simple runner without pytest
    tests = [test_analyzer_runs, test_analyzer_finds_something,
             test_finding_format, test_v1_detects_raw_ip,
             test_v2_detects_credentials, test_v3_detects_dangerous_exec,
             test_analyzer_on_directory]
    passed = 0
    for test in tests:
        try:
            test()
            print(f"  PASS: {test.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"  FAIL: {test.__name__} — {e}")
    print(f"\n{passed}/{len(tests)} tests passed")
