# Implementation Tasks: Fix Delete Command Prompt in Todo CLI

**Feature**: 002-fix-delete-prompt
**Date**: 2026-01-02
**Spec**: [spec.md](spec.md) | **Plan**: [plan.md](plan.md)

## Implementation Strategy

This feature updates the delete command confirmation prompt in the todo console application to strictly match integration test expectations. The approach focuses on modifying the CLI layer's delete command behavior while maintaining existing architecture and separation of concerns.

## Dependencies

This feature has no dependencies on other user stories since it's a focused bug fix for the delete command confirmation flow.

## Parallel Execution Examples

- Tests and implementation can be developed in parallel with CLI interface design
- Individual components can be updated independently once the core architecture is established

---

## Phase 1: Project Setup

**Goal**: Initialize any required configuration for the delete command fix

- [ ] T001 Review existing CLI implementation in `todo_app/cli.py` to understand current delete command structure
- [ ] T002 [P] Run existing tests to establish baseline: `pytest tests/`
- [ ] T003 [P] Document current delete command behavior for reference

---

## Phase 2: Foundational Components

**Goal**: Prepare the environment and understand the current implementation before making changes

- [ ] T004 Analyze current `_handle_delete` method in `todo_app/cli.py` to identify required changes
- [ ] T005 [P] Verify `TodoService.get_task(task_id)` method exists and functions as expected
- [ ] T006 [P] Identify integration tests that are currently failing due to delete command behavior
- [ ] T007 Review existing error handling patterns in CLI for consistency

---

## Phase 3: Fix Delete Command Confirmation Flow (Priority: P1)

**Goal**: Update the delete command to strictly match integration test expectations for confirmation prompt, logic, and output messages

**Independent Test**: Can be fully tested by running the application, using the delete command, and verifying the exact prompt and confirmation behavior matches requirements.

- [ ] T008 [US1] Update `_handle_delete` method in `todo_app/cli.py` to use `TodoService.get_task(task_id)` for retrieving the task
- [ ] T009 [P] [US1] Modify confirmation prompt to display exact text: "Are you sure you want to delete task '<title>'?"
- [ ] T010 [US1] Implement strict confirmation logic that only accepts lowercase 'y' as confirmation
- [ ] T011 [P] [US1] Update success message to display "Task #<id> deleted." when deletion is confirmed
- [ ] T012 [US1] Update cancellation message to display "Task deletion cancelled." when not confirmed
- [ ] T013 [P] [US1] Handle case where task ID doesn't exist, ensuring proper error flow
- [ ] T014 [US1] Add input validation to ensure only the required confirmation behavior
- [ ] T015 [P] [US1] Test delete command with various inputs ('y', 'Y', 'yes', empty, etc.) to verify behavior
- [ ] T016 [US1] Verify integration tests related to delete functionality now pass

---

## Phase 4: Polish & Cross-Cutting Concerns

**Goal**: Complete the implementation with proper error handling, user experience, and verification

- [ ] T017 Add comprehensive error handling throughout CLI layer for delete edge cases
- [ ] T018 [P] Implement graceful handling of invalid user inputs for delete confirmation
- [ ] T019 Update docstrings in `_handle_delete` method to reflect new behavior
- [ ] T020 [P] Improve error messages with better user feedback for delete operations
- [ ] T021 Add input validation for delete command (valid IDs, etc.)
- [ ] T022 [P] Run full integration test suite to ensure no regressions
- [ ] T023 Add type hints to modified methods if not already present
- [ ] T024 [P] Final verification that all acceptance scenarios from user stories work correctly
- [ ] T025 Run performance verification to ensure <100ms response times for delete operations
- [ ] T026 [P] Final code review and PEP 8 compliance check for modified files