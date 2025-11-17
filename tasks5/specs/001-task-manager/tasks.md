# Tasks: Command-Line Task Manager

**Input**: Design documents from `/specs/001-task-manager/`  
**Prerequisites**: plan.md (✓ complete), spec.md (✓ complete), research.md (✓ complete), data-model.md (✓ complete), contracts/ (✓ complete), quickstart.md (✓ complete)

**Tests**: Full test coverage required (TDD mandatory per constitution). Test tasks included per user story.

**Organization**: Tasks grouped by user story to enable independent implementation and testing of each story.

## Format: `- [ ] [ID] [P?] [Story?] Description with file path`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- **File paths**: Exact locations for all code changes
- **Test-first**: Tests written and failing before implementation

---

## Phase 1: Setup & Project Initialization

**Purpose**: Project structure and configuration

- [ ] T001 Create project root structure (src/, tests/, config/, docs/)
- [ ] T002 Create src/\_\_init\_\_.py and package structure for src/cli/, src/core/, src/storage/, src/utils/
- [ ] T003 [P] Create tests/\_\_init\_\_.py and test subdirectories (tests/unit/, tests/integration/, tests/contract/)
- [ ] T004 [P] Create setup.py with package metadata, dependencies (Click, Pydantic), extras_require for dev
- [ ] T005 [P] Create requirements.txt with runtime dependencies (click, pydantic, colorama)
- [ ] T006 [P] Create requirements-dev.txt with dev dependencies (pytest, pytest-cov, pytest-mock, flake8, mypy)
- [ ] T007 [P] Create config/.flake8 with linting rules and exclusions
- [ ] T008 [P] Create pytest.ini with test discovery and coverage configuration
- [ ] T009 [P] Create .github/workflows/test.yml for CI/CD (run tests, linting, type checks on push)
- [ ] T010 [P] Create VERSION file with initial version 1.0.0-alpha.1
- [ ] T011 Create src/utils/config.py to manage TASKMANAGER_HOME environment variable and file paths
- [ ] T012 Create src/core/exceptions.py with exception hierarchy (TaskManagerError, InvalidDescriptionError, TaskNotFoundError, FileWriteError, etc.)
- [ ] T013 Create docs/README.md with project overview, installation, quick start, examples
- [ ] T014 Create docs/ARCHITECTURE.md explaining clean architecture layers and design decisions

**Checkpoint**: Project structure ready, all dependencies installed, CI/CD pipeline configured

---

## Phase 2: Foundational Layer (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Domain Models (Required by all stories)

- [ ] T015 [P] Create src/core/models.py with Task class (id, description, is_complete, created_at, completed_at)
- [ ] T016 [P] Add Task validation in models.py (non-empty description, timestamp validation, immutable id)
- [ ] T017 [P] Create TaskList class in src/core/models.py (tasks array, storage_path, next_id)
- [ ] T018 Create src/core/service.py with TaskService class initialization (takes storage adapter as dependency)

### Storage Adapter Pattern (Required by all stories)

- [ ] T019 [P] Create src/storage/adapter.py with AbstractStorageAdapter interface (save, load methods)
- [ ] T020 [P] Create src/storage/errors.py with storage-specific exceptions (FileWriteError, FileReadError, CorruptedDataError, ConfigurationError)
- [ ] T021 Create src/storage/json_adapter.py implementing JsonStorageAdapter
- [ ] T022 Implement JsonStorageAdapter.load() method: read JSON, parse, validate, handle missing file gracefully
- [ ] T023 Implement JsonStorageAdapter.save() method: atomic write (temp file → rename), create directory if needed
- [ ] T024 Add JSON schema with version field in JsonStorageAdapter for future migration support

### CLI Entry Point (Required by all stories)

- [ ] T025 Create src/cli/\_\_init\_\_.py module initialization
- [ ] T026 Create src/cli/main.py with Click command group setup and error handler
- [ ] T027 Implement setup.py entry_point to expose task-manager CLI command

**Checkpoint**: Foundation ready - core models, storage layer, and CLI entry point working; user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Create and View Tasks (Priority: P1) �� MVP

**Goal**: Users can create tasks and see their complete task list. This is the core MVP.

**Independent Test**: Verified by: `task-manager add "Test" && task-manager list` shows task with ID and description

### Unit Tests for US1

- [ ] T028 [P] [US1] Create tests/unit/test_models.py with Task creation and validation tests
- [ ] T029 [P] [US1] Add Task field validation tests in tests/unit/test_models.py (empty description rejection, timestamp validation)
- [ ] T030 [P] [US1] Create tests/unit/test_service.py with TaskService.create_task() tests (valid input, returns Task with id, persists via adapter)
- [ ] T031 [P] [US1] Add TaskService.get_all_tasks() tests in tests/unit/test_service.py
- [ ] T032 [P] [US1] Create tests/unit/test_json_adapter.py with JSON serialization/deserialization tests
- [ ] T033 [P] [US1] Create tests/contract/test_cli_interface.py with CliRunner tests for add command (valid description, empty description rejection, output format)
- [ ] T034 [P] [US1] Add CliRunner contract tests for list command in tests/contract/test_cli_interface.py (empty list, populated list, format validation)
- [ ] T035 [US1] Create tests/integration/test_e2e_workflow.py for end-to-end: add task → list → verify persistence

### Implementation for US1

- [ ] T036 [P] [US1] Implement TaskService.create_task(description: str) → Task in src/core/service.py (validate, generate id, set timestamps, add to list, save)
- [ ] T037 [P] [US1] Implement TaskService.get_all_tasks() → List[Task] in src/core/service.py
- [ ] T038 [US1] Implement TaskService initialization to load tasks from storage on instantiation in src/core/service.py
- [ ] T039 [US1] Implement Click add command in src/cli/main.py: task-manager add "<description>" → calls service.create_task() → displays result with ID
- [ ] T040 [US1] Implement Click list command in src/cli/main.py: task-manager list → calls service.get_all_tasks() → formats and displays with IDs, descriptions, ✓/✗ status
- [ ] T041 [US1] Add help message for add/list commands in src/cli/main.py with usage examples
- [ ] T042 [US1] Implement error handling in add command: reject empty/whitespace descriptions with helpful message
- [ ] T043 [US1] Implement error handling in list command: show "task list is empty" message when no tasks exist

### Integration for US1

- [ ] T044 [US1] Test data persistence: create task → verify saved to ~/.task-manager/tasks.json → verify format matches schema
- [ ] T045 [US1] Test directory auto-creation: if ~/.task-manager doesn't exist, system creates it on first add command
- [ ] T046 [US1] Manual test workflow: add 3 tasks → list → verify all appear with IDs → exit → restart → list → verify all tasks restored

**Checkpoint**: At this point, User Story 1 (MVP) should be fully functional, testable independently, and deployable.

---

## Phase 4: User Story 2 - Mark Complete & Delete (Priority: P2)

**Goal**: Users can manage task lifecycle (mark complete, delete).

**Independent Test**: Verified by: create task → mark complete → verify ✓ in list → delete → verify removed

### Unit Tests for US2

- [ ] T047 [P] [US2] Add Task.mark_complete() transition tests in tests/unit/test_models.py (sets is_complete=true, sets completed_at)
- [ ] T048 [P] [US2] Create tests/unit/test_service.py with TaskService.mark_complete(id) tests (valid id, invalid id rejection, already complete handling)
- [ ] T049 [P] [US2] Add TaskService.delete_task(id) tests in tests/unit/test_service.py (valid id, invalid id rejection, ID stability after deletion)
- [ ] T050 [P] [US2] Add CliRunner contract tests for complete command in tests/contract/test_cli_interface.py (valid id, invalid id error, output format)
- [ ] T051 [P] [US2] Add CliRunner contract tests for delete command in tests/contract/test_cli_interface.py (valid id, invalid id error, confirmation)
- [ ] T052 [US2] Add error handling tests for non-existent task IDs (show available IDs in error message)

### Implementation for US2

- [ ] T053 [P] [US2] Implement TaskService.mark_complete(task_id: int) → Task in src/core/service.py (find task, set is_complete=true, set completed_at, save, return)
- [ ] T054 [P] [US2] Implement TaskService.delete_task(task_id: int) → void in src/core/service.py (find task, remove from list, save, maintain ID stability)
- [ ] T055 [US2] Implement Click complete command in src/cli/main.py: task-manager complete <id> → calls service.mark_complete() → displays confirmation
- [ ] T056 [US2] Implement Click delete command in src/cli/main.py: task-manager delete <id> → calls service.delete_task() → displays confirmation
- [ ] T057 [US2] Add error handling for complete command: show "Task not found" with available IDs when id is invalid
- [ ] T058 [US2] Add error handling for delete command: show "Task not found" with available IDs when id is invalid
- [ ] T059 [US2] Implement invalid ID format detection (non-integer input) with helpful error message

### Integration for US2

- [ ] T060 [US2] Test complete workflow: create task → mark complete → verify ✓ in list → verify persisted to file with completed_at timestamp
- [ ] T061 [US2] Test delete workflow: create task → delete → verify removed from list and from file → verify ID not reused (gap in IDs is OK)
- [ ] T062 [US2] Test error scenarios: attempt to complete non-existent ID → error message shows available IDs
- [ ] T063 [US2] Test persistence across restart: mark complete → delete some tasks → exit → restart → verify final state matches

**Checkpoint**: User Stories 1 AND 2 should both work independently and together; users have complete task lifecycle management

---

## Phase 5: User Story 3 - Data Persistence (Priority: P3)

**Goal**: Tasks survive application restarts via JSON file storage with error resilience.

**Independent Test**: Verified by: create tasks → stop app → restart app → verify all tasks restored with correct state

### Unit Tests for US3

- [ ] T064 [P] [US3] Add JSON round-trip tests in tests/unit/test_json_adapter.py (save → load → verify data intact, IDs stable)
- [ ] T065 [P] [US3] Add corrupted JSON handling tests in tests/unit/test_json_adapter.py (malformed JSON → graceful error)
- [ ] T066 [P] [US3] Add missing file handling tests in tests/unit/test_json_adapter.py (no file exists → initialize empty list)
- [ ] T067 [P] [US3] Add permission denied tests in tests/unit/test_json_adapter.py (mocked write failure → FileWriteError)
- [ ] T068 [P] [US3] Add disk full scenario tests in tests/unit/test_json_adapter.py (simulate ENOSPC → helpful error)

### Implementation for US3

- [ ] T069 [US3] Ensure all TaskService operations (create, complete, delete) call storage.save() immediately in src/core/service.py
- [ ] T070 [US3] Implement atomic write in JsonStorageAdapter (write to temp file, rename atomically) in src/storage/json_adapter.py
- [ ] T071 [US3] Implement TaskList state recovery on load in src/core/service.py: recalculate next_id from max task id
- [ ] T072 [US3] Add error handling for corrupted JSON file: catch JSON parse errors, provide user-friendly message, suggest recovery
- [ ] T073 [US3] Add error handling for permission errors: catch permission denied on write, provide helpful message suggesting disk check
- [ ] T074 [US3] Implement directory creation if not exists in JsonStorageAdapter (mkdir -p behavior) in src/storage/json_adapter.py
- [ ] T075 [US3] Add version field to JSON schema and handle v1.0 files in src/storage/json_adapter.py (future-proof for v2.0 migrations)
- [ ] T076 [US3] Test environment variable override: set TASKMANAGER_HOME to custom path, verify tasks stored at custom location

### Integration for US3

- [ ] T077 [US3] Create tests/integration/test_persistence.py: save tasks → load from file → verify exact match (including timestamps, IDs, completion status)
- [ ] T078 [US3] Test corrupted file recovery: manually corrupt tasks.json → start app → verify graceful error and option to recover
- [ ] T079 [US3] Test missing file: delete ~/.task-manager/tasks.json → start app → add task → verify file created automatically
- [ ] T080 [US3] Test large dataset: create 1000 tasks → save/load → measure time (should be <500ms per spec SC-002)
- [ ] T081 [US3] Test isolation: create user A tasks, switch TASKMANAGER_HOME to user B, verify user B has empty list (no cross-user data leak)

**Checkpoint**: All user stories complete and independently tested; full feature ready for cross-story integration

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements and cross-story validation

- [ ] T082 [P] Add comprehensive docstrings to all public methods in src/core/models.py, src/core/service.py, src/cli/main.py
- [ ] T083 [P] Create docs/DEVELOPMENT.md with developer guide (setup, TDD workflow, running tests, architecture)
- [ ] T084 [P] Add type hints to all functions in src/core/*.py, src/storage/*.py, src/utils/*.py
- [ ] T085 [P] Run mypy type checker and fix all type errors: mypy src/
- [ ] T086 [P] Run flake8 linter and fix style issues: flake8 src/ tests/
- [ ] T087 Generate coverage report and ensure ≥80% coverage: pytest --cov=src --cov-report=html
- [ ] T088 Create docs/API.md with CLI command reference (all commands, arguments, examples, exit codes)
- [ ] T089 Add --help flag support to all commands and implement help command in src/cli/main.py
- [ ] T090 Verify help messages follow format: descriptive title + usage example + available commands
- [ ] T091 [P] Run full test suite and ensure all tests pass: pytest -v
- [ ] T092 Run CI/CD pipeline verification: ensure .github/workflows/test.yml passes locally
- [ ] T093 Verify cross-platform compatibility: test on macOS with pathlib, test on simulated Windows paths
- [ ] T094 Create CHANGELOG.md documenting v1.0.0-alpha.1 features
- [ ] T095 Run quickstart guide validation: follow docs/quickstart.md steps, verify all steps work correctly
- [ ] T096 Manual end-to-end test: create 5 tasks → mark 2 complete → delete 1 → verify list → verify persistence → restart → verify final state

**Checkpoint**: All features complete, tested, documented, and ready for release

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - **BLOCKS all user stories**
- **User Stories (Phases 3-5)**: All depend on Foundational phase completion
  - User stories CAN RUN IN PARALLEL (different code files, no cross-dependencies)
  - Recommended: Complete in priority order (US1 → US2 → US3) for MVP validation
- **Polish (Phase 6)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories - MVP validator
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Independent of US1 implementation (but tests may use US1 tasks)
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Independent of US1/US2 (but benefits from pre-populated tasks for testing)

### Within Each User Story

1. Unit tests written first (Red phase TDD)
2. Implementation code written (Green phase)
3. Contract/integration tests written
4. Manual testing to verify acceptance scenarios

### Parallel Opportunities Within Phase 1

- All [P] marked tasks can run in parallel (T002-T010, T013-T014 don't block each other)
- Configuration files independent
- Test infrastructure independent

### Parallel Opportunities Within Phase 2

- All [P] marked model tasks can run in parallel (T015-T017, T019-T020)
- Models and storage adapter can be developed simultaneously
- CLI entry point independent of models

### Parallel Opportunities Within Each User Story

All [P] marked test tasks can be written in parallel:
- Unit tests for models
- Unit tests for service
- Unit tests for storage
- Contract tests for CLI

**Implementation** follows after tests are written and failing.

---

## Implementation Strategy

### MVP First (User Story 1 Only - Recommended)

1. ✅ Complete Phase 1: Setup
2. ✅ Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. ✅ Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: User Story 1 works independently
5. **Deploy/Demo**: Show working MVP (add + list tasks)
6. Proceed to Phase 4: User Story 2
7. Proceed to Phase 5: User Story 3
8. Complete Phase 6: Polish

**Timeline**: ~3-5 days with 1 developer

### Incremental Delivery (Recommended)

1. Phase 1 + 2 together: Foundation ready (~1 day)
2. Deploy User Story 1: Add and list tasks working (~1 day)
3. User Story 2: Complete and delete working (~1 day)
4. User Story 3: Persistence validated (~1 day)
5. Polish + Release: Documentation, coverage, quality (~1 day)

**Each story adds value without breaking previous stories**

### Parallel Team Strategy (If Multiple Developers)

With 2 developers:
1. Both complete Phase 1 + 2 together (foundation)
2. Developer A: User Story 1 (add/list)
3. Developer B: User Story 3 (persistence - can develop in parallel)
4. Then collaborate on User Story 2 (complete/delete - integrates both)
5. Both: Phase 6 (Polish, merge, validate)

With 3 developers:
1. All: Phase 1 + 2 (foundation)
2. Developer A: User Story 1 (add/list)
3. Developer B: User Story 2 (complete/delete)
4. Developer C: User Story 3 (persistence)
5. All: Phase 6 (Polish, integrate, release)

---

## Task Checklist Compliance

✅ All tasks follow strict format: `- [ ] [ID] [P?] [Story?] Description with file path`
✅ 96 total tasks organized into 6 phases
✅ Tests included (TDD: write tests first, then implementation)
✅ Parallel opportunities marked with [P]
✅ User story mapping: [US1], [US2], [US3] for story-specific tasks
✅ File paths specified for each code change
✅ Independent test criteria defined per user story
✅ Dependencies clearly documented
✅ Execution order logical (Setup → Foundational → Stories → Polish)

---

## Task Summary

| Phase | Name | Task Count | Status |
|-------|------|-----------|--------|
| 1 | Setup | 14 tasks | Ready |
| 2 | Foundational | 10 tasks | Ready |
| 3 | US1: Create & View | 19 tasks | Ready (MVP) |
| 4 | US2: Complete & Delete | 17 tasks | Ready |
| 5 | US3: Persistence | 18 tasks | Ready |
| 6 | Polish & QA | 15 tasks | Ready |
| **TOTAL** | **All Phases** | **96 tasks** | **Ready for Implementation** |

---

## Notes

- Each [P] task = independent file, can run in parallel
- [Story] labels map tasks to specific user stories for traceability
- Each user story independently completable and testable
- TDD workflow: tests fail → implement → tests pass → refactor
- Stop at any checkpoint to validate story independently
- Commit after each phase completion
- Follow constitution principles: TDD mandatory, clean code, simple architecture

