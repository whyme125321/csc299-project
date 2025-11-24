# Final System – CSC 299 Project

This project is the final deliverable for CSC-299 and demonstrates a complete command-line software system developed with the assistance of AI-coding tools. The system includes:

- **Personal Task Manager**
- **Personal Knowledge Management System (PKMS)**
- **Terminal-based Chat Interface**
- **AI Agent** capable of summarizing tasks and notes using the OpenAI API

All components run through a single CLI entrypoint, are written in Python, and store their state using JSON files for full portability across Windows, macOS, and Linux.

---

## Features Overview

### **1. Task Manager**
Manage daily tasks directly from the terminal:

- Add tasks  
- List tasks  
- Mark tasks as done  
- Delete tasks  
- Persistent JSON storage  

### **2. Personal Knowledge Management System (PKMS)**
Store and organize personal notes:

- Add notes (title + content)  
- List all notes  
- View individual notes  
- Delete notes  
- Persistent JSON storage  

### **3. Chat Interface**
A simple terminal chat:

- Type freely  
- View tasks using `/tasks`  
- View PKMS notes using `/notes`  
- Exit chat using `/exit`  

### **4. AI Agent (OpenAI)**
Uses the OpenAI API (GPT-5-mini) to:

- Summarize all PKMS notes  
- Summarize the task list  

### **5. Grab API key and put into bash**
```bash
export OPENAI_API_KEY="your-key-here"
```


## 🚀 Installation & Setup

### **1. Enter the project directory**
```bash
cd final_system
```

### **2. Install the project in editable mode**
```bash
uv pip install -e .
```

---

## 🧭 Running the Program

### **Show all commands**
```bash
uv run final_system --help
```

---

## 🗂 Task Manager Commands
```bash
uv run final_system tasks add "do homework"
uv run final_system tasks list
uv run final_system tasks done 0
uv run final_system tasks delete 0
```

---

## 📝 PKMS Commands
```bash
uv run final_system pkms add "lecture1" "notes about the lecture"
uv run final_system pkms list
uv run final_system pkms view 0
uv run final_system pkms delete 0
```

---

## 💬 Chat Interface
```bash
uv run final_system chat start
```

Inside chat:

- `/tasks` → show tasks  
- `/notes` → show notes  
- `/exit` → quit  

---

## 🤖 AI Agent Commands
```bash
uv run final_system agent summarize-notes
uv run final_system agent summarize-tasks
```
