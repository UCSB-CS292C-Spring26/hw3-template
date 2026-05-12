#!/usr/bin/env python3
"""
CS292C Homework 3: SKILL.md Static Analyzer
============================================
Analyze agent skill files for security vulnerabilities.

Usage:
    python3 analyzer.py skills/farmos_weather.md      # single file
    python3 analyzer.py skills/                        # entire directory

Vulnerability Classes:
    V1 - Hardcoded suspicious endpoints
    V2 - Credential exposure
    V3 - Dangerous execution primitives
    V4 - Unconfirmed destructive operations
    V5 - Data exfiltration patterns
"""

import sys
import os
import re
from dataclasses import dataclass, field
from typing import Optional


# ============================================================================
# Data Model
# ============================================================================

@dataclass
class Finding:
    """A single security finding."""
    skill_name: str
    vuln_class: str        # V1, V2, V3, V4, V5, ...
    severity: str          # CRITICAL, HIGH, MEDIUM, LOW
    location: str          # e.g., "line 15" or "section: API Base"
    description: str
    evidence: str          # the specific text that triggered the finding

    def __str__(self):
        return (
            f"[FINDING] {self.skill_name}\n"
            f"  Class: {self.vuln_class}\n"
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
# Parsing
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

    # Extract shell/command patterns with line numbers
    cmd_pattern = re.compile(
        r'(?:^|\n)\s*(?:```(?:bash|sh|shell)?\s*\n)?(.*?(?:curl|wget|npm|pip|brew|apt|'
        r'eval|exec|bash|sh|chmod|chown|rm\s|kill|launchctl|crontab|systemctl|'
        r'gpg|pass\s|openssl|ssh|scp).*?)(?:\n|$)',
        re.IGNORECASE
    )
    for i, line in enumerate(lines, 1):
        for match in cmd_pattern.finditer(line):
            skill.commands.append((i, match.group(1).strip()))

    return skill


# ============================================================================
# Detection Rules
#
# Implement each check_* function below. Each should return a list of Finding
# objects for any vulnerabilities detected.
# ============================================================================

def check_v1_suspicious_endpoints(skill: SkillInfo) -> list[Finding]:
    """
    V1: Hardcoded suspicious endpoints

    Look for:
    - Raw IP addresses in URLs (instead of domain names)
    - IPs in private/CGNAT ranges:
        - 10.0.0.0/8 (RFC 1918)
        - 172.16.0.0/12 (RFC 1918)
        - 192.168.0.0/16 (RFC 1918)
        - 100.64.0.0/10 (RFC 6598, CGNAT / Tailscale)
        - 127.0.0.0/8 (loopback)
    - Plaintext HTTP for anything that handles sensitive data
    - Hardcoded non-standard ports

    TODO: Implement this function.
    """
    findings = []

    # TODO: Check each URL in skill.urls for suspicious patterns
    # for line_num, url in skill.urls:
    #     ...

    return findings


def check_v2_credential_exposure(skill: SkillInfo) -> list[Finding]:
    """
    V2: Credential exposure

    Look for:
    - Passwords, tokens, secrets, API keys passed as CLI arguments
    - Credentials in environment variables exposed to child processes
    - Secrets written to world-readable files
    - Hardcoded credentials in the skill text
    - Patterns like: --password, --token, -p <secret>, API_KEY=, etc.

    TODO: Implement this function.
    """
    findings = []

    # TODO: Scan skill.raw_text and skill.commands for credential patterns

    return findings


def check_v3_dangerous_execution(skill: SkillInfo) -> list[Finding]:
    """
    V3: Dangerous execution primitives

    Look for:
    - eval(), exec(), Function() in any language
    - curl | sh, wget | bash (pipe-to-shell)
    - npm install -g, pip install (global installs)
    - subprocess/os.system with unsanitized input
    - Network-fetched content fed into execution contexts
      (download → write to disk → execute/render)

    TODO: Implement this function.
    """
    findings = []

    # TODO: Check skill.raw_text, skill.code_blocks, and skill.commands

    return findings


def check_v4_unconfirmed_destructive(skill: SkillInfo) -> list[Finding]:
    """
    V4: Unconfirmed destructive operations

    Look for:
    - File deletion (rm, unlink, shutil.rmtree)
    - System config changes (chmod, chown, /etc/ modifications)
    - Package installation without confirmation
    - Persistence mechanisms:
        - launchd plists (launchctl load)
        - cron jobs (crontab)
        - systemd services
        - login items / startup scripts
    - Operations that should require "confirm with user" but don't

    TODO: Implement this function.
    """
    findings = []

    # TODO: Check for persistence and destructive patterns

    return findings


def check_v5_data_exfiltration(skill: SkillInfo) -> list[Finding]:
    """
    V5: Data exfiltration patterns

    Look for:
    - Sensitive data (file paths, credentials, user data) flowing to
      network endpoints
    - Local file reads followed by network writes
    - User-identifying information sent to third-party services
    - Base64 encoding of file contents (common exfil obfuscation)
    - Patterns: read file → encode → POST to external service

    TODO: Implement this function.
    """
    findings = []

    # TODO: Look for data flow from local sources to network sinks

    return findings


# ============================================================================
# Main Analysis Pipeline
# ============================================================================

def analyze_skill(filepath: str) -> list[Finding]:
    """Run all checks on a single SKILL.md file."""
    skill = parse_skill(filepath)

    findings = []
    findings.extend(check_v1_suspicious_endpoints(skill))
    findings.extend(check_v2_credential_exposure(skill))
    findings.extend(check_v3_dangerous_execution(skill))
    findings.extend(check_v4_unconfirmed_destructive(skill))
    findings.extend(check_v5_data_exfiltration(skill))

    return findings


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
