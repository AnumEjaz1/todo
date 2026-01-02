# Quickstart Guide: Todo In-Memory Python Console App

**Feature**: 001-todo-console-app
**Date**: 2026-01-01

## Project Setup

### Prerequisites
- Python 3.13+ installed
- UV package manager installed

### Installation
1. Navigate to project directory
2. Initialize UV project: `uv init`
3. Install dependencies: `uv add <any-needed-deps>` (though Phase I uses standard library only)

### Running the Application
```bash
python -m todo_app.main
```

## Project Structure
```
todo_app/
├── __init__.py
├── main.py              # Program entry & REPL loop
├── models.py            # Task dataclass
├── repository.py        # InMemoryTodoRepository
├── service.py           # TodoService
├── cli.py               # UI commands & display logic
└── utils.py             # Helpers (optional)
```

## Core Components

### Task Model (`models.py`)
- Defines the Task dataclass with id, title, description, and completed fields
- Includes validation for task attributes

### Repository (`repository.py`)
- InMemoryTodoRepository class manages the task list
- Provides CRUD operations (create, read, update, delete)
- Handles auto-incrementing task IDs

### Service (`service.py`)
- TodoService orchestrates business logic
- Validates operations before repository calls
- Handles error cases and returns appropriate responses

### CLI (`cli.py`)
- Parses user commands and routes to service
- Formats output for user readability
- Manages the REPL loop and user interaction

### Main (`main.py`)
- Application entry point
- Initializes components and starts the REPL loop

## Available Commands
- `add <task-title>` - Add a new task
- `list` - View all tasks
- `update <task-id> <new-title>` - Update a task's title
- `complete <task-id>` - Mark a task as complete
- `delete <task-id>` - Delete a task
- `help` - Show available commands
- `exit` - Quit the application

## Development Guidelines
- Follow PEP 8 standards
- Write unit tests for each module
- Include type hints for all functions
- Add docstrings to all public methods
- Handle errors gracefully with user-friendly messages