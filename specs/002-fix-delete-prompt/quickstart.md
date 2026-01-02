# Quickstart Guide: Fix Delete Command Prompt in Todo CLI

**Feature**: 002-fix-delete-prompt
**Date**: 2026-01-01

## Overview
This guide provides quick instructions for implementing the fix to the delete command confirmation prompt in the todo console application to satisfy integration test expectations.

## Prerequisites
- Python 3.13+ installed
- Development environment set up for the todo application
- Access to the todo_app source code
- pytest for running tests

## Setup
1. Ensure you have the todo application codebase
2. Install dependencies: `pip install -e .` (or install development dependencies)
3. Verify existing tests pass: `pytest tests/`

## Implementation Steps

### 1. Update the Delete Command in CLI
Location: `todo_app/cli.py`

Modify the `_handle_delete` method to:
- Use `self._service.get_task(task_id)` to retrieve the task (not other methods)
- Display the exact prompt: `"Are you sure you want to delete task '{task.title}'?"`
- Accept only lowercase 'y' as confirmation (case-sensitive)
- On confirmation: delete the task and print `"Task #{task_id} deleted."`
- On cancellation: print `"Task deletion cancelled."`

### 2. Verification
After implementing the changes:

1. Run unit tests: `pytest tests/unit/`
2. Run integration tests: `pytest tests/integration/`
3. Manually test the delete command:
   - Add a task: `add Test Task`
   - Try deleting: `delete 1` (should prompt for confirmation)
   - Confirm with 'y' or cancel with other input

## Key Changes Summary
- **Prompt Text**: "Are you sure you want to delete task '<title>'?"
- **Confirmation**: Only lowercase 'y' confirms deletion
- **Success Message**: "Task #<id> deleted."
- **Cancellation Message**: "Task deletion cancelled."
- **Service Method**: Use `get_task(task_id)` for retrieving task for prompt

## Testing
- All existing unit tests should continue to pass
- Integration tests related to delete functionality should now pass
- Manual testing should confirm the exact behavior matches requirements

## Troubleshooting
- If tests fail, verify the exact prompt text matches requirements
- Ensure only lowercase 'y' is accepted (not 'Y', 'yes', etc.)
- Check that service method usage is correct
- Verify output messages match exactly

## Next Steps
1. Complete implementation of the delete command fix
2. Run full test suite to ensure no regressions
3. Update tasks.md with implementation tasks
4. Proceed to implementation phase