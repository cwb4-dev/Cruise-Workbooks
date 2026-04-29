# App Log: Weather Advisor

**File:** `weather.py`  
**Folder:** `Essentials/`  
**Version:** 1  
**Date Built:** *(paste date)*  
**Status:** ⚠️ In Progress

-----

## What This App Does

Fetches live temperature and weather conditions for any city using the
free Open-Meteo API (no API key needed). Recommends Lido Deck or Library
based on temperature and rain conditions.

-----

## Build Prompt

```
Create weather.py in the Essentials folder.

The script should:
1. Ask the user to type a city name
2. Fetch current temperature and weather condition from the Open-Meteo
   geocoding and forecast APIs -- no API key needed, completely free
3. Print the city name, temperature in both Celsius and Fahrenheit,
   and the current weather condition
4. Print a recommendation:
   - Temp above 22C and no rain → "🌞 Lido Deck recommended"
   - Temp below 18C or rainy conditions → "📚 Library recommended"
   - Otherwise → "☁️ Either works today"

Use only Python standard library plus the urllib module for HTTP requests.
Do not use the requests package.

Test case 1: Run with the city Nassau.
Expected: Temperature prints in C and F, recommendation prints, no errors.

Test case 2: Run with the city London.
Expected: Cooler temperature, likely Library recommendation.

Test case 3: Run with an invalid city name like "XYZABC123".
Expected: Script handles the error gracefully and prints a helpful message
instead of crashing.

Fix any errors automatically and confirm all three tests pass.
```

-----

## Test Results

|Test     |Expected                           |Result|Pass?|
|---------|-----------------------------------|------|-----|
|Nassau   |Temp in C and F, recommendation    |      |☐    |
|London   |Cooler temp, Library recommendation|      |☐    |
|XYZABC123|Graceful error message, no crash   |      |☐    |

-----

## Issues Encountered

*(document any errors or fixes here)*

-----

## How to Run

```bash
cd ~/at-sea-ipad-workbooks/Cruise-Workbook-2026
python3 Essentials/weather.py
```

-----

## Sample Output

*(paste actual output here after first successful run)*

-----

## Git Commit

```bash
git add Essentials/weather.py Essentials/app_log.md
git commit -m "Add App 1: Weather Advisor -- all tests passing"
git push
```

-----

*Atlantic Data Lab -- MSC Meraviglia 2026*