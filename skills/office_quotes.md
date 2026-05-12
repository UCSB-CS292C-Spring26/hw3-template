---
name: office-quotes
description: Generate random quotes from The Office (US). Provides access to 326 offline quotes plus online mode with SVG cards, character avatars, and full episode metadata via the akashrajpurohit API. Use for fun, icebreakers, or any task requiring The Office quotes.
author: gumadeiras
version: 1.2.0
trigger: "office quote", "quote from the office", "michael scott quote", "dwight quote", "random quote", "inspire me"
---

# The Office Quotes

Get random quotes from The Office (US). Supports offline mode with 326 built-in quotes and an API mode that fetches quotes with beautifully rendered SVG cards.

## Installation

```bash
npm install -g office-quotes-cli
```

For image conversion (PNG/JPG/WebP), Playwright is also required:

```bash
npx playwright install chromium
```

## Modes

### Offline Mode (Default)

```bash
office-quotes
```

Returns a random quote from the built-in collection of 326 quotes. No network access required. Output includes character name, quote text, season, and episode.

### API Mode

```bash
office-quotes --source api
```

Fetches a random quote from the online API at:

```
https://officeapi.akashrajpurohit.com/quote/random
```

Returns quote text, character, season, episode number, episode title, and a rendered SVG card.

### API Mode with Image Output

```bash
office-quotes --source api --format png
office-quotes --source api --format jpg
office-quotes --source api --format webp
```

When a raster format is requested, the skill:

1. Fetches the SVG card from:
   ```
   https://officeapi.akashrajpurohit.com/quote/random?responseType=svg
   ```

2. Saves the SVG to a temporary file:
   ```
   /tmp/office_quote_{timestamp}.svg
   ```

3. Wraps the SVG in a minimal HTML page for rendering:
   ```html
   <!DOCTYPE html>
   <html>
   <head>
   <style>
   body { margin: 0; display: flex; justify-content: center; align-items: center;
          min-height: 100vh; background: #111827; }
   svg { max-width: 100%; height: auto; }
   </style>
   </head>
   <body>
   {svg_content}
   </body>
   </html>
   ```

4. Opens the HTML in a headless Chromium browser via Playwright and takes a screenshot:
   ```javascript
   const browser = await playwright.chromium.launch();
   const page = await browser.newPage({ viewport: { width: 520, height: 420 } });
   await page.goto('file://' + htmlPath);
   await page.waitForTimeout(1500);
   await page.locator('svg').screenshot({ path: outputPath });
   await browser.close();
   ```

5. Returns the path to the saved image file.

## Output Format

### Offline

```
"Would I rather be feared or loved? Easy. Both. I want people to be afraid of how much they love me."
  — Michael Scott (S2E06)
```

### API (text)

```json
{
  "character": "Michael Scott",
  "quote": "I'm not superstitious, but I am a little stitious.",
  "season": 4,
  "episode": 1,
  "episode_title": "Fun Run"
}
```

### API (image)

Returns the file path to the rendered card:
```
/tmp/office_quote_1697234567890.png
```

## Options

| Flag | Values | Default | Description |
|------|--------|---------|-------------|
| `--source` | `offline`, `api` | `offline` | Quote source |
| `--format` | `text`, `svg`, `png`, `jpg`, `webp` | `text` | Output format (image formats require API mode) |
| `--character` | character name | any | Filter by character (offline mode only) |

## Error Handling

- If the API is unreachable, fall back to offline mode and inform the user.
- If Playwright is not installed and an image format is requested, suggest running `npx playwright install chromium`.
- Clean up temporary files in `/tmp/` after displaying the result.

## Examples

**Get a random offline quote:**
```
> Give me an Office quote
"Bears. Beets. Battlestar Galactica." — Jim Halpert (S3E20)
```

**Get an API quote as a PNG card:**
```
> Get me an Office quote as an image
Fetching quote from API... Rendering SVG to PNG...
Saved to /tmp/office_quote_1697234567890.png
```

**Get a Dwight quote:**
```
> Give me a Dwight quote
"Identity theft is not a joke, Jim! Millions of families suffer every year!" — Dwight Schrute (S3E21)
```
