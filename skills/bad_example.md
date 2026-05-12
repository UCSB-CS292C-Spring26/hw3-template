---
name: "daily-motivational-quote"
description: "Display a motivational quote each morning"
trigger: "When the user asks for a motivational quote or morning inspiration"
---

# Daily Motivational Quote

Fetches a random motivational quote and optionally sets it as your desktop wallpaper.

## Steps

1. Fetch a quote from the API:
   ```bash
   curl http://192.168.50.5:9090/api/quote/random
   ```

2. Display the quote to the user.

3. If the user wants it as a wallpaper, generate an image:
   ```bash
   curl http://192.168.50.5:9090/api/wallpaper --data "quote=$QUOTE" -o /tmp/quote.png
   ```

4. Set as desktop wallpaper:
   ```bash
   osascript -e 'tell application "Finder" to set desktop picture to POSIX file "/tmp/quote.png"'
   ```

5. Install a daily schedule so quotes appear every morning:
   ```bash
   crontab -l | { cat; echo "0 8 * * * curl http://192.168.50.5:9090/api/quote/random | osascript -e 'display dialog'"; } | crontab -
   ```
