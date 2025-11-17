# Feature Specification: Command-Line Task Manager

**Feature Branch**: `001-task-manager`  
**Created**: 2025-11-15  
**Status**: Draft  
**Input**: Build a command-line task manager that supports creating tasks, listing tasks, marking tasks complete, deleting tasks, and saving all tasks to a local JSON file. The system should be simple, fast, and easy to use from the terminal. It should follow clean architecture, include automated tests, and be able to run on macOS, Linux, and Windows.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Create and View Tasks (Priority: P1)

A user can quickly create new tasks from the command line and immediately see their task list. This is the core MVP functionality that provides value on its own.

**Why this priority**: Creating and viewing tasks is the fundamental feature—without this, the task manager has no purpose. This story is independent and can be demonstrated immediately.

**Independent Test**: Can be tested by running the CLI to create a task, verify it's stored, list tasks, and confirm the task appears. This delivers the core value of a working task manager.

**Acceptance Scenarios**:

1. **Given** the task manager is running, **When** the user enters `task-manager add "Buy groceries"`, **Then** the task is created with a unique ID and displayed with an uncompleted status.
2. **Given** the task manager has existing tasks, **When** the user enters `task-manager list`, **Then** all tasks are displayed with their IDs, descriptions, and completion status (✓ or ✗).
3. **Given** an empty task list, **When** the user enters `task-manager list`, **Then** a friendly message indicates there are no tasks (rather than blank output).

---

### User Story 2 - Mark Tasks Complete and Delete (Priority: P2)

A user can mark tasks as complete and remove tasks they no longer need. This adds task lifecycle management.

**Why this priority**: Once users can create tasks, they need to complete or remove them. This story builds on P1 and adds practical task management capabilities.

**Independent Test**: Can be tested independently by creating a task from US1, then marking it complete and deleting it. The system remains functional whether or not this story is implemented.

**Acceptance Scenarios**:

1. **Given** a task with ID "1" exists in the list, **When** the user enters `task-manager complete 1`, **Then** the task is marked as complete (indicated by ✓) and persisted.
2. **Given** a task with ID "2" exists and is marked complete, **When** the user enters `task-manager list`, **Then** the completed task is visibly marked differently from incomplete tasks.
3. **Given** a task with ID "3" exists, **When** the user enters `task-manager delete 3`, **Then** the task is removed from the list and no longer appears in subsequent `list` commands.
4. **Given** the user attempts to delete a non-existent task ID, **When** they enter `task-manager delete 999`, **Then** a clear error message indicates the task was not found.

---

### User Story 3 - Data Persistence (Priority: P3)

Tasks are automatically saved to a local JSON file and restored when the task manager starts. This ensures data survives between sessions.

**Why this priority**: After users create and manage tasks, they expect the data to persist. This story completes the core experience but can be tested independently with a simple file system check.

**Independent Test**: Can be tested by creating tasks, closing the application, restarting it, and verifying tasks are restored. This works independently from the complete/delete features.

**Acceptance Scenarios**:

1. **Given** the user has created tasks in a session, **When** they exit the task manager, **Then** all tasks are saved to a local JSON file (location configurable or default to `~/.task-manager/tasks.json`).
2. **Given** the task manager is restarted, **When** it loads, **Then** all previously saved tasks are restored with their IDs, descriptions, and completion status intact.
3. **Given** the tasks JSON file is corrupted or missing, **When** the task manager starts, **Then** it gracefully handles the error with a helpful message and initializes with an empty task list (or offers recovery options).
4. **Given** tasks are on different machines or user accounts, **When** they access different JSON files, **Then** each user's tasks are isolated and independent.

---

### Edge Cases

- What happens when a user provides a task description that is empty or only whitespace? (Should reject with a clear error message)
- What happens when a user attempts to complete or delete a task that doesn't exist? (Should display a specific error indicating the ID was not found)
- What happens when the user's disk is full or write permissions are denied? (Should provide a helpful error message and suggest remediation)
- What happens when a user enters an invalid command or incorrect number of arguments? (Should display usage/help message)
- What happens when the JSON file grows very large (thousands of tasks)? (Should load efficiently without significant delay)
- What happens when the same task manager is run from multiple terminals simultaneously? (File access conflicts should be handled gracefully—either with file locking, atomic writes, or clear error messaging)

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST support creating a new task with a user-provided description via `task-manager add <description>`
- **FR-002**: System MUST assign each task a unique, sequential ID upon creation
- **FR-003**: System MUST list all tasks with their IDs, descriptions, and completion status (completed/incomplete indicator) via `task-manager list`
- **FR-004**: System MUST mark a task as complete via `task-manager complete <task-id>` and display the completed status in subsequent lists
- **FR-005**: System MUST delete a task from the list via `task-manager delete <task-id>` and remove it from subsequent listings
- **FR-006**: System MUST persist all tasks to a local JSON file immediately after any create, complete, or delete operation
- **FR-007**: System MUST load persisted tasks from the JSON file upon startup and restore the complete task list
- **FR-008**: System MUST handle invalid user input gracefully with helpful error messages (e.g., missing arguments, invalid task IDs, malformed commands)
- **FR-009**: System MUST display a help/usage message when the user enters `task-manager help` or uses an invalid command
- **FR-010**: System MUST follow clean architecture principles: separate concerns between CLI interface, business logic (task operations), and data persistence layers

### Key Entities

- **Task**: Represents a single item on the user's to-do list
  - **Attributes**: ID (unique, integer or UUID), description (string, non-empty), isComplete (boolean), createdAt (ISO timestamp), completedAt (optional ISO timestamp)
  - **Relationships**: None (tasks are independent)
  - **Persistence**: Stored in JSON file with the above attributes
  
- **TaskList**: The in-memory collection of all tasks loaded from the JSON file
  - **Attributes**: tasks (array of Task objects), filePath (string, location of JSON file)
  - **Relationships**: Contains zero or more Task objects
  - **Operations**: Add task, remove task, mark complete, save to file, load from file

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can create, list, complete, and delete tasks using simple, intuitive CLI commands (verified by following the acceptance scenarios without additional training)
- **SC-002**: The task manager responds to all user commands in under 500ms on a typical computer (whether on macOS, Linux, or Windows)
- **SC-003**: Tasks persist across application restarts—all previously created tasks are restored when the application relaunches
- **SC-004**: The system handles all edge cases gracefully without crashing (corrupted files, invalid input, permission errors, simultaneous access)
- **SC-005**: All core functionality (create, list, complete, delete, persist, load) has automated test coverage with a minimum of 80% code coverage for the business logic layer
- **SC-006**: The application runs without modification on macOS, Linux, and Windows systems
- **SC-007**: Help and error messages are clear and guide users toward correct usage (e.g., "Invalid task ID: 999. Use 'task-manager list' to see valid IDs")
- **SC-008**: The application follows clean architecture principles with separated concerns: CLI layer, business logic layer, and data persistence layer can be independently tested and replaced

## Assumptions

- **Task IDs**: Tasks will use sequential integer IDs (1, 2, 3, ...) for simplicity and user-friendliness. This assumes the task list size is manageable and IDs do not need to be UUID-like.
- **Storage Location**: The default JSON file location is `~/.task-manager/tasks.json` (standard home directory convention across platforms). Users may configure this via environment variable or config file in future iterations.
- **Concurrency**: The first iteration assumes single-user, single-session usage (tasks are not shared across multiple running instances). Concurrent access handling (file locking, atomic writes) is deferred to a future enhancement.
- **Data Format**: Tasks are stored in a flat JSON array format for simplicity, suitable for up to thousands of tasks. For larger datasets or complex queries, a database might be considered in future iterations.
- **Platform Compatibility**: The implementation will use only standard, cross-platform libraries (no Windows-specific or macOS-specific APIs beyond file system access). This ensures compatibility without modification.
