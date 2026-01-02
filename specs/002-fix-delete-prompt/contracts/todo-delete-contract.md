# API Contract: Delete Command in Todo CLI

**Feature**: 002-fix-delete-prompt
**Date**: 2026-01-02

## Overview
This contract defines the interface between the CLI layer and the service layer for the delete command, specifically focusing on the confirmation flow that must match integration test expectations.

## CLI Interface

### TodoCLI Class

#### Methods

##### `_handle_delete(args: str) -> None`
- **Purpose**: Handle the delete command with strict confirmation requirements
- **Parameters**:
  - `args` (str): Arguments for the delete command (task ID)
- **Behavior**:
  - Parse the task ID from args
  - Use `TodoService.get_task(task_id)` to retrieve the task
  - Display exact confirmation prompt: "Are you sure you want to delete task '<title>'?"
  - Accept only lowercase 'y' as confirmation
  - On confirmation: delete task and display "Task #<id> deleted."
  - On cancellation: display "Task deletion cancelled."
- **Dependencies**: TodoService.get_task(task_id), TodoService.delete_task(task_id)

## Service Interface

### TodoService Class

#### Methods

##### `get_task(task_id: int) -> Optional[Task]`
- **Purpose**: Retrieve a specific task by ID for confirmation prompt
- **Parameters**:
  - `task_id` (int): ID of the task to retrieve
- **Returns**: Task or None if task doesn't exist
- **Requirements**: Must be used specifically for the delete confirmation prompt
- **Post-condition**: Returns the requested task or None

##### `delete_task(task_id: int) -> bool`
- **Purpose**: Remove a task from the repository
- **Parameters**:
  - `task_id` (int): ID of the task to delete
- **Returns**: bool - True if task was deleted, False if task doesn't exist
- **Post-condition**: Task is removed from repository if it existed

## Data Contract

### Task Dataclass
```python
@dataclass
class Task:
    id: int
    title: str
    description: str = ""
    completed: bool = False
```

### Validation Rules
- `id`: Positive integer, unique within session
- `title`: 1-200 characters, not empty or whitespace only
- `description`: 0-1000 characters
- `completed`: Boolean value (True/False)

## User Interaction Contract

### Confirmation Flow
1. **Prompt Display**: "Are you sure you want to delete task '<title>'?" (exact text)
2. **Input Acceptance**: Only lowercase 'y' confirms deletion
3. **Success Response**: "Task #<id> deleted." (exact text)
4. **Cancellation Response**: "Task deletion cancelled." (exact text)

### Error Handling Contract
- **Invalid Task ID**: If task doesn't exist, appropriate error handling before confirmation
- **Non-numeric ID**: Proper error message when args don't contain a valid number
- **Service Unavailability**: Graceful degradation if service methods fail

### Expected Error Scenarios
1. **Task Not Found**: When get_task returns None, handle appropriately
2. **Invalid Input**: When args don't contain a valid task ID
3. **Service Error**: If service methods fail, handle gracefully

### Error Response Format
- Methods return boolean success indicators where appropriate
- Validation errors raise ValueError with descriptive messages
- Non-existent operations return False rather than throwing exceptions
- User-facing error messages are clear and actionable