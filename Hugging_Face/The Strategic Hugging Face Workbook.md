# 🤗 The Strategic Hugging Face Workbook

> **From API Consumer to ML Engineer** — A curated journey through 5 progressively complex projects that build real-world AI skills.

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)]https://www.python.org/downloads/)
[![Hugging Face](https://img.shields.io/badge/🤗-Transformers-yellow)](https://huggingface.co/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

---

## 🎯 Why This Repository Exists

Most tutorials teach you *how* to run code. This workbook teaches you **why** each project matters in the real world. Each project is strategically chosen to build a specific skill:

| Project | The "Why" (Career Skill) | Difficulty |
| :--- | :--- | :--- |
| **1. Sentiment** | 🧠 **Orchestration** - Swapping models like Lego bricks | ⭐ Easy |
| **2. Summarization** | 🔗 **Composition** - Chaining models to save cloud costs | ⭐⭐ Easy-Medium |
| **3. Disaster Tweets** | 🎯 **Adaptation** - Fine-tuning for custom domains | ⭐⭐⭐ Medium |
| **4. NER & Tokenizers** | ⚙️ **Mastery** - Rebuilding core components & label alignment | ⭐⭐⭐⭐ Hard |
| **5. Gradio Deployment** | 🚀 **Distribution** - End-to-end product delivery & MLOps | ⭐⭐⭐⭐⭐ Expert |

---

## 🗺️ Learning Journey Visual

```
Level 1 (Easy)          Level 5 (Hard)
    │                       │
    ▼                       ▼
┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐
│ Sent.  │─▶│ Summ.  │─▶│ Fine-  │─▶│ Token- │─▶│ Gradio │
│ Analy- │  │ + ZSL  │  │ tuning │  │ izer   │  │ Deploy │
└────────┘  └────────┘  └────────┘  └────────┘  └────────┘
    │           │           │           │           │
    ▼           ▼           ▼           ▼           ▼
 Orchestrate  Compose    Adapt      Rebuild     Ship
```

---

## 📚 Table of Contents

1. [Project 1: The "No-Code" Sentiment Analyzer](#-project-1-the-no-code-sentiment-analyzer)
2. [Project 2: Summarization & Zero-Shot Classification](#-project-2-summarization--zero-shot-classification)
3. [Project 3: Fine-tuning DistilBERT for Disaster Tweets](#-project-3-fine-tuning-distilbert-for-disaster-tweets)
4. [Project 4: Training a Custom Tokenizer + NER](#-project-4-training-a-custom-tokenizer--ner)
5. [Project 5: Serving with Gradio + HF Spaces](#-project-5-serving-with-gradio--hf-spaces)
6. [Quick Start](#-quick-start)
7. [Contributing](#-contributing)

---

## 🛠️ Quick Start

Want to jump straight to a specific project?

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/huggingface-workbook.git
cd huggingface-workbook

# Install dependencies (for all projects)
pip install -r requirements.txt

# Run Project 1 (Sentiment Analysis)
cd project_1_sentiment
python sentiment.py

# Run Project 5 (Gradio Web App)
cd ../project_5_gradio
python app.py
```

---

## 🌐 Live Demo

Check out the deployed Disaster Tweet Classifier from Project 5:

[![Hugging Face Spaces](https://img.shields.io/badge/🤗-Spaces-yellow)](https://huggingface.co/spaces/YOUR_USERNAME/disaster-tweet-classifier)

---

# 📖 The Projects

---

## Project 1: 🪴 The "No-Code" Sentiment Analyzer
**Difficulty:** ⭐ (Easy)  
**Core Concept:** `pipeline()` API & Model Hub Discovery  
**Time:** 15 minutes

### 🧠 Why This Project?
Most people quit ML because they think they need a Ph.D. to run a model. This project destroys that barrier in 5 minutes.

- **The Skill:** Learning the `pipeline` abstraction means you can now perform **any** NLP task (translation, summarization, question-answering) with the exact same syntax.
- **The Strategy:** It forces you to navigate the Hugging Face Hub. If you can swap a sentiment model for a NER model just by changing the handle (e.g., `"cardiffnlp/twitter-roberta"`), you are no longer a coder—you are an **AI orchestrator**.

### ✅ Pre-requisites
```bash
pip install transformers
```

### 📝 Steps

**1. The Basic Pipeline**
Create `sentiment.py`. This downloads the model and runs inference in 2 lines.

```python
from transformers import pipeline

# Checkpoint: You just downloaded 250MB of AI weights in seconds.
classifier = pipeline("sentiment-analysis")

result = classifier("I absolutely loved the new update, it fixed all my bugs!")
print(result)
# Output: [{'label': 'POSITIVE', 'score': 0.9998}]
```

**2. Batch Processing (The Performance Hack)**
Pipelines accept lists. Processing in bulk is 10x faster than looping because the GPU processes matrices in parallel.

```python
texts = [
    "This app crashes every single time I open it.",
    "The UI is decent, but the performance is sluggish.",
    "Customer support resolved my issue in 5 minutes. Amazing!"
]

results = classifier(texts)
for text, res in zip(texts, results):
    print(f"{res['label']} ({res['score']:.2f}) -> {text[:30]}...")
```

**3. The "Hub" Skill (Swapping Models)**
Go to [huggingface.co/models](https://huggingface.co/models). Filter by "Text Classification". Find `cardiffnlp/twitter-roberta-base-sentiment-latest`. This is trained on Twitter, so it understands sarcasm and internet slang better than the default model.

```python
# Checkpoint: You are now using a state-of-the-art social media model.
social_classifier = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment-latest")

tweet = "I can't even with this update rn 🙄"
print(social_classifier(tweet))
# Notice the labels: LABEL_0 = Negative, LABEL_1 = Neutral, LABEL_2 = Positive
```

---

## Project 2: 📝 Summarization & Zero-Shot Classification
**Difficulty:** ⭐⭐ (Easy-Medium)  
**Core Concept:** Task-specific Pipelines & Multi-step Chaining  
**Time:** 20 minutes

### 🧠 Why This Project?
Real-world AI is rarely a single model. It is a **pipeline**.

- **The Skill:** This teaches you **task composition**—using the output of Model A as the input for Model B.
- **The Strategy:** Summarization shrinks massive text (saving cloud compute costs), and Zero-Shot classification lets you tag data without retraining. This exact architecture is used by legal tech companies to summarize court documents and tag them by practice area, and by news aggregators to categorize articles on the fly.

### ✅ Pre-requisites
```bash
pip install transformers torch
```

### 📝 Steps

**1. The Summarizer (Sequence-to-Sequence)**
We use BART, which is specifically fine-tuned for news summarization. Notice the `max_length` and `min_length` constraints.

```python
from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

LONG_TEXT = """
The Apollo 11 space mission was the first time humans landed on the Moon. 
It was launched by NASA on July 16, 1969. The crew consisted of Commander Neil Armstrong, 
Command Module Pilot Michael Collins, and Lunar Module Pilot Edwin "Buzz" Aldrin. 
Armstrong and Aldrin landed on the lunar surface on July 20, while Collins remained in orbit. 
Armstrong's first step onto the lunar surface was broadcast on live TV to a worldwide audience. 
He described the event as "one small step for a man, one giant leap for mankind." 
The mission returned to Earth on July 24, 1969, splashing down in the Pacific Ocean.
"""

summary = summarizer(LONG_TEXT, max_length=50, min_length=20, do_sample=False)
print(summary[0]['summary_text'])
```

**2. Zero-Shot Classifier (No Training Data Required)**
We pass a text and a list of candidate labels. The model gives a probability for each—no fine-tuning needed.

```python
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

candidate_labels = ["space exploration", "technology", "sports", "politics"]
result = classifier(LONG_TEXT, candidate_labels)

print(f"Predicted: {result['labels'][0]} with score {result['scores'][0]:.2f}")
```

**3. The "Chain" (Production Pattern)**
We summarize *first* (reducing token count) and then classify the summary. This reduces inference time and cloud costs significantly.

```python
def analyze_text(text):
    # Step 1: Shrink the text
    summary = summarizer(text, max_length=50, min_length=20, do_sample=False)[0]['summary_text']
    
    # Step 2: Tag the summary
    classification = classifier(summary, candidate_labels)
    
    return {
        "summary": summary,
        "top_label": classification['labels'][0],
        "confidence": classification['scores'][0]
    }

output = analyze_text(LONG_TEXT)
print(output)
```

---

## Project 3: 🧬 Fine-tuning DistilBERT for Disaster Tweets
**Difficulty:** ⭐⭐⭐ (Medium)  
**Core Concept:** `Trainer` API & `Dataset` loading  
**Time:** 30 minutes (plus training time)

### 🧠 Why This Project?
Pre-trained models are generalists. Your data is specific. A financial model fails on social media slang.

- **The Skill:** This forces you to confront the sacred trifecta of HF: **(Load Data) -> (Tokenize) -> (Train)**. It introduces the `Trainer` API, which abstracts away the ugly PyTorch training loops.
- **The Strategy:** If you can fine-tune a sentiment model on tweets, you can fine-tune BERT to detect legal clauses, medical conditions, or internal company support tickets. This is the **gatekeeper skill** that turns you from an "API caller" into an "ML Developer."

### ✅ Pre-requisites
```bash
pip install transformers datasets accelerate evaluate scikit-learn
```

### 📝 Steps

**1. Load the Dataset**
We use the famous `rcds/disaster_tweets` dataset. Target `1` = Real disaster, `0` = Not a disaster.

```python
from datasets import load_dataset

dataset = load_dataset("rcds/disaster_tweets")
print(dataset["train"][0]) # Check structure: {'text': "...", 'target': 0}
```

**2. Tokenization (The Critical Step)**
We convert text to `input_ids` (numbers). We use `padding="max_length"` to ensure all sequences are the same length for batch training.

```python
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

def tokenize_function(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=128)

tokenized_datasets = dataset.map(tokenize_function, batched=True)
```

**3. Prepare for PyTorch**
We remove raw text to save RAM and rename `target` to `labels` (the keyword the Trainer expects).

```python
tokenized_datasets = tokenized_datasets.remove_columns(["text", "id", "keyword", "location"])
tokenized_datasets = tokenized_datasets.rename_column("target", "labels")
tokenized_datasets.set_format("torch")

# Subset for speed (use 5k training, 1k validation)
train_dataset = tokenized_datasets["train"].shuffle(seed=42).select(range(5000))
eval_dataset = tokenized_datasets["train"].shuffle(seed=42).select(range(5000, 6000))
```

**4. Load Model & Training Arguments**
We load DistilBERT specifically for classification (`num_labels=2`). We set `load_best_model_at_end=True` to save the best checkpoint.

```python
from transformers import AutoModelForSequenceClassification, TrainingArguments, Trainer

model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased", num_labels=2)

training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    save_strategy="epoch",
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=3,
    weight_decay=0.01,
    load_best_model_at_end=True,
    metric_for_best_model="accuracy",
)
```

**5. Define Metrics & Trainer**
We need a function to compute accuracy during evaluation.

```python
import evaluate
import numpy as np

metric = evaluate.load("accuracy")

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    return metric.compute(predictions=predictions, references=labels)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    compute_metrics=compute_metrics,
)
```

**6. Train & Test**
Run the trainer, then test your custom model.

```python
trainer.train()
print(trainer.evaluate()) # Should hit ~75-80% accuracy

# Test on a new string
test_text = "A massive fire breaks out in downtown Los Angeles."
inputs = tokenizer(test_text, return_tensors="pt")
outputs = model(**inputs)
pred = outputs.logits.argmax(-1).item()
print("🚨 DISASTER" if pred == 1 else "✅ SAFE")
```

---

## Project 4: 🔬 Training a Custom Tokenizer + NER
**Difficulty:** ⭐⭐⭐⭐ (Hard)  
**Core Concept:** Custom Tokenizer Training & Token Classification Alignment  
**Time:** 45 minutes

### 🧠 Why This Project?
This is the **senior-level skill**. Everyone knows how to call `AutoTokenizer.from_pretrained()`. Almost nobody knows how to train one from scratch.

- **The Skill:** If you work in Healthcare (e.g., "remdesivir"), Finance (e.g., "NVDA"), or Legal (e.g., "§1983"), the base tokenizer will butcher your domain-specific words into meaningless subwords, increasing sequence length and slowing inference. Training your own Byte-Pair Encoding (BPE) tokenizer fixes this.
- **The Strategy:** Furthermore, **Token Classification (NER)** teaches you the hardest logic in NLP: *Label Alignment*. When a tokenizer splits a word into 3 subwords, how do you assign the NER tag to all 3? Mastering this means you can build production-grade Information Extraction systems.

### ✅ Pre-requisites
```bash
pip install transformers tokenizers datasets seqeval
```

### 📝 Steps

**1. Gather Domain Text (The Corpus)**
We need raw text to train the tokenizer. We load a medical QA dataset just to steal the text.

```python
from datasets import load_dataset

# We only use this for the raw strings to build the vocab
med_dataset = load_dataset("bigbio/med_qa", split="train")
raw_texts = med_dataset["question"] + med_dataset["answer"] 
```

**2. Train the BPE Tokenizer**
We start from scratch, set a small `vocab_size` (5,000) to see the effect, and save it.

```python
from tokenizers import Tokenizer
from tokenizers.models import BPE
from tokenizers.trainers import BpeTrainer
from tokenizers.pre_tokenizers import Whitespace

tokenizer = Tokenizer(BPE(unk_token="[UNK]"))
tokenizer.pre_tokenizer = Whitespace()

trainer = BpeTrainer(special_tokens=["[UNK]", "[CLS]", "[SEP]", "[PAD]", "[MASK]"], vocab_size=5000)
tokenizer.train_from_iterator(raw_texts, trainer)

tokenizer.save("med_tokenizer.json")
print(f"New Vocab size: {tokenizer.get_vocab_size()}")
```

**3. Load Model & Resize Embeddings**
Our new tokenizer has 5,000 tokens, but the base BERT expects 30,522. We must resize the embedding matrix to match.

```python
from transformers import BertForTokenClassification

model = BertForTokenClassification.from_pretrained("bert-base-uncased", num_labels=9) # 9 NER tags
model.resize_token_embeddings(5000) # Critical step!
```

**4. The "Label Alignment" Logic (The Hard Part)**
This function maps NER tags to subwords. If a word is split into 3 subwords, the first subword gets the tag, and the next two get `-100` (which PyTorch ignores during loss calculation).

```python
def tokenize_and_align_labels(examples):
    tokenized_inputs = tokenizer(examples["tokens"], truncation=True, is_split_into_words=True)
    labels = []
    for i, label in enumerate(examples["ner_tags"]):
        word_ids = tokenized_inputs.word_ids(batch_index=i)
        previous_word_idx = None
        label_ids = []
        for word_idx in word_ids:
            if word_idx is None:
                label_ids.append(-100) # Ignore special tokens
            elif word_idx != previous_word_idx:
                label_ids.append(label[word_idx]) # First subword gets the tag
            else:
                label_ids.append(-100) # Subword repeats get ignored
            previous_word_idx = word_idx
        labels.append(label_ids)
    tokenized_inputs["labels"] = labels
    return tokenized_inputs
```

**5. Map to Dataset & Train**
We apply this complex function to our NER dataset.

```python
ner_dataset = load_dataset("bigbio/gnormplus") 
tokenized_ner = ner_dataset.map(tokenize_and_align_labels, batched=True)

# Use the Trainer API exactly as in Project 3, but compute_metrics should use seqeval
# (See HF docs for full implementation)
```

---

## Project 5: 🚀 Serving with Gradio + HF Spaces
**Difficulty:** ⭐⭐⭐⭐⭐ (Expert)  
**Core Concept:** Production Deployment, UI, and MLOps  
**Time:** 40 minutes

### 🧠 Why This Project?
A model in a Jupyter notebook is a graveyard. A model with a web UI is a **portfolio piece**.

- **The Skill:** Gradio lets you build a web interface in pure Python—no HTML/JavaScript required. Deploying to Hugging Face Spaces forces you to write a `requirements.txt` and handle environment constraints.
- **The Strategy:** This is the "Finish Line." You take the exact model you fine-tuned in Project 3, give it a user interface, and generate a **public URL** (your-username.hf.space). You can send this to recruiters, stakeholders, or your grandma. It proves you can do **End-to-End ML**, which is the #1 skill companies hire for.

### ✅ Pre-requisites
```bash
pip install gradio transformers torch
```

### 📝 Steps

**1. The Prediction Wrapper**
We load our fine-tuned model from Project 3 and map the ugly `LABEL_0` to human-readable text.

```python
from transformers import pipeline
import gradio as gr

# Load the model you saved in Project 3
classifier = pipeline("text-classification", model="./results/checkpoint-500") 

def predict(text):
    result = classifier(text)[0]
    # Convert HF label to human string
    label = "🚨 DISASTER" if result['label'] == 'LABEL_1' else "✅ SAFE"
    return f"{label} (Confidence: {result['score']:.2f})"
```

**2. Build the Interface**
Gradio is incredibly intuitive. We define inputs, outputs, and add example inputs so users can test instantly.

```python
demo = gr.Interface(
    fn=predict,
    inputs=gr.Textbox(lines=2, placeholder="Enter a tweet or news headline..."),
    outputs=gr.Textbox(label="Prediction Result"),
    title="🆘 Disaster Tweet Detector",
    description="Enter text to check if it refers to a real disaster (e.g., earthquake, fire) or not.",
    examples=[
        ["Firefighters are battling a massive blaze in the city center."],
        ["I just had a fire day at work, finished all my tasks early!"],
        ["Earthquake shakes the northern region, no casualties reported."]
    ]
)

# share=True creates a public link valid for 72 hours
demo.launch(share=True)
```

**3. Deploy to Hugging Face Spaces (The Resume Move)**
1. Go to [huggingface.co/new-space](https://huggingface.co/new-space). Select **Gradio** as the SDK.
2. In your local folder, save the code above as `app.py`.
3. Create a `requirements.txt` file:
   ```text
   transformers
   gradio
   torch
   ```
4. Push to the Space via Git:
   ```bash
   git add .
   git commit -m "Deploy disaster tweet classifier"
   git push
   ```
5. **Boom.** Your app is live forever at `your-username.hf.space`. Add this to your LinkedIn.

---

## 🤝 Contributing

Found a bug or want to add a new project?

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-project`)
3. Commit your changes (`git commit -m 'Add amazing project'`)
4. Push to the branch (`git push origin feature/amazing-project`)
5. Open a Pull Request

All contributions are welcome! 🚀

---

## ⭐ Support This Project

If this workbook helped you, please give it a ⭐ on GitHub!

[![Star History Chart](https://api.star-history.com/svg?repos=YOUR_USERNAME/huggingface-workbook&type=Date)](https://star-history.com/#YOUR_USERNAME/huggingface-workbook&Date)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Congratulations!** You have completed the workbook. You are no longer just a "user" of models; you are a builder who understands the entire lifecycle from loading pre-trained weights to deploying microservices. 🚀