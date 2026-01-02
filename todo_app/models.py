"""Data models for the todo application."""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Task:
    """Represents a single todo task with its properties.

    Attributes:
        id (int): Unique identifier for the task
        title (str): Brief description of the task
        description (str): Detailed description of the task (optional)
        completed (bool): Completion status of the task (default: False)
    """

    id: int
    title: str
    description: str = ""
    completed: bool = False

    def __post_init__(self):
        """Validate the task after initialization.

        Raises:
            ValueError: If title is empty, too long, description is too long,
                       or ID is not a positive integer
        """
        if not self.title or not self.title.strip():
            raise ValueError("Title cannot be empty or contain only whitespace")

        if len(self.title) > 200:
            raise ValueError("Title must be 200 characters or less")

        if len(self.description) > 1000:
            raise ValueError("Description must be 1000 characters or less")

        if not isinstance(self.id, int) or self.id <= 0:
            raise ValueError("ID must be a positive integer")