# CS292C Homework 3: Security Audit of Agent Skills

**Out:** Lecture 11 (5/5) | **Due:** Lecture 16 (5/21) 11:59pm | **Weight:** 12%

## Overview

Agent skills (SKILL.md files) are the executable infrastructure that governs how coding agents operate. Skills published on registries like ClawHub can contain harmful behaviors that evade both VirusTotal and LLM-based reviewers.

In this assignment, you will build a **static analysis tool** that automatically inspects SKILL.md files and flags potentially harmful or deceptive behaviors.

**Language:** Python 3.10+. No external dependencies required (standard library is sufficient).

## Setup

```bash
python3 analyzer.py skills/farmos_weather.md       # single skill
python3 analyzer.py skills/                         # all skills
```

## Submission

Push all work to this repo before the deadline:
1. `analyzer.py` — your static analysis tool
2. `report.md` — findings report
3. Run `bash check.sh` before submitting.

## The Skills

Four SKILL.md files are provided in `skills/`. Each is a real skill that was published on ClawHub and **passed both VirusTotal and ClawHub's own safety scanners**. However, each skill contains at least one security issue.

| Skill | Description |
|-------|-------------|
| `farmos_weather.md` | Weather data for farm fields |
| `passwordstore_broker.md` | Password manager bridge |
| `office_quotes.md` | The Office (US) quote generator |
| `email_daily_summary.md` | Daily email digest |

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

| Part | Points | What We Check |
|------|--------|---------------|
| Part 1: Analyzer | 50 | We run your analyzer on **hidden test skills** (not the ones in `skills/`). Points based on true positives found and false positive rate. |
| Part 2: Skill Analysis | 30 | Correctness and depth of findings for the four provided skills. |
| Part 3: Defense Recommendations | 20 | Specificity and feasibility of proposed defenses. |
| **Total** | **100** | |

## Tips

- **Start by reading the skills carefully.** Before writing any code, read each SKILL.md as if you were a security auditor. What looks suspicious? That intuition will guide your detection rules.
- **Think about what a skill *should* vs. *actually* does.** Does the skill's behavior match its description? Does it access resources beyond what it claims to need?
- **Generalize.** Your analyzer will be graded on unseen skills. Don't hardcode checks for specific skills — build rules that catch *classes* of problems.
- 8 free late days are shared across all assignments.

## Academic Integrity

Using AI coding assistants is permitted and encouraged. You must understand and be able to explain every detection rule in your analyzer. The instructor reserves the right to conduct oral examinations.
