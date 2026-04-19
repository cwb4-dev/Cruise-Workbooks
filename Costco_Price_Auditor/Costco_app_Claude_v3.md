# Costco Price Auditor: iPad + Claude.ai Edition

A fully iPad-native implementation of a Costco price adjustment agent. No terminal, no code editor, no hosting -- everything runs inside Claude.ai using Projects, Artifacts, and the vision and web search features. You’ll build it once in about 30 minutes and then spend two minutes a week running the audit.

-----

## What You’ll End Up With

- A **Claude.ai Project** called "Costco Price Auditor" that remembers your receipts, your preferences, and your prompts across sessions.
- A **receipt tracker Artifact** -- an interactive web page living inside the Project that stores your receipts and matches persistently between chats.
- A **weekly workflow** where you open the Project, upload new receipts, say "run this week’s audit," and get a ready-to-screenshot report in under two minutes.
- **Zero cost beyond your Claude subscription.** No AWS, no Resend, no cron, no VPS.

-----

## Prerequisites

1. **iPad with Claude.ai** -- either the Claude iOS app from the App Store, or Safari pointed at `claude.ai`. Both work; the app is smoother for file uploads.
1. **Claude subscription** -- Free works for light use, but Pro ($20/mo) is strongly recommended because Projects, the artifact storage feature, and extended thinking all benefit from higher usage limits.
1. **Settings to enable** (tap your name → Settings):
- **Web search**: ON -- so Claude can pull current CostcoInsider deals without you copy-pasting.
- **Memory**: ON (optional but recommended) -- remembers preferences across Projects.
- **Artifacts**: ON (default).
1. **Your recent Costco receipts** -- as PDFs in Files, photos in Photos, or emails in Mail. Digital receipts from Costco’s email work great.

-----

## Part 1: Create the Project (one time, ~5 minutes)

### Step 1.1 -- Open Claude.ai and create a new Project

**What to do:** In the Claude app, tap the sidebar icon (top-left), then tap **Projects**, then **+ New Project**.

**What to enter:**

- **Name:** `Costco Price Auditor`
- **Description:** `Parses my Costco receipts, matches them against current deals, and tells me what I can claim at the membership counter within the 30-day window.`

**Expected outcome:** An empty Project page with sections for Project Instructions, Project Knowledge, and Chats.

-----

### Step 1.2 -- Paste the Project Instructions

**What to do:** Tap **Set project instructions** (or the pencil icon next to Instructions). Paste the block below verbatim. Tap **Save Instructions**.

**Paste this:**

```
You are the Costco Price Auditor. You help the user reclaim money through Costco's 30-day price adjustment policy by parsing receipts and cross-referencing them against current deals.

## Your three core jobs

1. **Parse receipts.** When the user uploads a receipt image or PDF, extract every line item into structured JSON (see the Receipt Parser prompt in Project Knowledge).

2. **Find matches.** When the user asks you to "run the audit" or "check for adjustments," compare their recent purchases against current Costco deals. Use web search to pull the latest deals from costcoinsider.com. Use extended thinking for the matching logic (see the Deal Matcher prompt in Project Knowledge).

3. **Compose the report.** Produce a clean HTML report as an Artifact showing (a) price adjustments the user can claim and (b) Temporary Price Drops Costco already applied at checkout.

## Operating rules

- Default to the Receipt Tracker artifact for anything involving stored data. When the user uploads a receipt, add it to the tracker. When they ask to see their receipts, open the tracker.
- Always show your reasoning for matches with confidence below 0.90 so the user can sanity-check before walking into Costco.
- Currency always formatted as $X.XX. Dates as "Apr 12, 2026".
- Costco's price adjustment window is 30 days from purchase date. Anything older is out of scope; say so clearly.
- Expand Costco receipt abbreviations when you extract them. "CKN/VEG DUMP" is dumplings, "T TURTLENECK" is a Tahari turtleneck, "KS" prefix means Kirkland Signature.
- If a receipt is unreadable or clearly not Costco, tell the user and stop.

## Tone

Direct, friendly, no fluff. The user is a builder who appreciates precision. Show numbers, show your work, don't pad.
```

**Expected outcome:** The instructions appear in the Project sidebar. Every chat inside this Project will now start with this context baked in.

-----

### Step 1.3 -- Add the Receipt Parser prompt to Project Knowledge

**What to do:** Tap **Add content** under Project Knowledge → **Add text**. Title it `Receipt Parser Prompt`. Paste the block below. Tap **Save**.

**Paste this:**

```
# Receipt Parser Prompt

When the user uploads a Costco receipt (PDF or image), use these rules to extract line items.

## Output format
Return a single JSON object, then a short human-readable summary. No markdown fences around the JSON.

{
  "purchase_date": "YYYY-MM-DD",
  "warehouse": "city or warehouse number if visible",
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

## Rules

1. line_position is the order on the receipt, starting at 1.
2. item_number is the 6–7 digit Costco SKU next to each item. Null if missing.
3. description is the raw receipt text, uppercase, abbreviations intact.
4. normalized_description is your plain-English expansion:
   - "CKN/VEG DUMP" → "Chicken & Vegetable Dumplings"
   - "T TURTLENECK" → "Tahari Turtleneck Sweater"
   - "KS PAPER TWL" → "Kirkland Signature Paper Towels"
   - "ORG BABY SPIN" → "Organic Baby Spinach"
5. price_paid is the final per-line price after any TPD already applied at checkout.
6. If a line like "TPD/1234567 -3.00" appears, attach it to the preceding item: tpd_applied=true, tpd_amount=3.00, price_paid reflects the post-discount amount.
7. Ignore tax, subtotals, payment lines, and the barcode at the bottom.
8. If unreadable or not a Costco receipt, return {"error": "reason"} and stop.

## After parsing

Call the Receipt Tracker artifact and add the new receipt. Then give the user a one-line confirmation: "Added 12 items from Apr 12 receipt, total $247.83."
```

**Expected outcome:** A new entry appears in Project Knowledge. Claude will reference it whenever you upload a receipt.

-----

### Step 1.4 -- Add the Deal Matcher prompt to Project Knowledge

**What to do:** Add another text file to Project Knowledge. Title it `Deal Matcher Prompt`. Paste the block below.

**Paste this:**

```
# Deal Matcher Prompt

When the user asks to "run the audit" or "check for adjustments," do the following:

## Step 1 -- Gather inputs
- Today's date.
- All receipts in the Receipt Tracker artifact with purchase_date within the last 30 days.
- Current active Costco deals. Use web search: query "costcoinsider.com current coupon book" and fetch the most recent monthly savings post. Also check for a weekly hot buys post. Extract item_number, description, sale_price, regular_price, valid_from, valid_to for every deal listed.

## Step 2 -- Think through each purchase
Use extended thinking. For each line item in each receipt within the 30-day window:

1. Days elapsed between purchase_date and today. If > 30, skip.
2. Search active deals for a match:
   - Exact item_number match → confidence 0.95–1.00.
   - Clear normalized_description match (brand, size, variety all agree) → 0.75–0.94.
   - Plausible but ambiguous match → 0.50–0.74. Still return it, but flag it.
   - Anything below 0.50 → not a match.
3. Among matching deals, pick the lowest sale_price.
4. If sale_price < (price_paid - tpd_amount), this is an adjustment.
5. savings = (price_paid - tpd_amount) - sale_price.

## Step 3 -- Handle edge cases
- Same item bought twice on one receipt: match both lines independently. Both qualify.
- Deal only counts if today falls between valid_from and valid_to.
- If the user already got a TPD at checkout, use the post-TPD price when comparing.

## Step 4 -- Produce the report
Generate (or update) the Price Match Report artifact with two tables:

**Table 1 -- Price Adjustments Available** (sorted by savings desc):
Item | Purchased | Paid | Current Sale | Savings | Confidence

**Table 2 -- TPD Savings Already Applied** (informational, from receipts in the past 7 days):
Item | Purchased | Regular | Paid | Saved

Header line: "Found $X.XX in adjustments across N items. Take your receipts to the membership counter."

Footer: "Bring receipts within 30 days of purchase."

Style: system-ui font, clean tables with 1px borders and #f9f9f9 alternating rows, savings column bold green (#2d8a3e), max-width 640px centered. Below-0.80 confidence rows get a ⚠️ marker and a small note.
```

**Expected outcome:** Second knowledge entry saved. Claude now has the matching logic available on demand.

-----

### Step 1.5 -- Create the Receipt Tracker artifact

This is the persistent data store. It lives as an Artifact inside the Project and uses Claude’s artifact storage API to remember receipts across sessions.

**What to do:** Start a new chat inside the Project. Send this exact message:

> Create a React artifact called "Receipt Tracker" that persistently stores my Costco receipts and matches using window.storage. It should have:
> 
> - A tab view with three tabs: Receipts, Matches, Stats.
> - **Receipts tab**: list of receipts, each showing purchase_date, warehouse, total, and expandable line items. A "Delete" button per receipt.
> - **Matches tab**: list of matches stored from past audits, each showing item, savings, confidence, and date matched. Sortable by savings.
> - **Stats tab**: lifetime savings claimed, receipts processed, matches found, average weekly savings.
> - A "Clear all data" button in Stats with a confirmation prompt.
> - Storage keys: `receipts:{id}` for each receipt, `matches:{id}` for each match, `stats` for aggregates. Use shared=false so it’s private to me.
> - Load all data on mount, show a spinner while loading, handle empty states gracefully.
> - Style it clean and minimal: white background, system-ui, rounded cards, subtle shadows.
> 
> Also expose two helper functions I can ask you to call in future chats: `addReceipt(receiptJson)` and `addMatch(matchJson)`. When I paste in receipt JSON you’ve extracted, update this artifact.

**Expected outcome:** Claude generates a React artifact that renders on the right side of the chat (or full-screen on iPad). It will be empty at first. The artifact persists -- when you come back in a week, open the Project, open this artifact, and your receipts are still there.

**Pin it:** Tap the artifact’s title, then the pin icon or "Add to project." This keeps it accessible from the Project sidebar.

-----

### Step 1.6 -- Test the setup with a sample receipt

**What to do:** In the same chat, upload any Costco receipt (tap the + icon, then Photo Library or Files). Say:

> Parse this receipt using the Receipt Parser Prompt and add it to the Receipt Tracker.

**Expected outcome:**

- Claude reads the image.
- Returns structured JSON with your line items, expanded descriptions, any TPDs detected.
- Updates the Receipt Tracker artifact -- open it and the receipt appears under the Receipts tab.
- Gives you a one-line confirmation like "Added 14 items from Apr 12 receipt, total $247.83."

If the JSON looks wrong (bad item numbers, missed TPDs, garbled descriptions), go back to Project Knowledge, edit the Receipt Parser Prompt to address the issue, and re-upload. This is the prompt-iteration loop the original AWS article talked about -- done in 30 seconds, no redeploy.

-----

## Part 2: Weekly Usage (ongoing, ~2 minutes per week)

### Step 2.1 -- Collect the week’s receipts

**What to do:** Over the week, as you shop, save receipts one of these ways:

- **Paper receipts:** Open Notes or Files on iPad, tap Camera → Scan Documents, scan the receipt. Saves as PDF.
- **Digital receipts from Costco email:** Save the PDF attachment to Files.
- **Photo of receipt:** Just take a photo. Claude’s vision handles photos fine.

Keep them in a single Files folder called `Costco Receipts/Unprocessed` so you can grab them all at once.

**Expected outcome:** A folder with however many receipts you collected this week. Typically 1–3 for most households.

-----

### Step 2.2 -- Friday night (or whenever): run the audit

**What to do:** Open the Claude app → Projects → Costco Price Auditor → **+ New Chat**.

Send this message, attaching all unprocessed receipts:

> Here are this week’s receipts. Parse each one, add them to the Receipt Tracker, then run the audit: fetch current CostcoInsider deals via web search, match against all receipts from the last 30 days in my tracker, and produce the Price Match Report artifact.

**Expected outcome:** Claude will:

1. Parse each receipt (watch the JSON stream in).
1. Update the Receipt Tracker artifact.
1. Search the web for current deals (you’ll see a "Searching…" indicator).
1. Think through matches with extended thinking visible.
1. Generate a Price Match Report artifact with your two tables.

This takes 60–90 seconds depending on how many receipts you uploaded.

-----

### Step 2.3 -- Review the report

**What to do:** Tap the Price Match Report artifact to open it full-screen. Scan Table 1 for adjustments you can claim.

**Expected outcome:** Something like:

> **Found $12.00 in adjustments across 3 items. Take your receipts to the membership counter.**
> 
> |Item              |Purchased|Paid  |Current Sale|Savings    |Confidence|
> |------------------|---------|------|------------|-----------|----------|
> |Kirkland Dumplings|Apr 12   |$14.99|$11.99      |**$3.00**  |0.98      |
> |Tahari Turtleneck |Apr 10   |$24.99|$19.99      |**$5.00**  |1.00      |
> |Organic Spinach   |Apr 14   |$7.49 |$5.49       |**$2.00** ⚠️|0.76      |
> 
> ⚠️ Spinach match is lower confidence -- description matches but item number wasn’t visible on receipt. Verify at counter.

-----

### Step 2.4 -- Screenshot or share the report

**What to do:** Take a screenshot of the artifact (top button + home button, or top button + volume up on newer iPads). Or tap the artifact’s share icon → AirDrop to yourself, email it, or save to Files.

**Expected outcome:** You have a portable version of the report to take to Costco. The item names, prices, and item numbers are all you need at the membership counter.

-----

### Step 2.5 -- Walk into Costco Saturday morning

**What to do:** Bring your original receipts and your screenshot. Go to the membership counter. Show them: "I bought these within the last 30 days, and they’re on sale now. I’d like a price adjustment."

**Expected outcome:** They refund the difference to your card. Takes 2–5 minutes at the counter.

-----

### Step 2.6 -- Mark as claimed (optional)

**What to do:** Back in Claude, open the Receipt Tracker artifact → Matches tab. Add a note or toggle a "claimed" checkbox for the items you got refunded. This keeps your Stats tab accurate.

**Expected outcome:** Lifetime savings number goes up. Satisfying.

-----

## Part 3: Maintenance & Iteration

### When the Receipt Parser misses something

**Symptom:** Claude extracts the wrong price, misses a TPD, or garbles a description.

**Fix:**

1. Open the Project → Project Knowledge → Receipt Parser Prompt.
1. Add the specific case to the abbreviations list or rules section.
1. Re-upload the receipt and say "re-parse with the updated rules."

Takes less than a minute. No deploy, no code.

-----

### When the deal scraper misses deals

**Symptom:** You know an item’s on sale but Claude didn’t find the match.

**Fix:** In the audit chat, say:

> Also search costco.com for current weekly hot buys on [item name], and check the r/Costco current deals thread.

Claude will broaden its search. If you find a reliable secondary source, add it to the Deal Matcher Prompt permanently:

> In Step 1 also search [new source URL] for additional deals.

-----

### When the report format isn’t quite right

**Symptom:** Tables too wide, colors off, missing a column you want.

**Fix:** Just say it in chat: "Add a column showing the item number. Make the table full width on mobile. Remove the confidence column for matches above 0.95."

Claude updates the artifact in place. Next week’s report uses the new format because the Project Instructions now remember your preferences (or pin the adjusted prompt back into Project Knowledge to be sure).

-----

## Part 4: What You’re Giving Up vs. The Coded Version

**Giving up:**

- **True automation.** Nothing fires Friday at 9 PM by itself. You have to open the app. Realistically this takes two minutes a week and you’re going to Costco on Saturday anyway.
- **Email delivery.** The report is an artifact, not an email. Screenshots work fine, but if you really want email, forward the screenshot to yourself.
- **Multi-user support.** Only you can see your Project. Not a limitation for personal use.

**Gaining:**

- **Zero setup beyond these steps.** No AWS account, no CDK, no Docker, no API keys, no SES verification.
- **Zero hosting cost.** Just your Claude subscription.
- **Zero maintenance.** Nothing to patch, nothing to redeploy when a dependency updates.
- **Instant prompt iteration.** Edit the Project Knowledge and the next run uses the new prompt.
- **Fully mobile.** Every step works on iPad. Most steps work on iPhone too.

-----

## Part 5: Optional Upgrades Later

### 5.1 Shortcut for faster receipt capture

Build an iOS Shortcut: "Share receipt to Costco Auditor." Takes a photo or PDF from the Share Sheet, opens Claude.ai with a pre-typed prompt "Parse this receipt and add to tracker," and attaches the file. Cuts your weekly workflow from two minutes to thirty seconds.

**How:** Shortcuts app → + → Add Action → Receive [Images, Files] from Share Sheet → Add Action → Open URLs → URL: `claude.ai/project/<your-project-id>` → save. Not perfect (you still tap send) but close.

### 5.2 Email-in receipts

Forward your Costco email receipts to yourself at a dedicated address, then once a week dump the whole folder into Claude in one batch. Keeps you from interrupting yourself mid-week.

### 5.3 Scheduled reminder (not scheduled execution)

Set a repeating reminder: "Friday 9 PM -- run Costco audit." Reminder fires, you tap the notification, it deep-links into the Project. You’re back to two minutes a week.

### 5.4 Upgrade to the coded version later

If you outgrow this and want real automation, the prompts in Project Knowledge drop directly into the build spec from the earlier README. Nothing you do here is throwaway.

-----

## Summary Checklist

Setup (one time):

- [ ] Enable web search and artifacts in Claude settings.
- [ ] Create the "Costco Price Auditor" Project.
- [ ] Paste the Project Instructions.
- [ ] Add Receipt Parser Prompt to Project Knowledge.
- [ ] Add Deal Matcher Prompt to Project Knowledge.
- [ ] Create the Receipt Tracker artifact.
- [ ] Test with one sample receipt.

Weekly:

- [ ] Scan/save new receipts to Files.
- [ ] Open Project, new chat, upload receipts, say "run the audit."
- [ ] Screenshot the report.
- [ ] Go to Costco, collect money.

That’s the whole system. Built on an iPad, runs on an iPad, costs nothing extra.