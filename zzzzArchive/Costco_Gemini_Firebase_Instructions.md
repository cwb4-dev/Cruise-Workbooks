# Costco Receipt Scanner & Price Match Agent: Gemini-Firebase Edition

This project is a "Simple, Elegant, and Couch Potato" implementation of a Costco price matching agent. It uses the Google/Firebase toolchain to automate the process of checking receipts against current deals with "maximum curiosity and minimum friction."

## Overview
- **Goal**: Automate price adjustment claims for Costco purchases within a 30-day window.
- **Philosophy**: No over-engineered code. Use Gemini's multimodal reasoning to replace complex OCR and scrapers.
- **Stack**: Firebase (Hosting, Functions, Firestore, Storage) + Gemini 2.0 Flash via Vertex AI.

---

## Step 1: Sandbox & Vibe Coding in Google AI Studio
Before building the "factory," we perfect the "brain" in the sandbox.

1. **Access AI Studio**: Go to [aistudio.google.com](https://aistudio.google.com).
2. **Select Model**: Choose **Gemini 2.0 Flash**. It provides the best balance of multimodal speed and reasoning for reading messy receipts.
3. **Draft the "Couch Potato" Prompt**:
   - Upload a photo of a recent Costco receipt.
   - Paste the following into the system instructions:
     > "You are the Costco Savings Guru. Analyze this receipt image. Extract the Date, Item Numbers, and Prices. Match these against current Costco warehouse savings. If an item bought within the last 30 days is now on sale, calculate the refund. Identify 'TPD' (Temporary Price Drops) already applied. Output a clean report with the exact phrase to say at the membership desk."
4. **Test & Iterate**: Ensure Gemini correctly identifies shorthand like 'CKN/VEG DUMP' without manual mapping.

---

## Step 2: Initialize the Project in Firebase Studio
Firebase Studio acts as your unified command center, using Gemini 2.5 Pro to help you build.

1. **Create Project**: Open **Firebase Studio** and create a new project.
2. **Enable Agent Mode**: Use the built-in AI Agent to scaffold the app.
3. **Configure Services**:
   - **Firestore**: For storing purchase history and deal logs.
   - **Cloud Storage**: To hold receipt images.
   - **Firebase Auth**: To secure your personal data.
   - **App Hosting**: To deploy the web dashboard.

---

## Step 3: Implement the Logic with Firebase Genkit
Genkit is the "glue" that connects Gemini to your data with minimal code.

1. **Define the Schema**: Create a simple "Receipt" and "Deal" schema in Firestore.
2. **Create the 'Price Match' Flow**:
   - Use Genkit to wrap your AI Studio prompt.
   - Set up a **multimodal input** so the flow accepts raw images directly from Cloud Storage.
3. **Tool Calling**: Connect the agent to a "Search Tool" via **Vertex AI Agent Builder**. This allows Gemini to search the web for the latest Costco coupon book text automatically.

---

## Step 4: Automate with Scheduled Cloud Functions
The true "Couch Potato" step—making it run while you're on the sofa.

1. **Create a Scheduled Function**: Set a Cloud Function to trigger every Friday at 9 PM (or your preferred time).
2. **The Logic**:
   - The function triggers the Genkit flow.
   - It pulls all receipts uploaded in the last 30 days.
   - It queries the latest deals.
3. **Notification**: Use **Firebase Extensions** (like "Send Email with Resend or Mailgun") to email you the final HTML report.

---

## Step 5: The "Couch Potato" Web UI
A single-page app (SPA) for easy uploads from your phone or laptop.

1. **Frontend**: A simple HTML/Tailwind file hosted on **Firebase Hosting**.
2. **Upload Function**: A "Drop Zone" that pushes files to Cloud Storage, which automatically triggers a metadata update in Firestore.
3. **Live Feedback**: Use Firestore's real-time listeners to watch the AI "think" through your receipts as it matches them to deals.

---

## Deployment
1. **Local Testing**: Run `firebase emulators:start` to test the logic locally.
2. **Deploy**: Run `firebase deploy`.
3. **Usage**: Snap a photo of your receipt at the Woodbury Costco, upload it, and wait for your Friday evening savings report.

---

## Why This Beats the AWS Version
- **No Manual OCR**: Gemini's native vision replaces the Nova/OCR pipeline.
- **Single SDK**: Manage everything through the Firebase ecosystem.
- **Massive Context**: Feed a whole month's worth of receipts into one prompt thanks to Gemini's 1M+ token window.
