---
name: "markdown-formatter"
description: "Format and lint Markdown files for consistency"
trigger: "When the user asks to format, lint, or clean up a Markdown file"
---

# Markdown Formatter

A simple skill that formats Markdown files for consistency. It checks heading levels, list indentation, and trailing whitespace.

## Tools Required

- `read_file` — to read the target Markdown file
- `write_file` — to write the formatted output

## Steps

1. Read the target Markdown file:
   ```bash
   cat "$TARGET_FILE"
   ```

2. Apply formatting rules:
   - Ensure a blank line before and after headings
   - Normalize list indentation to 2 spaces
   - Remove trailing whitespace
   - Ensure file ends with a single newline

3. Show the diff to the user and ask for confirmation:
   > "Here are the proposed formatting changes. Apply them? (yes/no)"

4. If the user confirms, write the formatted file back:
   ```bash
   write_file "$TARGET_FILE" "$FORMATTED_CONTENT"
   ```

5. Report summary:
   > "Formatted {filename}: {n} lines changed."

## Permissions

- `read_file`: Read access to the target file only
- `write_file`: Write access to the target file only (after user confirmation)

## Notes

- This skill only modifies the file the user explicitly names.
- All changes require user confirmation before writing.
- No network access is needed.
- No packages are installed.
