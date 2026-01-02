"""Service layer for business logic of the todo application."""
from typing import List, Optional
from .models import Task
from .repository import InMemoryTodoRepository


class TodoService:
    """Service class that handles business logic for todo operations.

    This class acts as an intermediary between the CLI layer and the repository,
    providing methods to perform all todo operations with appropriate validation
    and error handling.
    """

    def __init__(self, repository: InMemoryTodoRepository):
        """Initialize the service with a repository.

        Args:
            repository (InMemoryTodoRepository): The repository to use for data operations
        """
        self._repository = repository

    def add_task(self, title: str, description: str = "") -> Task:
        """Add a new task with the given title and description.

        Args:
            title (str): The title of the task (required)
            description (str): The description of the task (optional, default: "")

        Returns:
            Task: The newly created Task object

        Raises:
            ValueError: If title is empty, too long, or description is too long
        """
        # Validate inputs
        if not title or not title.strip():
            raise ValueError("Title cannot be empty or contain only whitespace")

        if len(title) > 200:
            raise ValueError("Title must be 200 characters or less")

        if len(description) > 1000:
            raise ValueError("Description must be 1000 characters or less")

        return self._repository.create_task(title, description)

    def get_all_tasks(self) -> List[Task]:
        """Get all tasks.

        Returns:
            List[Task]: A list of all tasks in the repository
        """
        return self._repository.get_all_tasks()

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """Get a task by its ID.

        Args:
            task_id (int): The ID of the task to retrieve

        Returns:
            Task or None: The task with the given ID, or None if not found

        Raises:
            ValueError: If task_id is not a positive integer
        """
        if task_id <= 0:
            raise ValueError("Task ID must be a positive integer")

        return self._repository.get_task_by_id(task_id)

    def update_task(self, task_id: int, title: Optional[str] = None,
                    description: Optional[str] = None, completed: Optional[bool] = None) -> Optional[Task]:
        """Update a task with the given ID.

        Args:
            task_id (int): The ID of the task to update
            title (str, optional): New title for the task
            description (str, optional): New description for the task
            completed (bool, optional): New completion status for the task

        Returns:
            Task or None: The updated task, or None if task with given ID not found

        Raises:
            ValueError: If task_id is not positive, or if new title/description are invalid
        """
        if task_id <= 0:
            raise ValueError("Task ID must be a positive integer")

        # Validate inputs if provided
        if title is not None:
            if not title or not title.strip():
                raise ValueError("Title cannot be empty or contain only whitespace")

            if len(title) > 200:
                raise ValueError("Title must be 200 characters or less")

        if description is not None and len(description) > 1000:
            raise ValueError("Description must be 1000 characters or less")

        return self._repository.update_task(task_id, title, description, completed)

    def delete_task(self, task_id: int) -> bool:
        """Delete a task by its ID.

        Args:
            task_id (int): The ID of the task to delete

        Returns:
            bool: True if the task was deleted, False if not found

        Raises:
            ValueError: If task_id is not a positive integer
        """
        if task_id <= 0:
            raise ValueError("Task ID must be a positive integer")

        return self._repository.delete_task(task_id)

    def mark_task_complete(self, task_id: int) -> Optional[Task]:
        """Mark a task as complete.

        Args:
            task_id (int): The ID of the task to mark as complete

        Returns:
            Task or None: The updated task, or None if task with given ID not found

        Raises:
            ValueError: If task_id is not a positive integer
        """
        if task_id <= 0:
            raise ValueError("Task ID must be a positive integer")

        task = self._repository.get_task_by_id(task_id)
        if task is None:
            return None

        return self._repository.update_task(task_id, completed=True)

    def mark_task_incomplete(self, task_id: int) -> Optional[Task]:
        """Mark a task as incomplete.

        Args:
            task_id (int): The ID of the task to mark as incomplete

        Returns:
            Task or None: The updated task, or None if task with given ID not found

        Raises:
            ValueError: If task_id is not a positive integer
        """
        if task_id <= 0:
            raise ValueError("Task ID must be a positive integer")

        task = self._repository.get_task_by_id(task_id)
        if task is None:
            return None

        return self._repository.update_task(task_id, completed=False)