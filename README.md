# CS292C Homework 3: Security Audit of Agent Skills

**Out:** Lecture 11 (5/5) | **Due:** Lecture 16 (5/21) 11:59pm | **Weight:** 12%

## Overview

Agent skills (SKILL.md files) are the executable infrastructure that governs how coding agents operate. As we saw in Lectures 12–13, skills published on registries like ClawHub can contain **zero-day vulnerabilities** — harmful behaviors that evade both VirusTotal and LLM-based reviewers.

In this assignment, you will build a **static analysis tool** that automatically inspects SKILL.md files and flags potentially harmful behaviors. Your analyzer must detect real vulnerability patterns found in the wild, without prior knowledge of specific skills.

**The challenge:** The skills in `skills/` look innocent on the surface. They were all published on ClawHub and passed both VirusTotal and ClawHub's own safety scanners. Your job is to build a tool that catches what those scanners missed.

**Language:** Python 3.10+. No external dependencies required (regex, ast, and standard library are sufficient). You may optionally use `z3-solver` if your analysis benefits from constraint solving.

## Setup

```bash
# No special setup needed — just Python 3.10+
python3 --version  # should be 3.10 or higher

# Run your analyzer on a single skill
python3 analyzer.py skills/farmos_weather.md

# Run on all provided skills
python3 analyzer.py skills/
```

## Submission

Push all work to this repo before the deadline:
1. `analyzer.py` — your static analysis tool
2. `report.md` — findings report for the provided skills
3. Run `bash check.sh` before submitting.

## The Skills

Four SKILL.md files are provided in `skills/`. Each is a real skill that was published on ClawHub and passed existing safety scanners. **At least one vulnerability exists in each skill.** Your analyzer should find them.

| Skill | Description | Surface Appearance |
|-------|-------------|-------------------|
| `farmos_weather.md` | Weather data for farm fields | Simple API wrapper |
| `passwordstore_broker.md` | Password manager bridge | Credential management tool |
| `office_quotes.md` | The Office (US) quote generator | Fun/entertainment skill |
| `email_daily_summary.md` | Daily email digest | Productivity automation |

**Important:** You are NOT told what the vulnerabilities are. Discovering them is part of the assignment.

## Your Task

### Part 1: Build the Analyzer (50 points)

Implement `analyzer.py` — a static analysis tool that reads a SKILL.md file and outputs a structured report of potential security issues.

Your analyzer must check for **at least the following vulnerability classes:**

| ID | Vulnerability Class | Description |
|----|-------------------|-------------|
| `V1` | **Hardcoded suspicious endpoints** | URLs or IPs that raise red flags: raw IPs instead of domain names, non-publicly-routable addresses, plaintext HTTP for sensitive operations, or non-standard ports |
| `V2` | **Credential exposure** | Secrets, passwords, API keys, or tokens passed via command-line arguments, environment variables, or written to world-readable locations |
| `V3` | **Dangerous execution primitives** | Patterns like `eval`, `exec`, `curl\|sh`, `npm install -g`, or subprocess calls with unsanitized input from network sources |
| `V4` | **Unconfirmed destructive operations** | File deletion, system configuration changes, package installation, or persistence mechanisms (cron, launchd, systemd) without explicit user confirmation |
| `V5` | **Data exfiltration patterns** | Sensitive data (file contents, credentials, user data) flowing to network endpoints, especially third-party services or hardcoded destinations |

You may add additional vulnerability classes beyond these five.

**Output format:** Your analyzer must print structured output for each finding:

```
[FINDING] <skill_name>
  Class: <V1|V2|V3|V4|V5|...>
  Severity: <CRITICAL|HIGH|MEDIUM|LOW>
  Location: <line number or section>
  Description: <what was found>
  Evidence: <the specific text/pattern that triggered the finding>
```

Example:
```
[FINDING] example_skill
  Class: V1
  Severity: HIGH
  Location: line 15
  Description: Hardcoded raw IP address used as API endpoint
  Evidence: http://192.168.1.100:8080/api/data
```

### Part 2: Analyze the Skills (30 points)

Run your analyzer on all four provided skills and write up your findings in `report.md`.

For each skill, your report must include:
1. **Summary:** What does the skill claim to do? (1–2 sentences)
2. **Findings:** List each vulnerability found, with class, severity, and evidence
3. **Attack scenario:** For the most critical finding, describe a concrete attack: who is the attacker, what do they gain, and what is the blast radius? (3–5 sentences)
4. **Risk assessment:** Would you approve this skill for installation? Why or why not? (1–2 sentences)

### Part 3: Defense Recommendations (20 points)

In `report.md`, add a final section answering:

1. **(8 pts)** For each vulnerability class (V1–V5), propose a **specific, implementable** defense that an agent runtime could enforce. Be concrete — "validate URLs" is too vague; specify exactly what the runtime should check and reject.

2. **(6 pts)** Your analyzer uses static analysis (pattern matching on text). Describe **two limitations** of this approach — what kinds of vulnerabilities would it miss? Give a concrete example of each.

3. **(6 pts)** Propose one way to combine static analysis with **runtime monitoring** (from Lecture 10) to catch what static analysis misses. Describe the monitor's states and transitions.

## Grading

| Part | Points | What We Check |
|------|--------|---------------|
| Part 1: Analyzer | 50 | We run your analyzer on **hidden test skills** (not the ones in `skills/`). Points awarded based on true positives found and false positive rate. |
| Part 2: Skill Analysis | 30 | Correctness and depth of findings for the four provided skills. |
| Part 3: Defense Recommendations | 20 | Specificity and feasibility of proposed defenses. |
| **Total** | **100** | |

**Important:** Part 1 is graded on **hidden skills** that contain the same vulnerability classes (V1–V5) but are different skills from the ones provided. Build a general-purpose analyzer, not one that only works on the four examples.

## Analyzer Requirements

Your `analyzer.py` must:
1. Accept a file path (single `.md` file) or directory path as a command-line argument
2. Parse the SKILL.md and extract relevant sections (frontmatter, steps, code blocks, URLs, commands)
3. Apply your detection rules
4. Print findings in the structured format above
5. Exit with code 0 (even if findings are found — findings are not errors)

Skeleton code is provided in `analyzer.py` with the parsing infrastructure and output formatting. You implement the detection functions.

## Tips

- **Start by reading the skills carefully.** Before writing any code, read each SKILL.md as if you were a security auditor. What looks suspicious? That intuition will guide your detection rules.
- **Use regex for pattern matching.** Python's `re` module is sufficient for most detections. You don't need an AST parser for Markdown.
- **Think about what's NOT said.** Some vulnerabilities are about what the skill *doesn't* mention — no TLS, no confirmation step, no user approval.
- **Test on the provided skills first**, then generalize. Your analyzer will be graded on unseen skills.
- **Think about network topology.** Not all IP addresses are publicly routable. Research which IP ranges are reserved for private or special use — this knowledge is essential for V1 detection.
- 8 free late days are shared across all assignments.

## Academic Integrity

Using AI coding assistants is permitted and encouraged. You must understand and be able to explain every detection rule in your analyzer. The instructor reserves the right to conduct oral examinations.
