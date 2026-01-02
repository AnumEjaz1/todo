"""Repository for managing todo tasks in memory."""
from typing import List, Optional
from .models import Task


class InMemoryTodoRepository:
    """In-memory repository for storing and managing Task objects.

    This class provides methods to create, read, update, and delete Task objects
    in memory. It maintains an internal list of tasks and an auto-incrementing
    ID counter for new tasks.
    """

    def __init__(self):
        """Initialize the repository with an empty list of tasks and an ID counter."""
        self._tasks: List[Task] = []
        self._next_id = 1

    def create_task(self, title: str, description: str = "") -> Task:
        """Create a new task with the given title and description.

        Args:
            title (str): The title of the task (required)
            description (str): The description of the task (optional, default: "")

        Returns:
            Task: The newly created Task object with a unique ID

        Raises:
            ValueError: If title is empty, too long, or description is too long
        """
        # Validate inputs before creating the task
        if not title or not title.strip():
            raise ValueError("Title cannot be empty or contain only whitespace")

        if len(title) > 200:
            raise ValueError("Title must be 200 characters or less")

        if len(description) > 1000:
            raise ValueError("Description must be 1000 characters or less")

        task = Task(
            id=self._next_id,
            title=title.strip(),
            description=description,
            completed=False
        )

        self._tasks.append(task)
        self._next_id += 1

        return task

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """Retrieve a task by its ID.

        Args:
            task_id (int): The ID of the task to retrieve

        Returns:
            Task or None: The task with the given ID, or None if not found
        """
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    def get_all_tasks(self) -> List[Task]:
        """Retrieve all tasks.

        Returns:
            List[Task]: A copy of the list of all tasks in the repository
        """
        return self._tasks.copy()  # Return a copy to prevent external modification

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
            ValueError: If new title is empty, too long, or description is too long
        """
        task = self.get_task_by_id(task_id)
        if task is None:
            return None

        # Update fields if they are provided
        if title is not None:
            if not title or not title.strip():
                raise ValueError("Title cannot be empty or contain only whitespace")

            if len(title) > 200:
                raise ValueError("Title must be 200 characters or less")

            task.title = title.strip()

        if description is not None:
            if len(description) > 1000:
                raise ValueError("Description must be 1000 characters or less")

            task.description = description

        if completed is not None:
            task.completed = completed

        return task

    def delete_task(self, task_id: int) -> bool:
        """Delete a task by its ID.

        Args:
            task_id (int): The ID of the task to delete

        Returns:
            bool: True if the task was deleted, False if not found
        """
        task = self.get_task_by_id(task_id)
        if task is None:
            return False

        self._tasks.remove(task)
        return True

    def get_next_id(self) -> int:
        """Get the next available ID for a new task.

        Returns:
            int: The next available ID
        """
        return self._next_id