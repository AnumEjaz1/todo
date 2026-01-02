# Todo API Contract: Todo In-Memory Python Console App

**Feature**: 001-todo-console-app
**Date**: 2026-01-01

## Overview
This contract defines the interface between the CLI layer and the service layer for the in-memory todo application.

## Service Interface

### TodoService Class

#### Methods

##### `add_task(title: str, description: str = "") -> int`
- **Purpose**: Add a new task to the repository
- **Parameters**:
  - `title` (str): Title of the task (required, 1-200 characters)
  - `description` (str): Description of the task (optional, 0-1000 characters)
- **Returns**: int - The ID of the newly created task
- **Exceptions**:
  - `ValueError` if title is empty or exceeds length limits
- **Post-condition**: Task is added to the in-memory repository with completed=False

##### `get_all_tasks() -> List[Task]`
- **Purpose**: Retrieve all tasks from the repository
- **Parameters**: None
- **Returns**: List[Task] - All tasks in the repository
- **Exceptions**: None
- **Post-condition**: Returns complete list of tasks in insertion order

##### `get_task(task_id: int) -> Optional[Task]`
- **Purpose**: Retrieve a specific task by ID
- **Parameters**:
  - `task_id` (int): ID of the task to retrieve
- **Returns**: Task or None if task doesn't exist
- **Exceptions**: None
- **Post-condition**: Returns the requested task or None

##### `update_task(task_id: int, title: str = None, description: str = None) -> bool`
- **Purpose**: Update an existing task's properties
- **Parameters**:
  - `task_id` (int): ID of the task to update
  - `title` (str): New title (optional)
  - `description` (str): New description (optional)
- **Returns**: bool - True if task was updated, False if task doesn't exist
- **Exceptions**:
  - `ValueError` if title is provided but is empty or exceeds length limits
- **Post-condition**: Task properties are updated if task exists

##### `delete_task(task_id: int) -> bool`
- **Purpose**: Remove a task from the repository
- **Parameters**:
  - `task_id` (int): ID of the task to delete
- **Returns**: bool - True if task was deleted, False if task doesn't exist
- **Exceptions**: None
- **Post-condition**: Task is removed from repository if it existed

##### `mark_task_complete(task_id: int, completed: bool = True) -> bool`
- **Purpose**: Update the completion status of a task
- **Parameters**:
  - `task_id` (int): ID of the task to update
  - `completed` (bool): Completion status (default True)
- **Returns**: bool - True if task status was updated, False if task doesn't exist
- **Exceptions**: None
- **Post-condition**: Task's completed status is updated if task exists

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

## Error Handling Contract

### Expected Error Scenarios
1. **Invalid Task ID**: Methods that take a task_id return False when the ID doesn't exist
2. **Invalid Input**: Methods validate input and raise ValueError for invalid data
3. **Repository Issues**: Repository methods handle any internal errors and propagate appropriately

### Error Response Format
- Methods return boolean success indicators where appropriate
- Validation errors raise ValueError with descriptive messages
- Non-existent operations return False rather than throwing exceptions