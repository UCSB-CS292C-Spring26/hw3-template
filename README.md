# CS292C Homework 3: Security Audit of Agent Skills

**Out:** Lecture 11 (5/5) | **Due:** Lecture 16 (5/21) 11:59pm | **Weight:** 12%

## Overview

Agent skills (SKILL.md files) are the executable infrastructure that governs how coding agents operate. Skills published on registries like ClawHub can contain harmful behaviors that evade both VirusTotal and LLM-based reviewers.

In this assignment, you will build a **static analysis tool** that automatically inspects SKILL.md files and flags potentially harmful or deceptive behaviors.

**Language:** Python 3.10+. No external dependencies required (standard library is sufficient).

## Setup

```bash
python3 analyzer.py skills/bad_example.md            # single skill
python3 analyzer.py skills/                           # all skills
```

## Submission

Push all work to this repo before the deadline:
1. `analyzer.py` — your static analysis tool
2. `report.md` — findings report
3. Run `bash check.sh` before submitting.

## Worked Example

To help you get started, we provide two reference skills:

### `skills/safe_example.md` — A clean skill (no issues)

This is a simple Markdown formatter. It reads a file, formats it, **asks the user for confirmation**, then writes it back. No network access, no package installs, no persistence. Your analyzer should produce **no findings** on this skill.

### `skills/bad_example.md` — A skill with obvious issues

This "motivational quote" skill has several problems. Here is what a correct analyzer should output:

```
[FINDING] daily-motivational-quote
  Severity: HIGH
  Location: line 14
  Description: URL uses a raw IP address instead of a domain name
  Evidence: http://192.168.50.5:9090/api/quote/random

[FINDING] daily-motivational-quote
  Severity: MEDIUM
  Location: line 14
  Description: Plaintext HTTP used (no TLS)
  Evidence: http://192.168.50.5:9090/api/quote/random

[FINDING] daily-motivational-quote
  Severity: HIGH
  Location: line 27
  Description: Cron job installed without asking the user for confirmation
  Evidence: crontab -l | { cat; echo "0 8 * * * curl ..."; } | crontab -
```

Note: This is not an exhaustive list — your analyzer may find additional issues in `bad_example.md`. The point is to show the expected output format and the level of specificity we expect.

**Use these two skills to calibrate your analyzer** before running it on the four real skills below.

---

## The Skills

Four SKILL.md files are provided in `skills/`. Each is a real skill that was published on ClawHub and **passed both VirusTotal and ClawHub's own safety scanners**. However, each skill contains at least one security issue.

| Skill | Description |
|-------|-------------|
| `farmos_weather.md` | Weather data for farm fields |
| `passwordstore_broker.md` | Password manager bridge |
| `office_quotes.md` | The Office (US) quote generator |
| `email_daily_summary.md` | Daily email digest |

Your job is to figure out what's wrong with each one.

## Your Task

### Part 1: Build the Analyzer (50 points)

Implement `analyzer.py` — a static analysis tool that reads a SKILL.md file and outputs a structured report of potential security issues.

**You decide what to check for.** Read the four skills carefully, identify the security issues, then generalize your findings into detection rules that would catch similar issues in other skills.

Your analyzer should be **general-purpose** — it will be graded on hidden skills (not the four provided) that contain similar classes of issues.

**Output format:** Your analyzer must print structured output for each finding:

```
[FINDING] <skill_name>
  Severity: <CRITICAL|HIGH|MEDIUM|LOW>
  Location: <line number or section>
  Description: <what was found and why it's a problem>
  Evidence: <the specific text/pattern that triggered the finding>
```

### Part 2: Analyze the Skills (30 points)

Run your analyzer on all four provided skills and write up your findings in `report.md`.

For each skill, your report must include:
1. **Summary:** What does the skill claim to do? (1–2 sentences)
2. **Findings:** List each issue found, with severity and evidence
3. **Attack scenario:** For the most critical finding, describe a concrete attack: who is the attacker, what do they gain, and what is the blast radius? (3–5 sentences)
4. **Risk assessment:** Would you approve this skill for installation? Why or why not? (1–2 sentences)

### Part 3: Defense Recommendations (20 points)

In `report.md`, add a final section:

1. **(8 pts)** For each category of issue you identified, propose a **specific, implementable** defense that an agent runtime could enforce.

2. **(6 pts)** Describe **two limitations** of your static analysis approach — what kinds of issues would it miss? Give a concrete example of each.

3. **(6 pts)** Propose one way to combine static analysis with **runtime monitoring** (from Lecture 10) to catch what static analysis misses. Describe the monitor's states and transitions.

## Grading

### Part 1 Grading (50 points)

We run your analyzer on **hidden test skills** not included in this repo. These hidden skills contain similar classes of issues to the ones in `skills/`, but are different skills.

Points are awarded based on **detection categories**, not individual skills:

| Criteria | Points |
|----------|--------|
| Detects issues in category A across hidden skills | 10 |
| Detects issues in category B across hidden skills | 10 |
| Detects issues in category C across hidden skills | 10 |
| Detects issues in category D across hidden skills | 10 |
| Low false positive rate (< 3 false positives per skill on clean skills) | 10 |

The categories correspond to the types of issues present in the four provided skills. If your analyzer catches the issues in the provided skills using general rules (not hardcoded checks), it will score well on the hidden skills too.

### Part 2 & 3 Grading

| Part | Points |
|------|--------|
| Part 2: Skill Analysis | 30 |
| Part 3: Defense Recommendations | 20 |
| **Total** | **100** |

## Tips

- **Start by reading the skills carefully.** Before writing any code, read each SKILL.md as if you were a security auditor. What looks suspicious? That intuition will guide your detection rules.
- **Use the worked example** (`bad_example.md`) to test your output format and make sure your basic checks work before tackling the harder skills.
- **Use the safe example** (`safe_example.md`) to verify your analyzer doesn't flag clean skills (false positives hurt your score).
- **Think about what a skill *should* vs. *actually* does.** Does the skill's behavior match its description? Does it access resources beyond what it claims to need?
- **Generalize.** Don't hardcode checks for specific skills — build rules that catch *classes* of problems.
- 8 free late days are shared across all assignments.

## Academic Integrity

Using AI coding assistants is permitted and encouraged. You must understand and be able to explain every detection rule in your analyzer. The instructor reserves the right to conduct oral examinations.
