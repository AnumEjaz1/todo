# Feature Specification: Fix Delete Command Prompt in Todo CLI

## Overview
This feature addresses integration test failures by updating the delete command confirmation prompt in the todo console application to strictly match expected behavior. The delete command currently does not follow the exact prompt format and confirmation logic required by integration tests.

## User Scenarios & Testing

### Primary User Flow
1. User runs the todo application and adds a task
2. User executes the delete command with a task ID (e.g., `delete 1`)
3. Application displays exact confirmation prompt: "Are you sure you want to delete task '<title>'?"
4. User enters 'y' to confirm deletion or any other input to cancel
5. On confirmation: Task is deleted and message "Task #<id> deleted." is displayed
6. On cancellation: Deletion is cancelled and message "Task deletion cancelled." is displayed

### Edge Cases
- User enters 'Y' (uppercase) - should be treated as cancellation (only lowercase 'y' confirms)
- User enters 'yes' - should be treated as cancellation
- User enters empty input - should be treated as cancellation
- User enters invalid task ID - appropriate error handling should occur

## Functional Requirements

### FR-001: Exact Confirmation Prompt
**Requirement**: The application must display the exact confirmation prompt: "Are you sure you want to delete task '<title>'?" when a user initiates a delete command.

**Acceptance Criteria**:
- The prompt text matches exactly (case-sensitive, spacing, punctuation)
- The task title is properly escaped/quoted in the prompt
- The prompt is displayed immediately when the delete command is processed

### FR-002: Strict Confirmation Logic
**Requirement**: The application must accept only lowercase 'y' as confirmation to delete the task.

**Acceptance Criteria**:
- Only input of exactly 'y' (lowercase, single character) confirms deletion
- Any other input (including 'Y', 'yes', 'Yes', 'YEs', empty string, etc.) cancels deletion
- The confirmation input is case-sensitive

### FR-003: Deletion Success Message
**Requirement**: When user confirms deletion with 'y', the task must be deleted and the application must display "Task #<id> deleted."

**Acceptance Criteria**:
- The task with the specified ID is removed from the system
- The exact message "Task #<id> deleted." is displayed (with proper ID)
- The task no longer appears in subsequent task listings

### FR-004: Cancellation Message
**Requirement**: When user does not confirm deletion (any input other than 'y'), deletion must be cancelled and "Task deletion cancelled." must be displayed.

**Acceptance Criteria**:
- The task remains in the system
- The exact message "Task deletion cancelled." is displayed
- No changes are made to the task list

### FR-005: Service Method Usage
**Requirement**: The implementation must use `TodoService.get_task(task_id)` to retrieve the task for the confirmation prompt.

**Acceptance Criteria**:
- The delete command implementation calls `TodoService.get_task(task_id)` to get the task
- No other service methods are used to retrieve the task for the prompt
- The retrieved task's title is used in the confirmation prompt

## Success Criteria

### Quantitative Measures
- All integration tests related to the delete functionality pass (100% success rate)
- The delete command handles 100% of confirmation scenarios correctly
- Response time for delete operations remains under 100ms

### Qualitative Measures
- Users can successfully delete tasks using the confirmation workflow
- Users understand the confirmation requirement through clear prompt messaging
- The application behaves consistently across different types of input for confirmation

## Key Entities

### Task
- The primary entity affected by this feature
- Properties: ID (int), title (string), description (string), completed (bool)
- The delete operation removes the specified task from the system

### User Input
- Confirmation input that determines whether deletion proceeds
- Must be exactly 'y' to proceed, any other input cancels

## Assumptions

- The existing `TodoService.get_task(task_id)` method is available and functional
- The CLI framework supports the required input/output patterns
- Integration tests are the authoritative source for expected behavior
- The service layer properly handles the delete operation once confirmed

## Dependencies

- TodoService class with get_task and delete_task methods
- Task model with accessible title property
- CLI input/output system
- Existing integration tests that define expected behavior