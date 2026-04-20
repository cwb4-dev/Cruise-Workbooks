# Costco Price Auditor: The "No-Code" Gemini & Firebase Blueprint

This project implements the full functionality of the AWS "Price Match Agent" using an entirely prompt-based workflow. By leveraging **Firebase Studio** and **Genkit**, you move from architect to owner without writing traditional manual code.

## Overview
- **Goal**: Reclaim money from Costco price drops within 30 days.
- **Method**: 100% Prompt-driven development and AI reasoning.
- **Tools**: Firebase Studio (Agent Mode), Gemini 2.0 Flash, Genkit (.prompt files).

---

## Pillar 1: App Scaffolding (Natural Language Only)
Instead of writing CDK or infrastructure-as-code, you "talk" your app into existence.

1.  **Launch Firebase Studio Agent**: Open your project and enter **Agent Mode**.
2.  **The "Master App" Prompt**: Enter the following:
    > "Create a web application for auditing Costco receipts. It needs a secure upload zone for images, a Firestore database to store item details, and a dashboard to show potential refunds. Set up the backend to trigger a Gemini analysis whenever a new receipt is uploaded."
3.  **Automatic Provisioning**: The Agent automatically configures **Cloud Firestore**, **Cloud Storage**, and **Firebase Auth** based on this description.

---

## Pillar 2: Logic via Dotprompt (.prompt Files)
You replace complex Python parsing logic with a single text-based prompt file that Gemini follows.

1.  **Create `auditor-logic.prompt`**: This file acts as the "brain" of your auditor.
2.  **The Instructions**:
    * **Model**: Gemini 2.0 Flash.
    * **Input**: Receipt Image + Current Deal Text.
    * **Instructions**:
        > "1. Extract the Item ID and price from the image. 
        > 2. Compare it to the provided deal text. 
        > 3. If a match is found and the current price is lower, calculate the difference. 
        > 4. Handle shorthand (e.g., 'CKN/VEG DUMP' is Dumplings). 
        > 5. Output only a structured JSON object."
3.  **Refinement**: If Costco changes their receipt format, you simply edit the text in this file. No code changes required.

---

## Pillar 3: Automation & Wiring (Genkit Flows)
Genkit allows you to "wire" your database to your AI using simple flow definitions.

1.  **The Flow Prompt**: Tell the Firebase Studio Agent:
    > "Create a Genkit Flow that takes an image from my storage bucket, runs it through my 'auditor-logic.prompt', and saves the resulting JSON into the 'receipts' collection in Firestore."
2.  **Scheduled Execution**: Instruct the Agent to "Create a scheduled Cloud Function that runs this flow every Friday at 9 PM to check for new warehouse deals."

---

## Pillar 4: Native Thinking (Calendar Logic)
Instead of writing math functions to calculate "30 days from today," you let Gemini "think" through the dates.

1.  **Reasoning Instructions**: Add a "Thinking" block to your prompt:
    > "Think through the dates. If the purchase date on the receipt is more than 30 days before today's date, ignore the item. If it is within 30 days, proceed with the price comparison."
2.  **The Result**: Gemini uses its internal reasoning to handle leap years, month lengths, and date formatting automatically.

---

## Why This is the "Minimum Friction" Path
- **No SDK Guesswork**: You don't have to guess undocumented ARN formats like the AWS version.
- **Natural Language Iteration**: You "code" by talking to the Firebase Agent.
- **Unified Tooling**: Everything lives in one Firebase project, accessible from your iPad or MacBook Air.
