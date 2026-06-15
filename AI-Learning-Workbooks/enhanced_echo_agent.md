# AI Agent Concepts Workbook: Hands-On Project

**Goal**: Build a small, practical project called **"EchoAgent"** — a simple CLI-based AI agent simulator. This workbook will guide you step-by-step to understand **Agents, Codex Code (style), Prompts, Memory, Skills, MCP, and Routines** by implementing them in code.

This is designed for learning with tools like Grok Build, Claude Code, Codex CLI, or even plain Python + LLM APIs.

---

## 🚀 Before You Start: Context & Why This Matters

### What You're Building & Why

AI agents are everywhere: ChatGPT's actions, GitHub Copilot's code generation, autonomous robotics. But **how do they actually work?** Most tutorials show you the finished product. This workbook is different—you'll **build the engine from scratch**.

By implementing EchoAgent, you'll understand:
- How **Prompts** shape agent behavior
- How **Memory** prevents asking for the same info twice
- How **Skills** make agents powerful (instead of just chatty)
- How **MCP** bridges the gap between cloud AI and real tools
- How **Agents** orchestrate everything into intelligent workflows
- How **Routines** automate repetitive sequences

**Real-world connection**: The coffee machine you'll simulate in this project is the exact same pattern Netflix uses to recommend shows, or how Shopify uses agents to answer customer support tickets.

### Recommended Prerequisites
- Basic Python (loops, functions, classes, JSON)
- 4-6 hours across 2-3 coding sessions
- Ideally, complete the **Lazy Chef conceptual workbook first** (45 mins) — the metaphors will make this code click

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

**What You'll Have When Done**: A working CLI where you can run commands like:
```bash
python main.py "Add 5 and 7 using calculator skill"
# Output: Plan: Break down task... Executing calculator skill. Result: 12
```

And then extend it to simulate the Lazy Chef coffee machine scenario.

---

## Setup

1. Create a new directory:
   ```bash
   mkdir echo-agent && cd echo-agent
   git init
   ```

2. Create a Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   ```

3. Install basics:
   ```bash
   pip install rich click pyyaml  # For nice CLI + config
   ```

4. Create `requirements.txt`:
   ```
   rich==13.5.0
   click==8.1.0
   pyyaml==6.0
   ```

5. Create a blank `README.md` and `.gitignore`

---

## Core Concepts & Exercises

### 1. Prompts
**Concept**: Instructions given to the "agent" (you or LLM). Prompts shape everything—behavior, tone, priorities.

**Why It Matters**: A bad prompt makes an agent unpredictable. A good prompt makes it reliably useful. Same underlying code, different prompt = completely different agent.

**Exercise**:
- Create `prompts.py`

```python
# prompts.py
"""
System prompts and user prompt builders.
Think of this as the agent's 'constitution'—everything it does flows from here.
"""

SYSTEM_PROMPT = """
You are EchoAgent, a helpful CLI agent.
Your job is to help the user accomplish their goals step-by-step.
Always think step-by-step before acting.
Use available skills when needed.
Be concise and actionable in responses.
Never repeat the same question twice.
"""

def create_user_prompt(goal: str, context: str = "") -> str:
    """
    Build a user prompt that the agent will reason about.
    Args:
        goal: What the user wants to accomplish
        context: Any additional context (from memory, previous runs)
    """
    prompt = f"Goal: {goal}\n"
    if context:
        prompt += f"Context: {context}\n"
    prompt += "Respond with: 1) Your Plan 2) The Action You'll Take."
    return prompt

# EXPERIMENT: Try these variations
ALT_PROMPT_BUTLER = """
You are EchoAgent, a formal British butler. 
Respond with impeccable diction and deference.
Always refer to the user as "sir" or "madam".
"""

ALT_PROMPT_SARCASTIC = """
You are EchoAgent, a sarcastic tech bro.
Be witty. Make pop culture references.
But still get the job done.
"""

# EXERCISE: How do you think these different prompts would change agent output?
# Hint: The skill execution is the same—only the tone changes.
```

**Task**: 
1. Run experiments: Save output with each prompt above and compare
2. Customize a prompt for YOUR tone preference
3. Answer: How did the prompt change behavior without changing any code?

---

### 2. Memory
**Concept**: Persistent state (short-term conversation + long-term project memory). Without memory, the agent asks "What's your name?" every single time.

**Why It Matters**: Memory is what makes agents feel "smart" vs. annoying. It's the difference between a helpful assistant and a chatbot.

**Exercise**:
- Create `memory.py`

```python
# memory.py
"""
Agent memory system.
- short_term: Current conversation (cleared between sessions)
- long_term: Persistent facts about the user (saved to disk)
"""

import json
from pathlib import Path
from datetime import datetime

class AgentMemory:
    def __init__(self, memory_file="agent_memory.json"):
        self.file = Path(memory_file)
        self.short_term = []  # Current session conversation
        self.long_term = self.load()  # Persistent facts
    
    def load(self):
        """Load long-term memory from disk."""
        if self.file.exists():
            return json.loads(self.file.read_text())
        # Default memory structure (copy this pattern for your own agents)
        return {
            "user_profile": {},
            "facts": [],
            "rules": [],
            "last_updated": None
        }
    
    def save(self):
        """Save long-term memory to disk."""
        self.long_term["last_updated"] = datetime.now().isoformat()
        self.file.write_text(json.dumps(self.long_term, indent=2))
        print(f"💾 Memory saved to {self.file}")
    
    def add_fact(self, fact: str):
        """Learn a new fact about the user."""
        if fact not in self.long_term["facts"]:
            self.long_term["facts"].append(fact)
            self.save()
    
    def add_rule(self, rule: str):
        """Store a behavioral rule."""
        if rule not in self.long_term["rules"]:
            self.long_term["rules"].append(rule)
            self.save()
    
    def get_context(self, recent_only=5):
        """Retrieve recent conversation context for the agent to reference."""
        return "\n".join(self.short_term[-recent_only:])
    
    def record_action(self, action: str):
        """Log what the agent did in this session."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.short_term.append(f"[{timestamp}] {action}")
    
    def show_memory(self):
        """Pretty-print memory state (useful for debugging)."""
        print("\n=== SHORT-TERM MEMORY (This Session) ===")
        for item in self.short_term:
            print(f"  {item}")
        print("\n=== LONG-TERM MEMORY (Persistent) ===")
        print(json.dumps(self.long_term, indent=2))

# EXAMPLE: How the coffee agent would use this
if __name__ == "__main__":
    memory = AgentMemory()
    memory.add_fact("User drinks Decaf coffee")
    memory.add_fact("User lives in Woodbury, MN")
    memory.add_rule("Always brew coffee before 8 AM")
    memory.show_memory()
```

**Task**:
1. Create the memory system
2. Add facts manually for yourself (name, location, preferences)
3. Run the example and see memory persist between runs
4. Answer: What happens if you delete `agent_memory.json` and run again?

---

### 3. Skills
**Concept**: Reusable modular capabilities. Skills are what the agent *does*. Without skills, it's just a chatbot.

**Why It Matters**: Each skill is a "power"—the more skills, the more the agent can do. Skills are how you extend agent capabilities safely (vs. hardcoding everything).

**Exercise**:
Create a `skills/` directory with the architecture:

```
skills/
├── __init__.py
├── base.py
├── calculator.py
├── text_processor.py
└── file_reader.py
```

- Create `skills/base.py` (base class for all skills):

```python
# skills/base.py
"""
Base skill class. All skills inherit from this.
Think of Skill as a "power" the agent can use.
"""

from abc import ABC, abstractmethod

class Skill(ABC):
    """Abstract base class for all agent skills."""
    
    @abstractmethod
    def execute(self, **kwargs):
        """Execute the skill. Subclasses override this."""
        pass
    
    @property
    def name(self):
        """Return the skill's name."""
        return self.__class__.__name__
    
    @property
    def description(self):
        """Return a brief description of what this skill does."""
        return "Base skill"
```

- Create `skills/calculator.py`:

```python
# skills/calculator.py
"""
Calculator skill: Demonstrates math operations.
This is a simple skill—real ones might be much more complex.
"""

from skills.base import Skill

class CalculatorSkill(Skill):
    """Perform math operations."""
    
    @property
    def description(self):
        return "Performs addition, subtraction, multiplication, division"
    
    def execute(self, operation: str, a: float, b: float = None):
        """
        Execute a math operation.
        Args:
            operation: "add", "subtract", "multiply", "divide"
            a: First number
            b: Second number
        Returns:
            The result
        """
        try:
            if operation == "add":
                return a + b
            elif operation == "subtract":
                return a - b
            elif operation == "multiply":
                return a * b
            elif operation == "divide":
                if b == 0:
                    return "Error: Division by zero"
                return a / b
            else:
                return "Unknown operation"
        except Exception as e:
            return f"Skill execution failed: {e}"
```

- Create `skills/text_processor.py`:

```python
# skills/text_processor.py
"""
Text processing skill: Demonstrates string manipulation.
Real agents use this for summarization, extraction, etc.
"""

from skills.base import Skill

class TextProcessorSkill(Skill):
    """Summarize and process text."""
    
    @property
    def description(self):
        return "Summarizes text, extracts keywords, analyzes sentiment"
    
    def execute(self, operation: str, text: str):
        """
        Perform text operations.
        Args:
            operation: "summarize", "extract_keywords", "count_words"
            text: The text to process
        """
        if operation == "summarize":
            # Simple summarization: first sentence + last sentence
            sentences = text.split(".")
            summary = f"{sentences[0]}. {sentences[-1]}"
            return summary
        
        elif operation == "extract_keywords":
            # Simple keyword extraction: words longer than 5 chars
            words = text.split()
            keywords = [w for w in words if len(w) > 5]
            return keywords
        
        elif operation == "count_words":
            return len(text.split())
        
        else:
            return "Unknown operation"
```

- Create `skills/__init__.py`:

```python
# skills/__init__.py
"""Load all skills dynamically."""

from skills.calculator import CalculatorSkill
from skills.text_processor import TextProcessorSkill

def load_skills():
    """Return all available skills."""
    return {
        "calculator": CalculatorSkill(),
        "text_processor": TextProcessorSkill(),
    }
```

**Task**:
1. Build the skill system
2. Create 2 additional skills (e.g., `file_reader.py`, `weather_simulator.py`)
3. Test: Can you list all available skills?
4. Answer: How would you add a "coffee_brewer" skill?

---

### 4. Agents
**Concept**: The orchestrator that reads prompts, uses memory, chooses skills, and acts. The brain.

**Why It Matters**: The Agent is where everything connects. It's the decision-maker.

**Exercise**:
- Create `agent.py`

```python
# agent.py
"""
The Agent: The orchestrator that ties everything together.
This is where Prompts + Memory + Skills + MCP + Routines converge.
"""

from prompts import SYSTEM_PROMPT, create_user_prompt
from memory import AgentMemory
from skills import load_skills

class EchoAgent:
    """
    EchoAgent: A simple agent that demonstrates all 7 core concepts.
    """
    
    def __init__(self, name="EchoAgent"):
        self.name = name
        self.memory = AgentMemory()
        self.skills = load_skills()
        self.conversation_history = []
    
    def run(self, goal: str):
        """
        Execute a goal.
        Steps:
        1. Read the goal
        2. Pull context from memory
        3. Create a plan
        4. Execute skills if needed
        5. Record the result
        """
        print(f"\n🤖 {self.name} is thinking...\n")
        
        # Step 1: Read the goal
        print(f"📌 Goal: {goal}")
        
        # Step 2: Pull context from memory
        context = self.memory.get_context(recent_only=3)
        user_prompt = create_user_prompt(goal, context)
        print(f"📚 Context from memory: {context if context else '(none)'}")
        
        # Step 3: Create a plan (simulate reasoning)
        plan = self._reason_about_goal(goal)
        print(f"🧠 Plan: {plan}\n")
        
        # Step 4: Execute skills if possible
        result = self._execute_skills_for_goal(goal)
        
        # Step 5: Record in memory
        self.memory.record_action(f"Executed goal: {goal} -> {result}")
        self.conversation_history.append({"goal": goal, "result": result})
        
        print(f"✅ Result: {result}\n")
        return result
    
    def _reason_about_goal(self, goal: str) -> str:
        """Simulate the agent thinking through a goal."""
        # In a real agent, this would call an LLM
        # For now, we simulate thinking
        if "add" in goal.lower() or "calculator" in goal.lower():
            return "Use calculator skill"
        elif "summarize" in goal.lower() or "text" in goal.lower():
            return "Use text processor skill"
        else:
            return "Analyze goal and choose appropriate skill"
    
    def _execute_skills_for_goal(self, goal: str) -> str:
        """Execute relevant skills based on the goal."""
        # Try calculator skill
        if "add" in goal.lower():
            try:
                # Parse numbers from goal (very simple)
                numbers = [int(s) for s in goal.split() if s.isdigit()]
                if len(numbers) >= 2:
                    result = self.skills["calculator"].execute("add", numbers[0], numbers[1])
                    return result
            except Exception as e:
                return f"Calculator skill failed: {e}"
        
        # Try text skill
        if "summarize" in goal.lower():
            return self.skills["text_processor"].execute("summarize", goal)
        
        return "No matching skill found for this goal"
    
    def list_skills(self):
        """Show all available skills."""
        print(f"\n📋 {self.name}'s Skills:")
        for skill_name, skill in self.skills.items():
            print(f"  - {skill_name}: {skill.description}")
    
    def show_memory(self):
        """Display the agent's memory."""
        self.memory.show_memory()

# WORKED EXAMPLE: How the full agent loop works
if __name__ == "__main__":
    agent = EchoAgent("CoffeeBot")
    agent.list_skills()
    agent.memory.add_fact("Prefers Decaf coffee")
    
    # Run a goal
    agent.run("Add 5 and 7 using calculator skill")
    
    # Show what the agent remembers
    agent.show_memory()
```

**Task**:
1. Build the agent
2. Run: `agent.run("Add 10 and 20 using calculator skill")`
3. Verify the result is 30
4. Add a new goal type and corresponding skill check
5. Answer: How would you make the agent choose skills automatically (without keyword matching)?

---

### 5. MCP (Model Context Protocol) Simulation
**Concept**: Standardized way for agents to call external tools. Think of it as a plugin system.

**Why It Matters**: MCP is how real agents talk to Slack, GitHub, your smart home, etc. This simulation shows the pattern.

**Exercise**:
- Create `mcp_tools.py`

```python
# mcp_tools.py
"""
MCP Tools: Simulating tool registry for agent integration.
Think of MCP as the 'plugin API' that agents use to talk to the outside world.
"""

import json

TOOLS = {}

def register_tool(name: str, description: str, func):
    """Register a new tool that the agent can call."""
    TOOLS[name] = {
        "description": description,
        "function": func
    }
    print(f"✅ Tool registered: {name}")

def call_tool(tool_name: str, **kwargs):
    """Call a registered tool."""
    if tool_name not in TOOLS:
        return f"❌ Tool '{tool_name}' not found"
    
    try:
        func = TOOLS[tool_name]["function"]
        result = func(**kwargs)
        return result
    except Exception as e:
        return f"❌ Tool execution failed: {e}"

def list_tools():
    """List all available tools."""
    print("\n🔧 Available MCP Tools:")
    for tool_name, tool_info in TOOLS.items():
        print(f"  - {tool_name}: {tool_info['description']}")

# EXAMPLE: Simulated smart home tools
def toggle_smart_plug(plug_id: str, state: str):
    """Simulate toggling a smart plug (the coffee machine!)."""
    if state not in ["ON", "OFF"]:
        return "Error: state must be 'ON' or 'OFF'"
    return f"✅ Smart plug '{plug_id}' turned {state}"

def get_weather(location: str):
    """Simulate fetching weather data."""
    weather_data = {
        "Woodbury, MN": {"temp": 65, "condition": "Sunny"},
        "New York, NY": {"temp": 72, "condition": "Rainy"}
    }
    return weather_data.get(location, "Location not found")

def check_calendar(day: str):
    """Simulate checking a calendar."""
    calendar = {
        "Monday": ["Standup 9:30 AM", "Review meeting 2 PM"],
        "Friday": ["Retro 3 PM", "Happy hour 5 PM"]
    }
    return calendar.get(day, "No events")

# Register the tools
register_tool(
    "toggle_smart_plug",
    "Turn a smart home device ON or OFF",
    toggle_smart_plug
)

register_tool(
    "get_weather",
    "Get weather data for a location",
    get_weather
)

register_tool(
    "check_calendar",
    "Get calendar events for a day",
    check_calendar
)

# WORKED EXAMPLE
if __name__ == "__main__":
    list_tools()
    
    # Call the tools like an agent would
    result1 = call_tool("toggle_smart_plug", plug_id="kitchen_coffee", state="ON")
    print(f"\nResult: {result1}")
    
    result2 = call_tool("get_weather", location="Woodbury, MN")
    print(f"Result: {result2}")
    
    result3 = call_tool("check_calendar", day="Monday")
    print(f"Result: {result3}")
```

**Task**:
1. Create the MCP tool registry
2. Add a new tool (e.g., `send_notification`, `play_music`)
3. Call it from the agent
4. Answer: How is MCP different from just importing a Python library?

---

### 6. Routines
**Concept**: Pre-defined workflows (sequences of actions). Like a shell script for agents.

**Why It Matters**: Routines automate repetitive tasks without agent thinking. They're "fire and forget."

**Exercise**:
- Create `routines.py`

```python
# routines.py
"""
Routines: Pre-defined automation sequences.
Like cron jobs or shell scripts, but for agents.
"""

from agent import EchoAgent
from mcp_tools import call_tool

def morning_coffee_routine(agent: EchoAgent):
    """
    The 'Lazy Chef' morning routine simulation.
    Demonstrates how all 7 components work together.
    """
    print("\n" + "="*50)
    print("🌅 MORNING COFFEE ROUTINE STARTING...")
    print("="*50 + "\n")
    
    # Step 1: Check weather
    print("📍 Step 1: Checking weather in Woodbury, MN...")
    weather = call_tool("get_weather", location="Woodbury, MN")
    print(f"Weather: {weather}")
    
    # Step 2: Check calendar
    print("\n📅 Step 2: Checking today's calendar...")
    events = call_tool("check_calendar", day="Monday")
    print(f"Events: {events}")
    
    # Step 3: Brew coffee
    print("\n☕ Step 3: Brewing your Decaf coffee...")
    result = call_tool("toggle_smart_plug", plug_id="kitchen_coffee", state="ON")
    print(result)
    
    # Step 4: Agent synthesizes and acts
    print("\n🤖 Step 4: Agent synthesizing information...")
    agent.run("You're in Woodbury, it's rainy. Brew Decaf immediately.")
    
    print("\n" + "="*50)
    print("✅ MORNING ROUTINE COMPLETE")
    print("="*50)

def daily_summary_routine(agent: EchoAgent):
    """Daily summary routine: Reflect on what happened."""
    print("\n📊 Running Daily Summary Routine...")
    agent.memory.show_memory()
    print("✅ Summary complete")

# EXERCISE: Create your own routine
def backup_memory_routine(agent: EchoAgent):
    """Example: Back up agent memory at end of day."""
    print("\n💾 Backing up agent memory...")
    agent.memory.save()
    print("✅ Backup complete")

if __name__ == "__main__":
    # Test the routines
    agent = EchoAgent("LazyChef-Alpha")
    morning_coffee_routine(agent)
    daily_summary_routine(agent)
```

**Task**:
1. Create the routine system
2. Run the morning_coffee_routine
3. Create your own routine (e.g., `end_of_day_routine`, `exercise_reminder_routine`)
4. Answer: What's the difference between a Routine and just calling agent.run() manually?

---

### 7. Codex Code Style (Agentic Coding)
**Concept**: How agents write code — structured, with plans, tests, iteration.

**Why It Matters**: When agents generate code (or you write like an agent), you think in steps, test frequently, and iterate. This is the "agentic" approach.

**Exercise**:
Follow this pattern in your own code:

```python
# Template: The Agentic Coding Pattern
"""
PLAN:
1. Define the problem clearly
2. Break into small testable functions
3. Write tests FIRST
4. Implement functions one by one
5. Refactor for clarity
"""

def solve_problem(input_data):
    """
    Step 1: Plan
    - We need to process input_data
    - Expected output: cleaned_result
    
    Step 2: Code (with comments)
    """
    pass

# Step 3: Test
if __name__ == "__main__":
    test_input = "example"
    expected = "expected_output"
    actual = solve_problem(test_input)
    assert actual == expected, f"Expected {expected}, got {actual}"
    print("✅ Test passed")
```

Create `tests/test_agent.py`:

```python
# tests/test_agent.py
"""
Test suite for EchoAgent.
Good agents are tested agents.
"""

from agent import EchoAgent
from memory import AgentMemory
from skills import load_skills

def test_agent_initialization():
    """Test that agent initializes correctly."""
    agent = EchoAgent("TestBot")
    assert agent.name == "TestBot"
    assert agent.skills is not None
    print("✅ test_agent_initialization passed")

def test_memory_persistence():
    """Test that memory persists across sessions."""
    mem = AgentMemory("test_memory.json")
    mem.add_fact("Test fact")
    assert "Test fact" in mem.long_term["facts"]
    print("✅ test_memory_persistence passed")

def test_calculator_skill():
    """Test the calculator skill."""
    skills = load_skills()
    result = skills["calculator"].execute("add", 5, 3)
    assert result == 8, f"Expected 8, got {result}"
    print("✅ test_calculator_skill passed")

if __name__ == "__main__":
    test_agent_initialization()
    test_memory_persistence()
    test_calculator_skill()
    print("\n🎉 All tests passed!")
```

**Task**:
1. Run the test suite
2. Write 2 additional tests
3. Make all tests pass
4. Answer: Why is testing important for agents?

---

## Final Project Structure

After completing all exercises, your project should look like:

```
echo-agent/
├── agent.py                 # The orchestrator
├── memory.py               # Persistent state
├── prompts.py              # System + user prompts
├── mcp_tools.py            # External tool registry
├── routines.py             # Automated workflows
├── skills/
│   ├── __init__.py
│   ├── base.py            # Base class
│   ├── calculator.py      # Math skill
│   ├── text_processor.py  # Text skill
│   └── (your custom skills)
├── tests/
│   └── test_agent.py      # Test suite
├── main.py                # Entry point
├── agent_memory.json      # Persistent memory (auto-created)
├── requirements.txt       # Dependencies
├── .gitignore            # Git exclusions
├── README.md             # Project docs
└── venv/                 # Virtual environment
```

---

## main.py (Entry Point)

```python
# main.py
"""
Main entry point for EchoAgent CLI.
This is how users interact with the agent.
"""

import click
from agent import EchoAgent
from routines import morning_coffee_routine, daily_summary_routine
from mcp_tools import list_tools

@click.group()
def cli():
    """EchoAgent CLI - Your agentic learning tool."""
    pass

@cli.command()
@click.argument("goal")
def run(goal):
    """Run a goal through the agent."""
    agent = EchoAgent("EchoAgent")
    agent.run(goal)

@cli.command()
def skills():
    """List all available skills."""
    agent = EchoAgent("EchoAgent")
    agent.list_skills()

@cli.command()
def tools():
    """List all available MCP tools."""
    list_tools()

@cli.command()
def morning():
    """Run the morning coffee routine."""
    agent = EchoAgent("LazyChef-Alpha")
    morning_coffee_routine(agent)

@cli.command()
def summary():
    """Run the daily summary routine."""
    agent = EchoAgent("EchoAgent")
    daily_summary_routine(agent)

@cli.command()
def memory():
    """Show the agent's memory."""
    agent = EchoAgent("EchoAgent")
    agent.show_memory()

if __name__ == "__main__":
    cli()
```

Run with:
```bash
python main.py run "Add 5 and 7"
python main.py skills
python main.py tools
python main.py morning
python main.py memory
```

---

## Running & Extending

### Phase 1: Build the Foundation (2-3 hours)
1. Implement all modules (Agent, Memory, Prompts, Skills, MCP, Routines)
2. Run the test suite and verify everything works
3. Test each component in isolation

### Phase 2: Extend with Real Features (2-3 hours)
4. Add 3-5 new skills of your own
5. Create 2-3 new routines
6. Enhance memory to track more data
7. Add error handling and logging

### Phase 3: Connect to Real Systems (Optional, advanced)
8. Replace the simulated MCP tools with real ones (GitHub API, Slack, etc.)
9. Integrate a real LLM API (Anthropic, OpenAI) for actual reasoning
10. Build a web interface on top of the CLI
11. Deploy as a microservice

**Advanced Ideas**:
- Multi-agent collaboration (two agents working on the same goal)
- Auto-loading skills from `SKILL.md` files
- Learning from experience (agent improves over time)
- Hierarchical goals (big goal -> sub-goals -> skills)

---

## Reflection

Once you've built EchoAgent, answer these in your notebook or create a `REFLECTION.md` file:

1. **Prompts**: How did changing the system prompt affect behavior? What tone did you choose for your custom agent?

2. **Memory**: Why is memory crucial? What would break if memory didn't persist?

3. **Skills**: How do skills make agents more powerful? How would you add a skill for the agent you're building?

4. **MCP**: What real-world APIs would you connect via MCP? (GitHub, Stripe, your company's backend?)

5. **Agents**: How does the agent orchestrate everything? Is it just a decision tree, or something more?

6. **Routines**: How do routines save time vs. running tasks manually?

7. **Code Style**: How did the "agentic coding" approach (plan first, test early, iterate) feel different?

8. **Integration**: How does EchoAgent relate to the Lazy Chef project you read about? Can you sketch how to implement Lazy Chef in code?

---

## 🎯 Capstone: Build the Lazy Chef in Code

Once you've mastered all 7 components, implement the Lazy Chef coffee automator:

```python
def lazy_chef_morning_sequence():
    """
    The full "Lazy Chef" scenario in code.
    Uses: Prompt + Memory + Skills + MCP + Agent + Routine
    """
    agent = EchoAgent("LazyChef-Alpha")
    
    # Load user preferences from memory
    preferences = agent.memory.long_term.get("preferences", {})
    
    # MCP: Check weather and calendar
    weather = call_tool("get_weather", location=preferences["location"])
    calendar = call_tool("check_calendar", day="Monday")
    
    # Skills: Analyze and decide
    agent.run(f"User prefers {preferences['coffee']['type']} coffee. Weather is {weather}. Schedule is {calendar}")
    
    # MCP: Brew the coffee
    call_tool("toggle_smart_plug", plug_id="kitchen_coffee", state="ON")
    
    # Memory: Learn from this
    agent.memory.add_fact(f"On rainy days, user prefers to stay indoors")
    
    print("☕ Your coffee is ready!")

if __name__ == "__main__":
    lazy_chef_morning_sequence()
```

---

**Congratulations!** You've built a foundation for understanding modern AI agents. You now understand the seven core pieces and how they work together.

Share your repo, extend it further, and use these patterns in your own projects!

---

*Workbook enhanced with reflection and learning recommendations*  
*Original created with ❤️ by Grok*  
*Date: June 2026*
