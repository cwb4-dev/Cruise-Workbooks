# Costco Price Auditor: Claude Edition

A "Simple, Elegant, and Professional" implementation of a Costco price matching utility, built with a **Claude-based toolchain** and driven entirely by prompts. This version leverages **Claude Code** for scaffolding, **Claude Sonnet 4.5** for multimodal receipt parsing and reasoning, and the **Claude Agent SDK** for orchestration -- all wired up with plain text prompt files instead of hard-coded logic.

## Overview

- **Goal**: Automate price adjustment claims within the 30-day Costco window.
- **Philosophy**: "Prompt-first" architecture -- the prompts *are* the product. Iterate on text files, not code.
- **Tech Stack**: Claude Code (scaffolding agent), Claude Sonnet 4.5 (multimodal + reasoning), Claude Agent SDK (orchestration), SQLite (local store), and a cron job (scheduler).

-----

## Pillar 1: Scaffolding Focus (Claude Code)

Eliminate manual setup by having Claude Code generate the project skeleton from a single natural-language brief.

1. **Install Claude Code**: Run `npm install -g @anthropic-ai/claude-code` and authenticate with your Anthropic API key.
1. **Describe the App**: From an empty directory, launch `claude` and give it a high-level prompt:

> "Build a local Python app that ingests Costco receipt PDFs and images, uses Claude’s vision API to extract line items into SQLite, scrapes current weekly deals, and cross-references them to find price adjustment opportunities within 30 days. Include a CLI, a weekly cron runner, and email output via Resend. Organize prompts as standalone `.md` files I can edit without touching code."
1. **Zero-Boilerplate Setup**: Claude Code scaffolds the directory layout, `pyproject.toml`, SQLite schema, CLI entry point, and stub prompt files. You review each change in the diff view before accepting -- no hidden magic, no mystery infrastructure.
1. **Iterate Conversationally**: "Add a `--dry-run` flag." "Move the scraper into its own module." "Write tests for the deal matcher." Claude Code edits the repo in place.

-----

## Pillar 2: Prompt Files as Logic (`prompts/*.md`)

Replace hard-coded parsing and matching rules with editable Markdown prompt files. These are the heart of the system.

1. **Create `prompts/receipt_parser.md`**: The receipt OCR + normalization prompt.
- **Model**: `claude-sonnet-4-5` (multimodal).
- **System Instructions**:

> "You are a Costco inventory expert. Given a receipt image or PDF page, extract every line item as JSON with fields: `item_number`, `description`, `normalized_description`, `price_paid`, `tpd_applied` (bool), `tpd_amount`, `purchase_date`. Expand Costco abbreviations (e.g., ‘CKN/VEG DUMP’ → ‘Chicken & Vegetable Dumplings’, ‘T TURTLENECK’ → ‘Tahari Turtleneck Sweater’). Return only valid JSON -- no prose, no markdown fences."
1. **Create `prompts/deal_matcher.md`**: The price-match reasoning prompt.
- **System Instructions**:

> "You are given (1) a purchased item with date and price paid, and (2) a list of current Costco deals. Reason step-by-step: Is the purchase within 30 days of today? Does any active deal match this item by item_number first, then by normalized description? Is the deal price lower than what was paid? Output JSON: `{match_found, deal_item_number, savings, confidence, reasoning}`. Use extended thinking to work through ambiguous matches."
1. **Create `prompts/report_composer.md`**: The weekly email composer.
- Takes the matched results and produces a clean HTML email with two tables: *Price Adjustments Available* and *TPD Savings Already Applied*.
1. **Iterative Refinement**: When Costco introduces a new abbreviation or you spot a miss, edit the `.md` file and rerun. No redeploy, no code change.

-----

## Pillar 3: Claude Agent SDK (The Wiring)

Use the Claude Agent SDK to connect prompts, tools, and storage with minimal glue code.

1. **Define the Agent**: Create `agent/auditor.py` using the Claude Agent SDK. The agent has three tools:
- `parse_receipt(file_path)` -- loads the prompt from `prompts/receipt_parser.md`, sends the PDF/image to Sonnet 4.5, stores results in SQLite.
- `fetch_deals()` -- scrapes current deals from the weekly ad and coupon book, stores them in SQLite.
- `find_matches()` -- loads `prompts/deal_matcher.md`, iterates purchases × deals, writes matches to SQLite.
1. **Tool Use Loop**: The SDK handles the think-act-observe loop automatically. You give the agent a goal ("run the weekly audit") and it decides which tools to call and in what order based on your system prompt.
1. **Extended Thinking for Hard Cases**: Enable `thinking: {type: "enabled", budget_tokens: 4000}` on the matching call so Claude can reason through edge cases -- same item at different prices on two receipts, ambiguous abbreviations, items that went on sale *then* back up.
1. **Local Debugging**: Run `python -m agent.auditor --receipt path/to/receipt.pdf --verbose` to watch tool calls stream to the terminal. No dev UI needed; the logs tell the whole story.

-----

## Pillar 4: Extended Thinking (The Reasoning)

Use Claude’s extended thinking mode to handle the 30-day window and multi-item matching logic in the prompt layer, not in Python.

1. **Turn on Thinking**: In the deal_matcher prompt, instruct Claude:

> "Before producing JSON, think through: (a) the exact days elapsed between purchase_date and today, (b) whether that falls within the 30-day adjustment window, (c) whether item_number is an exact match or you’re inferring from description, and (d) your confidence in the match."
1. **Multi-Item Deduplication**: The prompt explicitly handles the case from the original project -- two of the same item on one receipt should both match, but each against the best available deal. Claude’s reasoning handles this cleanly without tracking indices manually.
1. **Confidence Scores**: Every match comes back with a `confidence` field. The report highlights high-confidence matches and flags low-confidence ones for human review before you walk into the warehouse.

-----

## Deployment & Usage

### Local Run

```bash
# Clone and install
git clone <your-repo> && cd costco-auditor
pip install -e .

# Add your API key
echo "ANTHROPIC_API_KEY=sk-ant-..." > .env
echo "RESEND_API_KEY=re_..." >> .env
echo "NOTIFY_EMAIL=you@example.com" >> .env

# Ingest a receipt
auditor ingest ~/Downloads/receipt_2026-04-12.pdf

# Run the full audit
auditor run
```

### Weekly Scheduled Run

Add one line to your crontab for a Friday 9 PM run:

```cron
0 21 * * 5 cd /path/to/costco-auditor && /usr/bin/env auditor run --email
```

That’s it. No containers, no EventBridge, no CDK stacks. A cron line and a Python script.

### Optional: Cloud Deployment

If you want it off your laptop, the same code drops onto a $4/mo VPS or a Cloudflare Worker with Cron Triggers. The Agent SDK and Anthropic API don’t care where they run.

-----

## What This Costs

At ~4 receipts/week and one weekly audit, expect roughly **$0.15–0.30/week** in Claude API usage (Sonnet 4.5 at current pricing, with prompt caching on the deal_matcher system prompt cutting repeat costs significantly). Email via Resend is free under 100/day. SQLite is free. Cron is free.

-----

## Why This Works Well with Claude

- **Vision quality**: Sonnet 4.5 handles messy receipt photos, faded thermal paper, and cryptic Costco abbreviations with high accuracy.
- **Extended thinking**: The 30-day window and best-deal-per-item logic live in the prompt as reasoning steps, not in Python.
- **Prompt caching**: The big system prompts (parser, matcher) are cached, so weekly reruns are cheap.
- **Claude Code for scaffolding**: You describe the project once, review the diff, and you’re running.
- **Agent SDK for orchestration**: The tool-use loop is handled for you; you write tools, not state machines.

-----

## What’s Next

- **iOS shortcut**: A Share Sheet extension that sends a receipt photo straight to the `ingest` endpoint -- snap at checkout, done.
- **Costco.com OAuth**: Once available, pull receipts directly from your account instead of uploading manually.
- **Multi-retailer**: The same prompt-first architecture extends to Target Circle, Amazon price drops, etc. Swap the scraper and the parser prompt; reuse everything else.

25 years of Costco membership. One Claude agent. Walk in Saturday morning and collect what you’re owed.