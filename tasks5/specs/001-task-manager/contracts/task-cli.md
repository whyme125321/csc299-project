# CLI Command Contract: task-manager

**Date**: 2025-11-15  
**Purpose**: Define the command-line interface specification and behavior contracts for the task manager CLI

---

## Application Entry Point

```bash
task-manager [COMMAND] [OPTIONS] [ARGUMENTS]
```

---

## Commands

### 1. ADD - Create a New Task

**Signature**:
```bash
task-manager add <description>
```

**Arguments**:
- `description` (required): Task description string
  - Must be non-empty, non-whitespace-only
  - Max 500 characters
  - Supports spaces and special characters
  - Quoted strings are preserved

**Examples**:
```bash
task-manager add "Buy groceries"
task-manager add "Write README documentation"
task-manager add "Review pull requests"
```

**Expected Output** (Success):
```
✓ Task created
  ID: 1
  Description: Buy groceries
```

**Expected Output** (Error - empty description):
```
✗ Error: Task description cannot be empty
  Usage: task-manager add "<description>"
```

**Exit Code**:
- Success: 0
- Failure: 1

**Behavior**:
1. Validate description is non-empty and non-whitespace
2. Generate unique sequential ID
3. Create task with creation timestamp
4. Add to in-memory task list
5. Persist to JSON file immediately
6. Return new task ID and description to user

**Persistence**: Tasks are immediately saved to `~/.task-manager/tasks.json` after creation

---

### 2. LIST - Display All Tasks

**Signature**:
```bash
task-manager list
```

**Arguments**: None

**Examples**:
```bash
task-manager list
```

**Expected Output** (Success - Tasks exist):
```
Your Tasks:
  1  ✓  Buy groceries
  2     Write report
  3  ✓  Review code
```

**Expected Output** (Success - No tasks):
```
Your task list is empty. Use 'task-manager add "<task>"' to create one.
```

**Expected Output** (Error - file corrupted):
```
✗ Error: Cannot load tasks (file corrupted)
  Suggestion: Check ~/.task-manager/tasks.json or delete it to start fresh
```

**Exit Code**:
- Success: 0
- Failure (corruption): 1
- Success (no tasks): 0

**Format Details**:
- Column 1: Task ID (right-aligned, 3 characters)
- Column 2: Status indicator (✓ for complete, blank for incomplete)
- Column 3: Task description (truncated if > 70 chars, suffix with "...")
- Completed tasks marked with ✓ prefix
- Incomplete tasks have empty space

**Behavior**:
1. Load tasks from JSON file (if not already loaded)
2. Display each task with ID, completion status, and description
3. Show friendly message if no tasks exist
4. Handle file corruption gracefully
5. Sort by creation order (insertion order)

---

### 3. COMPLETE - Mark a Task as Finished

**Signature**:
```bash
task-manager complete <task-id>
```

**Arguments**:
- `task-id` (required): Integer ID of task to complete
  - Must be positive integer
  - Must exist in current task list
  - Must not already be marked complete

**Examples**:
```bash
task-manager complete 1
task-manager complete 2
```

**Expected Output** (Success):
```
✓ Task marked complete
  ID: 1
  Description: Buy groceries
```

**Expected Output** (Error - task not found):
```
✗ Error: Task not found (ID: 999)
  Available task IDs: 1, 2, 3
  Use 'task-manager list' to see all tasks
```

**Expected Output** (Error - invalid ID format):
```
✗ Error: Invalid task ID '1a'
  Please provide a valid integer ID
```

**Expected Output** (Error - task already complete):
```
✗ Error: Task 1 is already marked complete
```

**Exit Code**:
- Success: 0
- Failure: 1

**Behavior**:
1. Validate task-id is valid integer
2. Find task with matching ID
3. If not found: show error with available IDs
4. If found and already complete: show message (warning, not error)
5. Mark task complete with current timestamp
6. Persist to JSON file immediately
7. Confirm completion to user

---

### 4. DELETE - Remove a Task

**Signature**:
```bash
task-manager delete <task-id>
```

**Arguments**:
- `task-id` (required): Integer ID of task to delete
  - Must be positive integer
  - Must exist in current task list

**Examples**:
```bash
task-manager delete 1
task-manager delete 3
```

**Expected Output** (Success):
```
✓ Task deleted
  ID: 1
  Description: Buy groceries
```

**Expected Output** (Error - task not found):
```
✗ Error: Task not found (ID: 999)
  Available task IDs: 2, 3, 5
  Use 'task-manager list' to see all tasks
```

**Expected Output** (Error - invalid ID format):
```
✗ Error: Invalid task ID 'abc'
  Please provide a valid integer ID
```

**Exit Code**:
- Success: 0
- Failure: 1

**Behavior**:
1. Validate task-id is valid integer
2. Find task with matching ID
3. If not found: show error with list of available IDs
4. If found: remove from task list
5. Do NOT renumber remaining tasks (IDs remain stable)
6. Persist to JSON file immediately
7. Confirm deletion to user

**Important**: Task IDs of remaining tasks are NOT affected by deletion (gap may exist)

---

### 5. HELP - Display Usage Information

**Signature**:
```bash
task-manager help
task-manager --help
task-manager -h
```

**Arguments**: None

**Expected Output**:
```
Usage: task-manager [COMMAND] [OPTIONS]

Commands:
  add <description>    Create a new task
  list                 Show all tasks
  complete <id>        Mark a task as complete
  delete <id>          Remove a task
  help                 Show this help message

Examples:
  task-manager add "Buy groceries"
  task-manager list
  task-manager complete 1
  task-manager delete 1

For more information, visit: https://github.com/yourname/task-manager
```

**Exit Code**: 0

**Behavior**: Display help text and exit successfully

---

## Global Options

### Configuration via Environment Variables

- `TASKMANAGER_HOME`: Override default task data directory (default: `~/.task-manager`)
  ```bash
  export TASKMANAGER_HOME=/custom/path
  task-manager list  # Uses /custom/path/tasks.json
  ```

- `TASKMANAGER_DEBUG`: Enable debug logging (future feature)
  ```bash
  export TASKMANAGER_DEBUG=1
  task-manager list
  ```

---

## Error Handling

### Standard Error Behavior

All error messages follow this format:
```
✗ Error: [Specific error description]
  [Context or suggestion for recovery]
  Usage: [Show correct command usage]
```

### Common Errors & Handling

| Scenario | Exit Code | User Message |
|----------|-----------|--------------|
| Invalid command | 1 | "Unknown command: {cmd}. Use 'task-manager help' for available commands." |
| Missing required argument | 1 | "Missing required argument: {arg}. Usage: {command}" |
| Invalid integer ID | 1 | "Invalid task ID '{id}'. Please provide a valid integer." |
| Task not found | 1 | "Task not found (ID: {id}). Available IDs: {list}. Use 'task-manager list' to see all." |
| Empty description | 1 | "Task description cannot be empty. Usage: task-manager add \"<description>\"" |
| Permission denied | 1 | "Permission denied: Cannot write to {path}. Check file permissions." |
| Disk full | 1 | "Disk full: Cannot save tasks. Free up disk space and try again." |
| Corrupted JSON | 1 | "Cannot load tasks (file corrupted). Check {path} or delete to start fresh." |

---

## Success Indicators

- **✓ symbol**: Indicates successful command completion
- **✗ symbol**: Indicates error or failure
- **Exit code 0**: Command completed successfully
- **Exit code 1**: Command failed

---

## Output Formatting

### Consistency Rules

1. **Messages**: Start with ✓ (success) or ✗ (error)
2. **Indentation**: Details indented with 2 spaces
3. **Line breaks**: Blank line between message and next prompt
4. **Color** (optional future feature): Green for success, Red for errors
5. **Unicode**: Use ✓ and ✗ symbols (supported on Windows 10+, macOS, Linux)

### Example Conversation

```bash
$ task-manager add "Buy milk"
✓ Task created
  ID: 1
  Description: Buy milk

$ task-manager add "Pay rent"
✓ Task created
  ID: 2
  Description: Pay rent

$ task-manager list
Your Tasks:
  1     Buy milk
  2     Pay rent

$ task-manager complete 1
✓ Task marked complete
  ID: 1
  Description: Buy milk

$ task-manager list
Your Tasks:
  1  ✓  Buy milk
  2     Pay rent

$ task-manager delete 1
✓ Task deleted
  ID: 1
  Description: Buy milk

$ task-manager list
Your Tasks:
  2     Pay rent
```

---

## Testing Contract

### CLI Tests Should Verify

1. **Command parsing**: All valid command formats are recognized
2. **Argument validation**: Invalid arguments are rejected with helpful errors
3. **Output format**: Messages follow the standard format (✓/✗, indentation)
4. **Exit codes**: Correct codes for success/failure
5. **Persistence**: Commands that modify state persist to file
6. **Isolation**: Commands don't interfere with each other
7. **Error messages**: Contain context and recovery suggestions

### Compliance Criteria

- All exit codes match specification
- Error messages are clear and actionable
- Help text is displayed for all command usage errors
- Task data persists correctly across commands
- No partial state changes (atomicity)

