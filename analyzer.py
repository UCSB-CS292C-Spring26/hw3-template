#!/usr/bin/env python3
"""
CS292C Homework 3: SKILL.md Static Analyzer
============================================
Analyze agent skill files for security issues.

Usage:
    python3 analyzer.py skills/farmos_weather.md      # single file
    python3 analyzer.py skills/                        # entire directory
"""

import sys
import os
import re
from dataclasses import dataclass, field


# ============================================================================
# Data Model
# ============================================================================

@dataclass
class Finding:
    """A single security finding."""
    skill_name: str
    severity: str          # CRITICAL, HIGH, MEDIUM, LOW
    location: str          # e.g., "line 15" or "section: API Base"
    description: str
    evidence: str          # the specific text that triggered the finding

    def __str__(self):
        return (
            f"[FINDING] {self.skill_name}\n"
            f"  Severity: {self.severity}\n"
            f"  Location: {self.location}\n"
            f"  Description: {self.description}\n"
            f"  Evidence: {self.evidence}\n"
        )


@dataclass
class SkillInfo:
    """Parsed information from a SKILL.md file."""
    filename: str
    name: str = ""
    description: str = ""
    raw_text: str = ""
    lines: list = field(default_factory=list)
    urls: list = field(default_factory=list)          # (line_num, url) pairs
    code_blocks: list = field(default_factory=list)   # (line_num, code) pairs
    commands: list = field(default_factory=list)       # (line_num, cmd) pairs


# ============================================================================
# Parsing — extracts structured info from a SKILL.md file.
# You may modify or extend this section as needed.
# ============================================================================

def parse_skill(filepath: str) -> SkillInfo:
    """Parse a SKILL.md file and extract structured information."""
    with open(filepath, 'r', encoding='utf-8') as f:
        raw_text = f.read()

    lines = raw_text.split('\n')
    skill = SkillInfo(
        filename=os.path.basename(filepath),
        raw_text=raw_text,
        lines=lines,
    )

    # Extract skill name from frontmatter or filename
    name_match = re.search(r'^name:\s*["\']?(.+?)["\']?\s*$', raw_text, re.MULTILINE)
    if name_match:
        skill.name = name_match.group(1)
    else:
        skill.name = os.path.splitext(skill.filename)[0]

    # Extract description from frontmatter
    desc_match = re.search(r'^description:\s*["\']?(.+?)["\']?\s*$', raw_text, re.MULTILINE)
    if desc_match:
        skill.description = desc_match.group(1)

    # Extract all URLs with line numbers
    url_pattern = re.compile(r'(https?://[^\s\)\"\'`>]+)')
    for i, line in enumerate(lines, 1):
        for match in url_pattern.finditer(line):
            skill.urls.append((i, match.group(1)))

    # Extract code blocks with line numbers
    in_code_block = False
    code_start = 0
    code_lines = []
    for i, line in enumerate(lines, 1):
        if line.strip().startswith('```'):
            if in_code_block:
                skill.code_blocks.append((code_start, '\n'.join(code_lines)))
                code_lines = []
                in_code_block = False
            else:
                in_code_block = True
                code_start = i
        elif in_code_block:
            code_lines.append(line)

    return skill


# ============================================================================
# Detection Rules
#
# TODO: Implement your detection logic below.
#
# You decide what to check for. Read the skills in skills/ carefully,
# identify the security issues, then implement detection functions that
# would generalize to other skills with similar problems.
#
# You can organize your code however you like — one big function, many
# small functions, or a class-based approach. The only requirement is
# that analyze_skill() returns a list of Finding objects.
# ============================================================================

def analyze_skill(filepath: str) -> list[Finding]:
    """
    Run all checks on a single SKILL.md file.

    TODO: Implement your detection logic here.
    Parse the skill, apply your rules, and return findings.
    """
    skill = parse_skill(filepath)
    findings = []

    # TODO: Add your detection rules here.
    # Example structure (delete this and replace with your own):
    #
    # for line_num, url in skill.urls:
    #     if some_check(url):
    #         findings.append(Finding(
    #             skill_name=skill.name,
    #             severity="HIGH",
    #             location=f"line {line_num}",
    #             description="Description of the issue",
    #             evidence=url,
    #         ))

    return findings


# ============================================================================
# Main — do not modify
# ============================================================================

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 analyzer.py <skill.md or directory>")
        print("Example: python3 analyzer.py skills/farmos_weather.md")
        print("         python3 analyzer.py skills/")
        sys.exit(1)

    target = sys.argv[1]

    if os.path.isdir(target):
        files = sorted([
            os.path.join(target, f)
            for f in os.listdir(target)
            if f.endswith('.md') and not f.startswith('README')
        ])
    elif os.path.isfile(target):
        files = [target]
    else:
        print(f"Error: {target} is not a file or directory")
        sys.exit(1)

    total_findings = 0
    for filepath in files:
        print(f"{'='*60}")
        print(f"Analyzing: {filepath}")
        print(f"{'='*60}")

        findings = analyze_skill(filepath)
        total_findings += len(findings)

        if findings:
            for f in findings:
                print(f)
        else:
            print("  No findings.\n")

    print(f"{'='*60}")
    print(f"Total: {total_findings} finding(s) across {len(files)} skill(s)")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
