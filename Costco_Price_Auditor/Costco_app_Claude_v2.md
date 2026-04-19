# Costco Price Auditor: Claude Edition -- Build Spec

A complete, buildable specification for a prompt-first Costco price adjustment agent. Hand this file to Claude Code and it has enough detail to scaffold a working app without guessing at schemas, prompts, or integration points.

-----

## 1. Goal & Scope

Build a local Python application that:

1. Ingests Costco receipts (PDF or image).
1. Uses Claude Sonnet 4.5 vision to extract line items into SQLite.
1. Scrapes current weekly deals from a known source.
1. Cross-references purchases against active deals within the 30-day price adjustment window.
1. Emails a weekly HTML report via Resend.
1. Runs on a cron schedule.

**Non-goals**: multi-user auth, web UI, cloud deployment, mobile app. Those are future work.

-----

## 2. Project Layout

```
costco-auditor/
├── pyproject.toml
├── README.md
├── .env.example
├── prompts/
│   ├── receipt_parser.md
│   ├── deal_matcher.md
│   └── report_composer.md
├── auditor/
│   ├── __init__.py
│   ├── cli.py               # Typer-based CLI entry point
│   ├── db.py                # SQLite schema + helpers
│   ├── agent.py             # Claude Agent SDK orchestration
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── parse_receipt.py
│   │   ├── fetch_deals.py
│   │   ├── find_matches.py
│   │   └── send_report.py
│   ├── scrapers/
│   │   ├── __init__.py
│   │   └── costco_insider.py
│   └── email_client.py      # Resend wrapper
└── tests/
    ├── fixtures/
    │   └── sample_receipt.pdf
    ├── test_parser.py
    └── test_matcher.py
```

-----

## 3. SQLite Schema

Single file at `~/.costco-auditor/auditor.db`. Create on first run.

```sql
CREATE TABLE IF NOT EXISTS receipts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_path TEXT NOT NULL,
    file_hash TEXT UNIQUE NOT NULL,           -- SHA256, prevents duplicate ingestion
    purchase_date DATE NOT NULL,
    warehouse TEXT,
    total REAL,
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS line_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    receipt_id INTEGER NOT NULL REFERENCES receipts(id) ON DELETE CASCADE,
    line_position INTEGER NOT NULL,           -- Order on receipt, for dedup
    item_number TEXT,                         -- Costco SKU, often 6-7 digits
    description TEXT NOT NULL,                -- Raw receipt text
    normalized_description TEXT,              -- Claude-expanded version
    price_paid REAL NOT NULL,
    tpd_applied BOOLEAN DEFAULT 0,            -- Temporary Price Drop at checkout
    tpd_amount REAL DEFAULT 0,
    UNIQUE(receipt_id, line_position)
);

CREATE TABLE IF NOT EXISTS deals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_number TEXT,
    description TEXT NOT NULL,
    sale_price REAL NOT NULL,
    regular_price REAL,
    savings REAL,
    valid_from DATE NOT NULL,
    valid_to DATE NOT NULL,
    source_url TEXT,
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS matches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    line_item_id INTEGER NOT NULL REFERENCES line_items(id),
    deal_id INTEGER NOT NULL REFERENCES deals(id),
    savings REAL NOT NULL,
    confidence REAL NOT NULL,                 -- 0.0 to 1.0
    reasoning TEXT,                           -- Claude's explanation
    reported BOOLEAN DEFAULT 0,               -- Included in a weekly report yet
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(line_item_id, deal_id)
);

CREATE INDEX idx_line_items_receipt ON line_items(receipt_id);
CREATE INDEX idx_deals_valid ON deals(valid_from, valid_to);
CREATE INDEX idx_matches_reported ON matches(reported);
```

-----

## 4. Prompt Files

### 4.1 `prompts/receipt_parser.md`

```markdown
You are a Costco receipt parsing expert. You will be given a receipt image or PDF page.

## Your task
Extract every purchased line item and return a single JSON object.

## Output format
Return ONLY valid JSON. No prose, no markdown fences, no explanation.
```

{
"purchase_date": "YYYY-MM-DD",
"warehouse": "string (city or number, if visible)",
"total": 0.00,
"items": [
{
"line_position": 1,
"item_number": "1234567",
"description": "CKN/VEG DUMP",
"normalized_description": "Chicken & Vegetable Dumplings",
"price_paid": 14.99,
"tpd_applied": false,
"tpd_amount": 0.00
}
]
}

```
## Rules
1. `line_position` is the order the item appears on the receipt, starting at 1.
2. `item_number` is the Costco SKU, usually 6–7 digits near the item name. If not visible, use null.
3. `description` is the raw text from the receipt, uppercase, abbreviations intact.
4. `normalized_description` is your expansion of Costco's shorthand into plain English. Examples:
   - "CKN/VEG DUMP" → "Chicken & Vegetable Dumplings"
   - "T TURTLENECK" → "Tahari Turtleneck Sweater"
   - "KS PAPER TWL" → "Kirkland Signature Paper Towels"
   - "ORG BABY SPIN" → "Organic Baby Spinach"
5. `price_paid` is the final price paid per line, after any TPD already applied.
6. If a line shows a discount like "TPD/1234567  -3.00", attach that to the preceding item: set `tpd_applied: true` and `tpd_amount: 3.00`, and make sure `price_paid` reflects the post-discount amount.
7. Ignore tax lines, subtotals, payment method lines, and the barcode at the bottom.
8. If the receipt is unreadable or clearly not a Costco receipt, return `{"error": "reason"}`.

## Think carefully about
- Multi-line items where the description wraps.
- TPDs applied to the line above, not the line below.
- Member savings summaries at the bottom -- those are totals, not line items.
```

### 4.2 `prompts/deal_matcher.md`

```markdown
You are a Costco price adjustment analyst. You will be given:
1. A purchased line item (with date, description, item_number, price_paid).
2. Today's date.
3. A list of currently active Costco deals.

## Your task
Determine whether this purchase qualifies for a price adjustment.

## Reasoning steps (use extended thinking)
1. Compute days elapsed between purchase_date and today. Is it ≤ 30? If not, no match possible -- return `{"match_found": false, "reason": "outside 30-day window"}`.
2. For each active deal, check:
   - Does `item_number` match exactly? (Highest confidence.)
   - If no item_number match, does the `normalized_description` clearly refer to the same product? (Lower confidence.)
3. Among matching deals, pick the one with the lowest `sale_price`.
4. If that price is lower than `price_paid - tpd_amount`, this is a valid adjustment.
5. Savings = `(price_paid - tpd_amount) - sale_price`.

## Output format
Return ONLY valid JSON:
```

{
"match_found": true,
"deal_id": 42,
"savings": 3.00,
"confidence": 0.95,
"reasoning": "Exact item_number match (1234567). Purchased 2026-04-10, today 2026-04-19, within window. Paid $14.99, current sale $11.99."
}

```
## Confidence guidance
- 0.95–1.00: Exact item_number match.
- 0.75–0.94: Description match with strong brand/size/variety agreement.
- 0.50–0.74: Plausible description match but ambiguous (e.g., same product line, different size).
- Below 0.50: Do not return as a match.

## Edge cases
- Same item purchased twice on one receipt: match each line independently. Both qualify.
- Item on sale then back to regular price: only matches while the deal is currently active (today between valid_from and valid_to).
- TPD already applied: subtract `tpd_amount` from `price_paid` before comparing to `sale_price`.
```

### 4.3 `prompts/report_composer.md`

```markdown
You are composing a weekly price adjustment report email.

## Input
You will receive two lists as JSON:
1. `adjustments`: matches where the user can walk into Costco and claim money back.
2. `tpd_savings`: items where Costco already applied a Temporary Price Drop at checkout (informational).

## Output
Return a single HTML email body with inline CSS. No `<html>` or `<body>` tags -- just the content that will go inside the email body. Use a clean, scannable layout.

## Structure
1. A short header: "Weekly Costco Price Audit -- [today's date]".
2. A one-line summary: "Found $X.XX in price adjustments across N items. You can claim these at the Costco membership counter."
3. **Table 1 -- Price Adjustments Available**. Columns: Item, Purchased, Paid, Current Sale, Savings, Confidence. Sort by savings descending.
4. **Table 2 -- TPD Savings Already Applied**. Columns: Item, Purchased, Regular Price, You Paid, Saved. Informational only.
5. A footer note: "Bring your receipt to the membership counter within 30 days of purchase. Item numbers above are for reference."

## Style
- Font: system-ui, sans-serif.
- Tables: full width, 1px borders, alternating row background (#f9f9f9).
- Savings column: bold, green (#2d8a3e).
- Confidence below 0.80: add a small ⚠️ next to the item and a row-level note.
- Max width 640px, centered.

## Rules
- Currency always formatted as `$X.XX`.
- Dates as `Apr 12, 2026`.
- If `adjustments` is empty, skip Table 1 and say "No price adjustments this week."
- If `tpd_savings` is empty, skip Table 2.
```

-----

## 5. Tool Implementations

### 5.1 `auditor/tools/parse_receipt.py`

Responsibilities:

- Accept a file path (PDF or image).
- Compute SHA256 hash. Skip if already in `receipts` table.
- If PDF, render each page to PNG at 200 DPI using `pypdfium2`.
- Send the image(s) to Claude Sonnet 4.5 with the system prompt from `prompts/receipt_parser.md`.
- Parse the JSON response.
- Insert a row into `receipts` and rows into `line_items`.

API call shape:

```python
from anthropic import Anthropic
import base64, pathlib

client = Anthropic()
system_prompt = pathlib.Path("prompts/receipt_parser.md").read_text()
image_b64 = base64.standard_b64encode(image_bytes).decode()

response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=4096,
    system=system_prompt,
    messages=[{
        "role": "user",
        "content": [
            {"type": "image", "source": {
                "type": "base64",
                "media_type": "image/png",
                "data": image_b64
            }},
            {"type": "text", "text": "Parse this receipt."}
        ]
    }]
)
```

Enable prompt caching on the system prompt to cut costs on repeat calls.

### 5.2 `auditor/tools/fetch_deals.py`

Responsibilities:

- Call `scrapers.costco_insider.scrape_current_deals()` (see §6).
- Upsert each deal into the `deals` table, keyed on `(item_number, valid_from)` or `(description, valid_from)` if no item number.
- Delete deals whose `valid_to` is more than 7 days in the past (keep a buffer).

### 5.3 `auditor/tools/find_matches.py`

Responsibilities:

- Query all `line_items` whose receipt `purchase_date` is within the last 30 days and which don’t already have a high-confidence match.
- For each, gather all currently active `deals` (`valid_from <= today <= valid_to`).
- For each (line_item, candidate_deals) pair, call Claude with the `deal_matcher.md` prompt and extended thinking enabled:

```python
response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=2048,
    thinking={"type": "enabled", "budget_tokens": 4000},
    system=matcher_prompt,
    messages=[{
        "role": "user",
        "content": json.dumps({
            "today": today.isoformat(),
            "purchase": line_item_dict,
            "deals": candidate_deals_list
        })
    }]
)
```

- If `match_found` is true and `confidence >= 0.80`, insert into `matches`.
- Lower-confidence matches are still stored but flagged in the report.

### 5.4 `auditor/tools/send_report.py`

Responsibilities:

- Query all `matches` where `reported = 0`, split into `adjustments` and `tpd_savings` (the latter comes from `line_items.tpd_applied = 1` on receipts from the past 7 days, not from `matches`).
- Call Claude with `report_composer.md` to generate the HTML body.
- Send via Resend:

```python
import resend
resend.api_key = os.environ["RESEND_API_KEY"]
resend.Emails.send({
    "from": "auditor@yourdomain.com",
    "to": os.environ["NOTIFY_EMAIL"],
    "subject": f"Costco Audit -- ${total_savings:.2f} available",
    "html": html_body
})
```

- On success, set `reported = 1` on the included matches.

-----

## 6. Scraper Target: CostcoInsider

**Recommended source**: `costcoinsider.com`. It publishes the current monthly savings book and weekly hot buys as structured HTML, keyed by item number, updated reliably.

**Backup source**: the `r/Costco` deals megathread (parse with Claude rather than CSS selectors -- more resilient).

### `auditor/scrapers/costco_insider.py`

```python
import httpx
from bs4 import BeautifulSoup
from datetime import date, datetime

BASE = "https://www.costcoinsider.com"

def scrape_current_deals() -> list[dict]:
    """Return a list of deal dicts ready to upsert into the deals table."""
    index = httpx.get(f"{BASE}/category/coupon-book/", timeout=30).text
    soup = BeautifulSoup(index, "html.parser")
    latest_post = soup.select_one("article a")["href"]

    page = httpx.get(latest_post, timeout=30).text
    page_soup = BeautifulSoup(page, "html.parser")

    # Validity dates are in the post title, e.g. "April 3 - April 28, 2026"
    title = page_soup.select_one("h1").get_text()
    valid_from, valid_to = parse_date_range(title)

    deals = []
    for row in page_soup.select("table.deals tbody tr"):
        cols = [c.get_text(strip=True) for c in row.select("td")]
        if len(cols) < 4:
            continue
        deals.append({
            "item_number": cols[0],
            "description": cols[1],
            "sale_price": parse_price(cols[2]),
            "savings": parse_price(cols[3]),
            "regular_price": parse_price(cols[2]) + parse_price(cols[3]),
            "valid_from": valid_from,
            "valid_to": valid_to,
            "source_url": latest_post
        })
    return deals

# parse_date_range() and parse_price() are small helpers.
```

**Known fragility**: the exact table structure on CostcoInsider shifts occasionally. If scraping returns zero rows, fall back to sending the raw HTML to Claude with a "extract deals as JSON" prompt. This is the Claude-native resilience pattern -- prompt your way out of broken selectors.

-----

## 7. Agent Orchestration

### `auditor/agent.py`

Use the Claude Agent SDK to expose the four tools. The agent’s system prompt:

```
You are the Costco Price Auditor. You have tools to:
- parse_receipt(file_path): OCR a receipt and store line items.
- fetch_deals(): update the local deals database from web sources.
- find_matches(): cross-reference purchases and deals, storing matches.
- send_report(): email the weekly summary and mark matches as reported.

When asked to "run the weekly audit", call fetch_deals, then find_matches, then send_report, in that order. Report back what you did at each step.
```

The agent handles the think-act-observe loop. You get a conversation log for free, which is your debugging output.

-----

## 8. CLI

### `auditor/cli.py` (Typer)

```bash
auditor ingest <path>          # Parse one receipt
auditor deals refresh          # Scrape and update deals
auditor audit                  # Run find_matches, print results, no email
auditor run [--email]          # Full weekly run: deals → matches → report
auditor db reset               # Nuke and recreate the database
```

Every command accepts `--verbose` to stream Claude’s reasoning.

-----

## 9. Environment & Configuration

### `.env.example`

```
ANTHROPIC_API_KEY=sk-ant-...
RESEND_API_KEY=re_...
NOTIFY_EMAIL=you@example.com
FROM_EMAIL=auditor@yourdomain.com
AUDITOR_DB_PATH=~/.costco-auditor/auditor.db
```

### `pyproject.toml` dependencies

```toml
[project]
name = "costco-auditor"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "anthropic>=0.40.0",
    "claude-agent-sdk>=0.2.0",
    "typer>=0.12",
    "httpx>=0.27",
    "beautifulsoup4>=4.12",
    "pypdfium2>=4.30",
    "resend>=2.0",
    "python-dotenv>=1.0",
]

[project.scripts]
auditor = "auditor.cli:app"
```

-----

## 10. Cron Setup

```cron
0 21 * * 5 cd /path/to/costco-auditor && /path/to/.venv/bin/auditor run --email >> ~/.costco-auditor/cron.log 2>&1
```

Friday 9 PM local time. Saturday morning you have your report.

-----

## 11. Testing Checklist

Before relying on the agent:

1. Ingest three real receipts of different styles (warehouse, gas, food court). Verify `line_items` rows look right.
1. Run `auditor deals refresh`. Verify the `deals` table has ≥ 50 rows and `valid_to` is in the future.
1. Run `auditor audit --verbose`. Spot-check a few matches -- are the reasoning strings correct? Any false positives?
1. Run `auditor run --email` manually. Verify the email arrives and the tables render in your mail client (test Gmail + Apple Mail at minimum).
1. Install the cron. Let it run one cycle unattended. Confirm the next email arrives.

-----

## 12. What’s Genuinely Hard vs. What’s Routine

**Routine** (Claude Code handles in one session): SQLite schema, CLI, Agent SDK wiring, Resend integration, prompt files, PDF rendering.

**Needs iteration**: the `receipt_parser.md` prompt -- your first five receipts will reveal abbreviations and layouts it doesn’t handle. Budget an hour of prompt-tweaking.

**Genuinely fragile**: the CostcoInsider scraper selectors. Plan to use the Claude-based HTML-to-JSON fallback from day one.

**Out of scope here**: Costco.com OAuth for automatic receipt retrieval. Not publicly available.

-----

## 13. Cost Estimate

Per weekly run (assuming ~5 new receipts, ~20 line items, ~80 active deals):

- Receipt parsing: ~5 × 3000 tokens = 15k input, 2k output ≈ $0.05
- Deal matching: ~20 × 2000 tokens = 40k input, 4k output ≈ $0.13 (with prompt caching on system prompt, closer to $0.08)
- Report composition: ~3k tokens total ≈ $0.01
- **Weekly total: $0.15–0.25.**

Monthly: under $1. Same order of magnitude as the original AWS version.

-----

## 14. Handoff Instructions to Claude Code

When you start your Claude Code session, paste this file and say:

> "Build the project described in this spec. Scaffold the directory structure from §2, create the SQLite schema from §3 as a migration in `auditor/db.py`, create the three prompt files from §4 verbatim, and stub out the four tools from §5 with working implementations. Use the CostcoInsider scraper from §6 but include the Claude HTML-to-JSON fallback. Wire everything through the Claude Agent SDK as described in §7. Generate a Typer CLI per §8. Write the two test files in §11 using a fixture receipt I’ll provide. Stop after each major component and show me the diff."

That prompt is enough. The spec carries the rest.