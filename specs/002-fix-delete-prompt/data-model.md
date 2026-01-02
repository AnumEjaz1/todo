# Data Model: Fix Delete Command Prompt in Todo CLI

**Feature**: 002-fix-delete-prompt
**Date**: 2026-01-02

## Task Entity
The existing Task entity is used by the delete command for the confirmation prompt.

### Attributes
- **id** (int): Unique identifier for the task, auto-incremented
  - Type: Positive integer
  - Generated automatically when task is created
  - Required: Yes
- **title** (str): Brief description of the task
  - Type: String
  - Maximum length: 200 characters
  - Required: Yes
  - Validation: Cannot be empty or whitespace only
- **description** (str): Detailed description of the task
  - Type: String
  - Maximum length: 1000 characters
  - Required: No (can be empty)
  - Default: Empty string
- **completed** (bool): Completion status of the task
  - Type: Boolean
  - Values: True (completed) or False (pending)
  - Default: False

### State Transitions
- **Initial State**: `completed = False` when task is created
- **Completed State**: `completed = True` when user marks task as complete
- **Reopened State**: `completed = False` when user unmarks task as complete
- **Deletion State**: Task is removed from the collection

### Validation Rules
1. Title must not be empty or contain only whitespace
2. Title must be 200 characters or less
3. Description must be 1000 characters or less
4. ID must be unique within the application session
5. ID must be a positive integer

## Task List Collection
The existing Task List Collection is affected by the delete operation.

### Structure
- **Type**: Python list containing Task objects
- **Operations**: Add, remove, update, retrieve by ID
- **Ordering**: Tasks maintain insertion order with auto-incremented IDs
- **Session Scope**: Exists only during application runtime

### Constraints
1. Tasks are stored only in memory during the session
2. No persistence across application restarts (Phase I requirement)
3. Task IDs are sequential and auto-incremented
4. Maximum recommended size: 1000 tasks (practical limit for console display)

### Deletion Impact
- When a task is deleted, it is removed from the collection
- The collection size decreases by 1
- Other tasks remain in the collection unchanged

## User Input Entity
The user input for confirmation is a simple string that determines the outcome.

### Attributes
- **value** (str): The user's input for confirmation
  - Type: String
  - Expected values: 'y' (for confirmation), any other value (for cancellation)
  - Required: Yes
  - Case-sensitive: Yes (only 'y', not 'Y' or 'yes')

### Validation Rules
1. Input must be exactly 'y' (lowercase) to confirm deletion
2. Any other input cancels the deletion
3. Empty input cancels the deletion
4. Multi-character input (like 'yes') cancels the deletion

## Relationships
- **Task List**: Contains multiple Task entities
- **Task**: Independent entity with no direct relationships to other tasks
- **User Input**: Determines the action taken on a specific Task
- **User Session**: Task list exists within the context of a single application session