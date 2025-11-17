# Data Model: Command-Line Task Manager

**Date**: 2025-11-15  
**Purpose**: Define domain entities, their relationships, validation rules, and state transitions

---

## Entity: Task

Represents a single item on a user's task list.

### Fields

| Field | Type | Required | Default | Notes |
|-------|------|----------|---------|-------|
| `id` | Integer | Yes | Auto-increment | Unique identifier, sequence starts at 1, stable across save/load |
| `description` | String | Yes | N/A | User-provided task name/description, non-empty, max 500 chars |
| `is_complete` | Boolean | Yes | False | Indicates task completion status |
| `created_at` | ISO 8601 Timestamp | Yes | Current time | When task was created (UTC timezone) |
| `completed_at` | ISO 8601 Timestamp | Optional | Null | When task was marked complete; null if incomplete (UTC timezone) |

### Validation Rules

- **id**: Must be positive integer, unique across all tasks, immutable after creation
- **description**: Non-empty string, no leading/trailing whitespace, max 500 UTF-8 characters
- **is_complete**: Boolean value; derived field based on `completed_at` presence (if `completed_at` is not null, `is_complete` must be true)
- **created_at**: Valid ISO 8601 timestamp in UTC (e.g., `2025-11-15T14:30:45Z`)
- **completed_at**: Valid ISO 8601 timestamp in UTC, or null; if present, must be >= `created_at`

### State Transitions

```
Initial State (after creation):
  id=N, description="...", is_complete=false, created_at=NOW, completed_at=null

Transition 1: Mark Complete
  is_complete → true, completed_at → NOW

Transition 2: Delete
  Task removed from task list
  
Note: One-way completion in MVP (no "mark incomplete" feature)
```

### Relationships

- **Task → TaskList**: Many-to-one relationship (many tasks belong to one task list)
- **Task → Task**: No relationships with other tasks (independent entities)

### Example JSON Representation

```json
{
  "id": 1,
  "description": "Buy groceries",
  "is_complete": false,
  "created_at": "2025-11-15T10:30:00Z",
  "completed_at": null
}
```

---

## Entity: TaskList

Represents the collection of all tasks for a user.

### Fields

| Field | Type | Required | Default | Notes |
|-------|------|----------|---------|-------|
| `tasks` | Array[Task] | Yes | Empty array | Collection of Task objects; maintained in order of creation |
| `storage_path` | String | Yes | `~/.task-manager/tasks.json` | File system path where tasks are persisted |
| `next_id` | Integer | Yes | 1 | Next available ID for new task creation; derived from max(task.id) + 1 |

### Validation Rules

- **tasks**: Array of valid Task objects; must maintain consistency (no duplicate IDs, IDs are sequential without gaps)
- **storage_path**: Valid file system path; directory must exist or be creatable
- **next_id**: Must be max(task.id) + 1; used to ensure unique IDs on task creation

### Operations

#### CreateTask(description: String) → Task

Creates and adds a new task to the list.

```
Input: description (non-empty string)
Process:
  1. Validate description (non-empty, non-whitespace)
  2. Assign id = next_id
  3. Set is_complete = false
  4. Set created_at = current UTC time
  5. Set completed_at = null
  6. Add task to tasks array
  7. Increment next_id
  8. Return new Task object
Output: Newly created Task
Exceptions: 
  - InvalidDescriptionError if description is invalid
  - TaskListFullError if maximum task count reached (deferred, not in MVP)
```

#### GetAllTasks() → Array[Task]

Retrieves all tasks in creation order.

```
Input: None
Output: Array of all Task objects (including completed tasks)
Exceptions: None
```

#### MarkComplete(task_id: Integer) → Task

Marks a task as complete.

```
Input: task_id (integer)
Process:
  1. Find task with matching id
  2. If found: set is_complete = true, set completed_at = current UTC time
  3. If not found: raise TaskNotFoundError
Output: Updated Task object
Exceptions:
  - TaskNotFoundError if task_id doesn't exist
  - InvalidStateError if task already complete (optional, per spec)
```

#### DeleteTask(task_id: Integer) → void

Removes a task from the list.

```
Input: task_id (integer)
Process:
  1. Find task with matching id
  2. If found: remove from tasks array
  3. If not found: raise TaskNotFoundError
Output: None
Exceptions:
  - TaskNotFoundError if task_id doesn't exist
  
Note: IDs of remaining tasks are NOT renumbered (stable IDs)
```

#### SaveToFile() → void

Persists all tasks to JSON file.

```
Input: None
Process:
  1. Serialize tasks array to JSON format with version header
  2. Write to storage_path (atomic write: temp file → rename)
  3. Create directory if needed (mkdir -p)
Output: None
Exceptions:
  - FileWriteError if permission denied or disk full
  - DirectoryCreationError if parent directory cannot be created
  - SerializationError if JSON encoding fails (shouldn't happen with valid data)
```

#### LoadFromFile() → void

Loads tasks from JSON file, replacing current list.

```
Input: None
Process:
  1. Check if storage_path exists
  2. If not exists: initialize as empty task list, return
  3. If exists: read and parse JSON
  4. Validate version field (v1.0 expected)
  5. Parse tasks array, validate each Task object
  6. Recalculate next_id = max(task.id) + 1
  7. Replace current tasks with loaded tasks
Output: None
Exceptions:
  - FileNotFoundError if storage_path points to invalid location (warning, not error)
  - JsonParseError if file is corrupted
  - ValidationError if task objects don't match schema
  - VersionMismatchError if version field indicates incompatible format (future)
```

### Relationships

- **TaskList → Task**: One-to-many relationship (one task list contains many tasks)
- **TaskList → Storage**: Depends on storage adapter for persistence

### Invariants (Must Always Hold True)

1. **ID Uniqueness**: No two tasks have the same ID
2. **ID Sequentiality**: Task IDs form a sequence (1, 2, 3, ..., N) with no gaps
3. **ID Immutability**: Once a task is created, its ID never changes
4. **Timestamp Ordering**: `completed_at` ≥ `created_at` for all tasks
5. **Completion Consistency**: If `is_complete` == true, then `completed_at` is not null; if `is_complete` == false, then `completed_at` is null
6. **Persistence Consistency**: Tasks in memory match persisted file after save; reloaded tasks match saved state

### Example JSON Representation

```json
{
  "version": "1.0",
  "tasks": [
    {
      "id": 1,
      "description": "Buy groceries",
      "is_complete": false,
      "created_at": "2025-11-15T10:30:00Z",
      "completed_at": null
    },
    {
      "id": 2,
      "description": "Write report",
      "is_complete": true,
      "created_at": "2025-11-14T14:00:00Z",
      "completed_at": "2025-11-15T09:00:00Z"
    },
    {
      "id": 3,
      "description": "Review code",
      "is_complete": false,
      "created_at": "2025-11-15T11:00:00Z",
      "completed_at": null
    }
  ]
}
```

---

## Relationships & Dependencies

```
┌─────────────────────────────────────────┐
│          TaskList (In Memory)           │
│  - tasks: Array[Task]                   │
│  - storage_path: String                 │
│  - next_id: Integer                     │
└─────────────────────────────────────────┘
          │
          │ contains
          ▼
┌─────────────────────────────────────────┐
│           Task (Domain Model)           │
│  - id: Integer (unique, sequential)     │
│  - description: String                  │
│  - is_complete: Boolean                 │
│  - created_at: ISO Timestamp            │
│  - completed_at: ISO Timestamp (opt)    │
└─────────────────────────────────────────┘
          │
          │ persists to
          ▼
┌─────────────────────────────────────────┐
│    JSON File on Disk                    │
│    ~/.task-manager/tasks.json           │
└─────────────────────────────────────────┘
```

---

## Error Handling

### Exception Hierarchy

```
TaskManagerError (Base Exception)
├── InvalidDescriptionError (validation failure)
├── TaskNotFoundError (operation on non-existent task)
├── FileWriteError (persistence failure)
├── FileReadError (loading failure)
├── CorruptedDataError (data validation on load)
└── ConfigurationError (invalid storage path, environment variables)
```

---

## Design Notes

### Why These Fields?

- **id**: Unique identification for operations (complete, delete); sequential for user-friendliness
- **description**: Core user data; max length prevents abuse
- **is_complete**: Enables filtering/sorting completed vs. active tasks
- **created_at / completed_at**: Audit trail; enables time-based queries (future features)

### Why No Other Fields?

- **Priority / Category**: Deferred to v2.0 (scope creep)
- **Due Date**: Out of scope for MVP
- **Notes / Subtasks**: Out of scope for MVP
- **Tags / Labels**: Out of scope for MVP

### Concurrency & Versioning

- **Current**: Single-user assumption; no locking mechanism
- **Future v2.0**: File locking or database backend for concurrent access
- **Schema Versioning**: `version` field in JSON enables migrations without breaking changes

---

## Testing Implications

### Unit Tests (models.py)

- Task object creation with valid/invalid descriptions
- Task state transitions (incomplete → complete)
- Validation of timestamp ordering
- ID immutability

### Integration Tests (persistence)

- TaskList save/load round-trip preserves all data
- IDs remain stable across save/load cycles
- Corrupted JSON handling
- Missing directory auto-creation

### Contract Tests (CLI)

- `task-manager add "Task description"` returns new task ID
- `task-manager list` displays all tasks with correct format
- `task-manager complete <id>` marks task complete
- `task-manager delete <id>` removes task

