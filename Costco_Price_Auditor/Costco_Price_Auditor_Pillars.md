# Costco Price Auditor: Gemini-Firebase Edition

This project is a "Simple, Elegant, and Professional" implementation of a Costco price matching utility. It leverages **Gemini 2.0 Flash** and **Firebase Genkit** to automate the process of checking receipts against current deals with "maximum curiosity and minimum friction".

## Overview
- **Goal**: Automate price adjustment claims within the 30-day Costco window.
- **Philosophy**: Use "Prompt-Based" architecture to handle messy receipt data and warehouse abbreviations without over-engineered manual code.
- **Tech Stack**: Firebase Studio, Gemini 2.0 Flash (Multimodal), Firebase Genkit, and Firestore.

---

## Pillar 1: Prototyping Focus (Firebase Studio Agent)
Eliminate manual infrastructure setup by using natural language to scaffold the app.

1.  **Open Firebase Studio**: Launch a new project and enter **Agent Mode** [cite: 2.1].
2.  **Describe the App**: Use a high-level prompt to generate the foundation:
    > "Build a web dashboard where I can upload Costco receipt photos. Use Gemini to extract the date and item numbers into Firestore. Create a scheduled logic that compares these items to the current monthly savings book." [cite: 2.1, 5.1]
3.  **Zero-Infrastructure Setup**: The Agent handles provisioning the database (Firestore), storage (Cloud Storage), and hosting automatically based on your description [cite: 2.1, 6.2].

---

## Pillar 2: Dotprompt Logic (.prompt files)
Replace hard-coded parsing with editable text files to refine how Gemini reads your receipts.

1.  **Create `receipt-parser.prompt`**: This is a standalone file that defines your AI's behavior [cite: 1.1, 5.2].
    * **Model**: Gemini 2.0 Flash [cite: 5.1].
    * **System Instructions**: 
        > "Act as a Costco inventory expert. Read this receipt image. Extract Item IDs, Prices, and Dates. Correct abbreviations (e.g., 'CKN/VEG DUMP' = Dumplings). Return a JSON object for Firestore." [cite: 1.1, 5.1]
2.  **Iterative Refinement**: Instead of changing code, you simply edit the text in the `.prompt` file to handle new Costco abbreviations as they appear [cite: 5.2].

---

## Pillar 3: Genkit Integration (The Wiring)
Use Genkit to "wire" your AI prompts directly to Firestore and Cloud Functions with minimal code.

1.  **Define the Flow**: Use Genkit to create an automated "Flow" that takes a receipt from Cloud Storage, sends it to your `.prompt` file, and saves the output to **Firestore** [cite: 4.2, 6.2].
2.  **Unified SDK**: Genkit manages the authentication and data mapping between the Gemini model and your Firebase services, reducing the "friction" of manual API calls [cite: 4.2].
3.  **Dev UI Debugging**: Use the Genkit Developer UI to run your flows locally and watch the data move from the receipt photo into your database in real-time [cite: 4.2].

---

## Pillar 4: Native Thinking (The Reasoning)
Utilize Gemini's internal "Thinking" process to handle the 30-day window logic.

1.  **Reasoning Instructions**: In your prompt, instruct Gemini to "Think step-by-step" [cite: 3.2].
2.  **Complex Matching**: Tell the model:
    > "Analyze the purchase date and current date. Think through the 30-day price match window. If the current date is within 30 days of purchase and the current price is lower, flag this for a refund." [cite: 3.2]
3.  **Accuracy**: This native reasoning allows Gemini to handle calendar logic and multi-item price comparisons without requiring complex mathematical code in your backend [cite: 3.1, 3.2].

---

## Deployment & Usage
1.  **Deploy**: Run `firebase deploy` to push the prompt-driven infrastructure to the cloud [cite: 2.1].
2.  **Auditor Run**: A **Scheduled Cloud Function** triggers the Genkit flow every Friday to generate your savings report [cite: 2.1, 4.2].
