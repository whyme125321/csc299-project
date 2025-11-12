# Tasks4 – OpenAI Chat Completions API Experiment  
### CSC 299 — AI Coding Assistants Project

## Overview
Tasks4 is a **standalone experiment** demonstrating your ability to use the **OpenAI Chat Completions API** within a Python program.  
Unlike previous tasks, Tasks4 does **not** use the PKMS or task manager code from Tasks1–Tasks3.  

The goal is simple:  
You provide multiple paragraph-length task descriptions, and your program sends each one to **ChatGPT-5-mini** to generate **short, concise summaries**.

This task prepares you for later milestones where AI agents will interact with your PKMS and task database.

---

## Features

### **1. Uses the OpenAI Chat Completions API**
Your code connects to the API and sends task descriptions as input.

### **2. Summarizes Multiple Paragraphs**
The program processes each description **independently** inside a loop.

### **3. Outputs Short Summaries**
Each long task description is transformed into a short, clear phrase.

### **4. Simple, Standalone Structure**
Does not use:
- Tasks1 JSON  
- Tasks2 code structure  
- Tasks3 package or pytest  

This module is intentionally lightweight.

---

## How It Works

1. The program defines two (or more) **paragraph-length descriptions** inside a list.
2. A loop iterates over each description.
3. Each description is sent to **ChatGPT-5-mini** using the Chat Completions API.
4. The model returns a **short summary phrase**.
5. The program prints each summary clearly.

Example:

Long description →  
“Design and implement a multi-agent PKMS system…”

Short summary →  
“Build PKMS multi-agent architecture”

---

## Example Code Behavior (Conceptual)

```
Description 1 → summarized
Description 2 → summarized
...
```

You should see multiple short summaries printed one after another.

---

## How to Run

Go into the tasks4 directory:

```bash
cd tasks4
```

Then run the module using uv:

```bash
uv run tasks4
```

This will execute the `tasks4.py` script and print the AI-generated summaries.

---

## Why This Matters

Tasks4 introduces the **first real use of AI** in your CSC-299 project:

- You learn how to call the **OpenAI API**.
- You practice looping through multiple independent queries.
- The output style mirrors how AI agents will later interact with:
  - Your PKMS  
  - Your task manager  
  - Future terminal-based chat interface  

This milestone is the foundation for real AI-assistant functionality in your final project.

---



