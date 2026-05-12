#!/usr/bin/env bash
# HW3 Submission Validator
# Run: bash check.sh

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

errors=0
warnings=0

pass_msg() { echo -e "  ${GREEN}✓${NC} $1"; }
warn_msg() { echo -e "  ${YELLOW}⚠${NC} $1"; warnings=$((warnings + 1)); }
fail_msg() { echo -e "  ${RED}✗${NC} $1"; errors=$((errors + 1)); }

echo ""
echo "═══════════════════════════════════════════"
echo "  CS292C HW3 Submission Checker"
echo "═══════════════════════════════════════════"
echo ""

# Check analyzer exists
echo "Analyzer"
if [ -f "analyzer.py" ]; then
    todo_count=$(grep -c "# TODO" analyzer.py 2>/dev/null || echo "0")
    if [ "$todo_count" -gt 0 ]; then
        warn_msg "analyzer.py has $todo_count remaining TODOs"
    else
        pass_msg "analyzer.py — no remaining TODOs"
    fi
else
    fail_msg "analyzer.py not found"
fi
echo ""

# Check report exists and has content
echo "Report"
if [ -f "report.md" ]; then
    line_count=$(wc -l < report.md | tr -d ' ')
    comment_lines=$(grep -c "^<!--" report.md 2>/dev/null || echo "0")
    content_lines=$((line_count - comment_lines))
    if [ "$content_lines" -gt 50 ]; then
        pass_msg "report.md has substantive content ($content_lines lines)"
    else
        warn_msg "report.md looks short ($content_lines lines of content)"
    fi
else
    fail_msg "report.md not found"
fi
echo ""

# Run analyzer on each skill
echo "Analyzer Execution"
for skill in skills/farmos_weather.md skills/passwordstore_broker.md skills/office_quotes.md skills/email_daily_summary.md; do
    if [ -f "$skill" ]; then
        output=$(python3 analyzer.py "$skill" 2>&1)
        if [ $? -eq 0 ]; then
            finding_count=$(echo "$output" | grep -c "\[FINDING\]" || echo "0")
            if [ "$finding_count" -gt 0 ]; then
                pass_msg "$skill — $finding_count finding(s)"
            else
                warn_msg "$skill — no findings (each skill has at least one vulnerability)"
            fi
        else
            fail_msg "$skill — analyzer crashed"
        fi
    fi
done
echo ""

# Run basic tests
echo "Basic Tests"
if python3 tests/test_basic.py > /dev/null 2>&1; then
    pass_msg "Basic tests pass"
else
    warn_msg "Some basic tests fail (run: python3 tests/test_basic.py)"
fi
echo ""

# Summary
echo "═══════════════════════════════════════════"
if [ "$errors" -eq 0 ] && [ "$warnings" -eq 0 ]; then
    echo -e "  ${GREEN}All checks passed!${NC} Ready to submit."
elif [ "$errors" -eq 0 ]; then
    echo -e "  ${YELLOW}$warnings warning(s)${NC}, 0 errors. Review warnings above."
else
    echo -e "  ${RED}$errors error(s)${NC}, $warnings warning(s). Fix errors before submitting."
fi
echo "═══════════════════════════════════════════"
echo ""

exit $errors
