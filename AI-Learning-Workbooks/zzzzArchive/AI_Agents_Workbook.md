# AI Agent Concepts Workbook: Hands-On Project

**Goal**: Build a small, practical project called **"EchoAgent"** — a simple CLI-based AI agent simulator. This workbook will guide you step-by-step to understand **Agents, Codex Code (style), Prompts, Memory, Skills, MCP, and Routines** by implementing them in code.

This is designed for learning with tools like Grok Build, Claude Code, Codex CLI, or even plain Python + LLM APIs.

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [Setup](#setup)
3. [Core Concepts & Exercises](#core-concepts--exercises)
4. [Final Project Structure](#final-project-structure)
5. [Running & Extending](#running--extending)
6. [Reflection](#reflection)

---

## Project Overview

**EchoAgent** is a lightweight Python CLI tool that simulates an AI agent. It can:
- Take user goals (prompts)
- Use "skills" (modular functions)
- Maintain memory (JSON + files)
- Execute simple routines
- Demonstrate MCP-style tool calling

By building it, you'll see how real agentic systems work under the hood.

**Tech Stack**: Python 3.10+, simple libraries (no heavy deps).

---

## Setup

1. Create a new directory:
   ```bash
   mkdir echo-agent && cd echo-agent
   git init
   ```

2. Create files (we'll do this step-by-step below).

3. Install basics:
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install rich click pyyaml  # For nice CLI + config
   ```

4. Create `requirements.txt` and `README.md`.

---

## Core Concepts & Exercises

### 1. Prompts
**Concept**: Instructions given to the "agent" (you or LLM).

**Exercise**:
- Create `prompts.py`

```python
# prompts.py
SYSTEM_PROMPT = """
You are EchoAgent, a helpful CLI agent.
Always think step-by-step before acting.
Use available skills when needed.
"""

def create_user_prompt(goal: str, context: str = "") -> str:
    return f"Goal: {goal}\nContext: {context}\nRespond with Plan + Action."
```

**Task**: Run experiments by changing the system prompt and observe behavior changes.

---

### 2. Memory
**Concept**: Persistent state (short-term conversation + long-term project memory).

**Exercise**:
- Create `memory.py`

```python
# memory.py
import json
from pathlib import Path

class AgentMemory:
    def __init__(self, memory_file="agent_memory.json"):
        self.file = Path(memory_file)
        self.short_term = []  # Current session
        self.long_term = self.load()
    
    def load(self):
        if self.file.exists():
            return json.loads(self.file.read_text())
        return {"rules": [], "facts": []}
    
    def save(self):
        self.file.write_text(json.dumps(self.long_term, indent=2))
    
    def add_fact(self, fact: str):
        self.long_term["facts"].append(fact)
        self.save()
    
    def get_context(self):
        return "\n".join(self.short_term[-5:])  # Last 5 messages
```

**Task**: Add rules like "always be concise" to long-term memory.

---

### 3. Skills
**Concept**: Reusable modular capabilities (like the bundled skills in agents).

**Exercise**:
- Create `skills/` directory and `skills/base.py`

```python
# skills/base.py
from abc import ABC, abstractmethod

class Skill(ABC):
    @abstractmethod
    def execute(self, **kwargs):
        pass

    @property
    def name(self):
        return self.__class__.__name__
```

Create example skills:
- `skills/calculator.py`
- `skills/file_reader.py`

Example:

```python
# skills/calculator.py
from skills.base import Skill

class CalculatorSkill(Skill):
    def execute(self, operation: str, a: float, b: float = None):
        if operation == "add":
            return a + b
        # Add more...
        return "Unknown operation"
```

**Task**: Create 2-3 skills. Make the agent discover them dynamically.

---

### 4. Agents
**Concept**: The brain that plans, uses tools, acts, reflects.

**Exercise**:
- Create `agent.py`

```python
# agent.py
from prompts import SYSTEM_PROMPT, create_user_prompt
from memory import AgentMemory
from skills import load_skills  # We'll create this

class EchoAgent:
    def __init__(self):
        self.memory = AgentMemory()
        self.skills = load_skills()
    
    def run(self, goal: str):
        prompt = create_user_prompt(goal, self.memory.get_context())
        print("System:", SYSTEM_PROMPT)
        print("User Prompt:", prompt)
        
        # Simulate thinking
        plan = f"Plan: Break down {goal}"
        print(plan)
        
        # Execute skills if needed
        result = self.execute_skills(goal)
        self.memory.short_term.append(f"Goal: {goal} -> {result}")
        return result
```

**Task**: Implement the planning loop with reflection.

---

### 5. MCP (Model Context Protocol) Simulation
**Concept**: Standardized way for agents to call external tools.

**Exercise**:
- Create `mcp_tools.py` simulating tool registry.

```python
# mcp_tools.py
TOOLS = {}

def register_tool(name, func):
    TOOLS[name] = func

def call_tool(tool_name, **kwargs):
    if tool_name in TOOLS:
        return TOOLS[tool_name](**kwargs)
    return "Tool not found"

# Example
register_tool("calculator", lambda a, b: a + b)
```

Integrate into agent.

---

### 6. Routines
**Concept**: Pre-defined workflows (sequences of actions).

**Exercise**:
- Create `routines.py`

```python
# routines.py
from agent import EchoAgent

def daily_summary_routine(agent: EchoAgent):
    print("Running Daily Summary Routine...")
    agent.run("Summarize today's facts from memory")
    # Chain more tasks
```

**Task**: Create routines like "code review", "backup memory", etc.

---

### 7. Codex Code Style (Agentic Coding)
**Concept**: How agents write code — structured, with plans, tests, iteration.

**Exercise**:
Follow this pattern in your own coding:
1. Plan
2. Write code
3. Test
4. Reflect & improve

Add tests using `pytest`.

---

## Final Project Structure

After completing exercises, your project should look like:

```
echo-agent/
├── agent.py
├── memory.py
├── prompts.py
├── mcp_tools.py
├── routines.py
├── skills/
│   ├── __init__.py
│   ├── base.py
│   ├── calculator.py
│   └── file_reader.py
├── main.py
├── agent_memory.json
├── tests/
│   └── test_agent.py
├── README.md
└── requirements.txt
```

---

## main.py (Entry Point)

```python
# main.py
import click
from agent import EchoAgent
from routines import daily_summary_routine

@click.command()
@click.argument("goal")
def cli(goal):
    agent = EchoAgent()
    result = agent.run(goal)
    print("Result:", result)

if __name__ == "__main__":
    cli()
```

Run with: `python main.py "Add 5 and 7 using calculator skill"`

---

## Running & Extending

1. Implement all modules.
2. Run the CLI.
3. Extend with real LLM calls (use Grok API or OpenAI).
4. Add persistence, more skills, and complex routines.
5. Turn it into a full agent by integrating with actual MCP servers.

**Next Level Ideas**:
- Connect to real MCP (e.g., GitHub tool).
- Make skills auto-load from `SKILL.md` files.
- Add multi-agent collaboration.

---

## Reflection

Answer these in your notebook or `REFLECTION.md`:

1. How did **prompts** affect agent behavior?
2. Why is **memory** crucial for consistency?
3. How do **skills** make agents more powerful?
4. What real-world tools resemble **MCP**?
5. How do **routines** reduce manual work?
6. What did building this teach you about **Agents** and **Codex-style** coding?

---

**Congratulations!** You've built a foundation for understanding modern AI agents.

Share your repo or ask Grok/Claude/Codex to help extend it!

---
*Workbook created with ❤️ by Grok*  
*Date: June 2026*