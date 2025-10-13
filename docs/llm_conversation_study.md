# LLM Conversation — Study & Learning

### Question:
Teach me how to use JSON files in Python.

### Answer:
Python includes a built-in `json` library that makes it easy to read and write structured data.

Example:
```python
import json

data = {"notes": [{"title": "Idea", "content": "Test note"}]}

# Save JSON
with open("data/notes.json", "w") as f:
    json.dump(data, f, indent=4)

# Load JSON
with open("data/notes.json", "r") as f:
    loaded = json.load(f)

print(loaded)



