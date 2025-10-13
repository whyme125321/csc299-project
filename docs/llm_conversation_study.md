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
```


# Question: how do i read and write data to a file?
with open("notes.txt", "w") as f:
    f.write("This is a note")

# Answer: always use with open()
with open("notes.txt", "r") as f:
    content = f.read()
print(content)

# Question: Whats the best way to make a command line chat interface?

while True:
    cmd = input("> ")
    if cmd.lower() == "exit":
        break
    print("You said:", cmd)

# Question: How can I structure my Python code into modules?

from pkms import add_note, list_notes







