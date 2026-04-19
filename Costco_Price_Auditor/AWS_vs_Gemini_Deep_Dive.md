# Deep Dive: AWS Bedrock vs. Gemini Prompt-Only Architecture

This document provides a high-fidelity comparison between the original AWS-based Costco Price Match Agent and the "Simple, Elegant" Gemini/Firebase Prompt-Only rewrite. 

## 1. Functional Logic: "Systems" vs. "Instructions"

| Feature | AWS Bedrock (Traditional "Building") | Gemini Prompt-Only ("Directing") |
| :--- | :--- | :--- |
| **OCR & Parsing** | Uses a multi-model pipeline. Nova 2 Lite performs initial extraction; if confidence is low, Nova Premier is triggered for a second pass. | **Native Multimodal**: Gemini 2.0 Flash reads the image and interprets the text in a single "glance." No secondary pass is needed. |
| **Shorthand Mapping** | Requires Python mapping or secondary AI logic to decode terms like "CKN/VEG DUMP" or "T TURTLENECK." | **Semantic Context**: Handled entirely within the `.prompt` file. You simply tell the AI, "Interpret abbreviations based on common Costco warehouse terminology." |
| **Match Reasoning** | Hard-coded logic comparing Item IDs and prices. The AI acts as a data extractor, and the code acts as the matcher. | **Cognitive Match**: Gemini's **Native Thinking** process reasons through the match. It analyzes "Unit Price" vs "Package Price" naturally. |

## 2. Infrastructure: "Stacks" vs. "Agents"

### AWS Bedrock (The Article Approach)
- **Deployment**: Three CDK stacks (Common, Amplify, AgentCore) written in TypeScript.
- **Maintenance**: Requires updating infrastructure-as-code (CDK) to change how the data flows.
- **Permissions**: Manually defined IAM policies for Lambda, S3, DynamoDB, and Bedrock.
- **The "Plumbing"**: You must manage the Docker container for the agent and the EventBridge scheduler targets.

### Gemini Prompt-Only (The Firebase Approach)
- **Deployment**: A single conversation with the **Firebase Studio Agent**. 
- **Maintenance**: "Vibe Coding." You update the app's behavior by describing the new requirements to the Agent.
- **Permissions**: Handled by Firebase's unified security rules, which are provisioned automatically during the prompt-based setup.
- **The "Flow"**: Genkit replaces complex containers. The "logic" is a simple text file (.prompt) wired to a database.

## 3. The Date Problem: "Math" vs. "Thinking"

Costco's 30-day window is a logic challenge.

- **AWS Implementation**: Relies on `datetime` Python libraries to calculate the delta between `purchase_date` and `current_date`.
- **Gemini Implementation**: Uses **Native Thinking**. The prompt instructs: *"Think about the calendar. Is today within 30 days of the purchase date? Account for month lengths and year transitions."* This removes the need for custom date-parsing code that often breaks on edge cases.

## 4. Cost and Efficiency

- **AWS**: Extremely cheap (~$0.10/week), but carries "technical debt" in the form of managed resources (ECR images, Lambda layers).
- **Gemini**: Similarly priced, but with **Zero Technical Debt**. There are no containers to patch or IAM roles to audit. The "code" is just a set of instructions.

## 5. Summary of the "Couch Potato" Advantage

The Gemini Prompt-Only version is the realization of "maximum curiosity, minimum friction." 
- **The Builder (AWS)**: Spends 80% of their time on the cloud environment and 20% on the AI.
- **The Architect (Gemini)**: Spends 5% of their time on the environment and 95% on perfecting the prompt logic to get the most money back from Costco.
