# Research: Fix Delete Command Prompt in Todo CLI

## Overview
This research document analyzes the current delete command implementation and identifies the specific changes needed to satisfy integration test expectations.

## Current Implementation Analysis

### Current Delete Command in cli.py
The current delete command implementation in `todo_app/cli.py` likely has the following behavior:
- Prompts user for confirmation before deleting
- Uses `input()` to get confirmation
- May have case-insensitive confirmation logic
- May use different prompt text than required
- May use different success/cancellation messages

### Required Changes
Based on the functional requirements:

1. **Exact Confirmation Prompt**: Must display exactly "Are you sure you want to delete task '<title>'?"
2. **Strict Confirmation Logic**: Only accept lowercase 'y' as confirmation
3. **Success Message**: Display "Task #<id> deleted." when confirmed
4. **Cancellation Message**: Display "Task deletion cancelled." when not confirmed
5. **Service Method Usage**: Use `TodoService.get_task(task_id)` to get the task for the prompt

## Implementation Strategy

### Decision: Update _handle_delete method in cli.py
**Rationale**: The delete command logic is contained in the `_handle_delete` method in `todo_app/cli.py`. This method needs to be updated to match the exact requirements.

**Alternatives considered**:
- A. Create a new method for delete confirmation - Rejected because it would duplicate functionality unnecessarily
- B. Update at the service layer - Rejected because the requirements specify not to change service code
- C. Update in the main loop - Rejected because it would mix command routing with business logic

### Decision: Use strict string comparison for confirmation
**Rationale**: The requirement is to accept only lowercase 'y', so we'll use exact string comparison `confirmation == 'y'`.

**Alternatives considered**:
- A. Case-insensitive comparison - Rejected because requirements specify only lowercase 'y' works
- B. Multiple confirmation options (y/yes/Yes) - Rejected because requirements specify only 'y'

### Decision: Use TodoService.get_task(task_id) for prompt
**Rationale**: Requirement FR-005 specifically states to use `TodoService.get_task(task_id)` to retrieve the task for the confirmation prompt.

**Alternatives considered**:
- A. Use repository directly - Rejected because requirements specify to use TodoService method
- B. Use different service method - Rejected because requirements specify this exact method

## Technical Implementation Details

### Current Method Signature
The `_handle_delete` method likely has the signature:
```python
def _handle_delete(self, args: str) -> None
```

### Expected Updated Implementation
1. Parse the task ID from args
2. Use `self._service.get_task(task_id)` to get the task (not other methods)
3. Display exact prompt: `f"Are you sure you want to delete task '{task.title}'?"`
4. Get confirmation input
5. Check if confirmation is exactly 'y' (case-sensitive)
6. If confirmed: delete task and show "Task #<id> deleted."
7. If not confirmed: show "Task deletion cancelled."

### Error Handling
- Handle invalid task ID (when get_task returns None)
- Handle non-numeric task ID in args
- Maintain existing error handling patterns

## Test Validation Strategy

The changes will be validated by running:
- `pytest tests/unit/` - to ensure unit tests still pass
- `pytest tests/integration/` - to ensure integration tests now pass
- Manual testing to verify the exact prompt and behavior

## Dependencies and Risks

### Dependencies
- TodoService.get_task(task_id) method must exist and work correctly
- TodoService.delete_task(task_id) method must exist and work correctly
- Task model must have a title attribute

### Risks
- Changing confirmation logic might affect user experience
- Exact prompt text must match integration tests exactly
- Need to ensure other CLI functionality is not affected