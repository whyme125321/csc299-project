# LLM Conversation — Study & Learning

**Q:**
Teach me how to use JSON files in Python.

**A:**
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

---

**Q:** how do I read and write data to a file?
**A:** you can read and write using Pythons built in file handling methods.
``` Python
with open("notes.txt", "w") as f:
    f.write("This is a note")
```

---

**A:** always use with open(...) so files close automatically.
```Python
with open("notes.txt", "r") as f:
    content = f.read()
print(content)
```

---

**Q:** Whats the best way to make a command line chat interface?
**A:** Start with a basic input loop.
``` Python
while True:
    cmd = input("> ")
    if cmd.lower() == "exit":
        break
    print("You said:", cmd)
```

---

**Q:** How can I structure my Python code into modules?
**A:** Keep your project modular by separating functionality:

main.py → user interface (chat loop)
pkms.py → note management logic
storage.py → JSON read/write functions

```Python
from pkms import add_note, list_notes
```

---


**Q:** What’s the purpose of using JSON instead of text files?
**A:** JSON is structured, human-readable, and easy to parse back into Python objects.
It’s better than plain text when storing multiple notes or tasks.
It also works well with AI and APIs later in your project.



