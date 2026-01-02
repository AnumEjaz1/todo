"""Unit tests for the TodoService."""
import pytest
from todo_app.service import TodoService
from todo_app.repository import InMemoryTodoRepository
from todo_app.models import Task


class TestTodoService:
    """Test cases for the TodoService class."""

    def setup_method(self):
        """Set up a fresh service instance for each test."""
        self.repository = InMemoryTodoRepository()
        self.service = TodoService(self.repository)

    def test_add_task_success(self):
        """Test adding a task successfully."""
        title = "Test Task"
        description = "Test Description"

        task = self.service.add_task(title, description)

        assert task.title == title
        assert task.description == description
        assert task.completed is False
        assert task.id == 1

    def test_add_task_without_description(self):
        """Test adding a task without description."""
        title = "Test Task"

        task = self.service.add_task(title)

        assert task.title == title
        assert task.description == ""
        assert task.completed is False
        assert task.id == 1

    def test_add_task_empty_title_error(self):
        """Test that adding a task with empty title raises an error."""
        with pytest.raises(ValueError, match="Title cannot be empty or contain only whitespace"):
            self.service.add_task("")

    def test_add_task_whitespace_only_title_error(self):
        """Test that adding a task with whitespace-only title raises an error."""
        with pytest.raises(ValueError, match="Title cannot be empty or contain only whitespace"):
            self.service.add_task("   ")

    def test_add_task_title_too_long_error(self):
        """Test that adding a task with a title longer than 200 characters raises an error."""
        long_title = "x" * 201

        with pytest.raises(ValueError, match="Title must be 200 characters or less"):
            self.service.add_task(long_title)

    def test_add_task_description_too_long_error(self):
        """Test that adding a task with a description longer than 1000 characters raises an error."""
        long_description = "x" * 1001

        with pytest.raises(ValueError, match="Description must be 1000 characters or less"):
            self.service.add_task("Test Task", long_description)

    def test_get_all_tasks_empty_initially(self):
        """Test that get_all_tasks returns an empty list initially."""
        tasks = self.service.get_all_tasks()

        assert tasks == []

    def test_get_all_tasks_returns_all_tasks(self):
        """Test that get_all_tasks returns all added tasks."""
        task1 = self.service.add_task("Task 1")
        task2 = self.service.add_task("Task 2", "Description for task 2")
        task3 = self.service.add_task("Task 3")

        tasks = self.service.get_all_tasks()

        assert len(tasks) == 3
        assert task1 in tasks
        assert task2 in tasks
        assert task3 in tasks

    def test_get_all_tasks_returns_copies_not_references(self):
        """Test that get_all_tasks returns copies to prevent external modification."""
        original_task = self.service.add_task("Task 1")
        tasks = self.service.get_all_tasks()

        # Modify the returned task list
        tasks.append("fake_task")

        # Verify that the original repository wasn't affected
        updated_tasks = self.service.get_all_tasks()
        assert len(updated_tasks) == 1
        assert updated_tasks[0].id == original_task.id


    def test_get_task_by_id_success(self):
        """Test retrieving a task by its ID."""
        task = self.service.add_task("Test Task")

        retrieved_task = self.service.get_task_by_id(task.id)

        assert retrieved_task == task

    def test_get_task_by_id_not_found(self):
        """Test retrieving a non-existent task ID."""
        retrieved_task = self.service.get_task_by_id(999)

        assert retrieved_task is None

    def test_get_task_by_invalid_id(self):
        """Test retrieving a task with invalid ID."""
        with pytest.raises(ValueError, match="Task ID must be a positive integer"):
            self.service.get_task_by_id(-1)

    def test_update_task_success(self):
        """Test updating a task."""
        original_task = self.service.add_task("Original Title", "Original Description")

        updated_task = self.service.update_task(
            original_task.id,
            title="Updated Title",
            description="Updated Description",
            completed=True
        )

        assert updated_task.title == "Updated Title"
        assert updated_task.description == "Updated Description"
        assert updated_task.completed is True

    def test_update_task_partial(self):
        """Test updating only some fields of a task."""
        original_task = self.service.add_task("Original Title", "Original Description")

        updated_task = self.service.update_task(
            original_task.id,
            title="Updated Title"
        )

        assert updated_task.title == "Updated Title"
        assert updated_task.description == "Original Description"  # Should remain unchanged
        assert updated_task.completed is False  # Should remain unchanged

    def test_delete_task_success(self):
        """Test deleting a task."""
        task = self.service.add_task("Test Task")

        result = self.service.delete_task(task.id)

        assert result is True

        # Verify the task no longer exists
        remaining_tasks = self.service.get_all_tasks()
        assert len(remaining_tasks) == 0

    def test_delete_task_not_found(self):
        """Test deleting a non-existent task."""
        result = self.service.delete_task(999)

        assert result is False

    def test_mark_task_complete(self):
        """Test marking a task as complete."""
        task = self.service.add_task("Test Task")
        assert task.completed is False

        completed_task = self.service.mark_task_complete(task.id)

        assert completed_task.completed is True

    def test_mark_task_incomplete(self):
        """Test marking a task as incomplete."""
        task = self.service.add_task("Test Task")
        # First mark as complete
        self.service.mark_task_complete(task.id)

        # Then mark as incomplete
        incomplete_task = self.service.mark_task_incomplete(task.id)

        assert incomplete_task.completed is False

    def test_mark_task_complete_success(self):
        """Test marking a task as complete successfully."""
        task = self.service.add_task("Test Task")
        assert task.completed is False

        completed_task = self.service.mark_task_complete(task.id)

        assert completed_task is not None
        assert completed_task.completed is True

    def test_mark_task_complete_not_found(self):
        """Test marking a non-existent task as complete."""
        result = self.service.mark_task_complete(999)

        assert result is None

    def test_mark_task_complete_invalid_id(self):
        """Test marking a task with invalid ID as complete."""
        with pytest.raises(ValueError, match="Task ID must be a positive integer"):
            self.service.mark_task_complete(-1)

    def test_mark_task_incomplete_success(self):
        """Test marking a task as incomplete successfully."""
        task = self.service.add_task("Test Task")
        # First mark as complete
        self.service.mark_task_complete(task.id)
        # Get the updated task to verify it's complete
        updated_task = self.service.get_task_by_id(task.id)
        assert updated_task.completed is True

        # Then mark as incomplete
        incomplete_task = self.service.mark_task_incomplete(task.id)

        assert incomplete_task is not None
        assert incomplete_task.completed is False

    def test_mark_task_incomplete_not_found(self):
        """Test marking a non-existent task as incomplete."""
        result = self.service.mark_task_incomplete(999)

        assert result is None

    def test_mark_task_incomplete_invalid_id(self):
        """Test marking a task with invalid ID as incomplete."""
        with pytest.raises(ValueError, match="Task ID must be a positive integer"):
            self.service.mark_task_incomplete(-1)

    def test_update_task_success(self):
        """Test updating a task successfully."""
        original_task = self.service.add_task("Original Title", "Original Description")

        updated_task = self.service.update_task(
            original_task.id,
            title="Updated Title",
            description="Updated Description",
            completed=True
        )

        assert updated_task is not None
        assert updated_task.title == "Updated Title"
        assert updated_task.description == "Updated Description"
        assert updated_task.completed is True

    def test_update_task_partial_updates(self):
        """Test updating only some fields of a task."""
        original_task = self.service.add_task("Original Title", "Original Description")

        # Update only the title
        updated_task = self.service.update_task(
            original_task.id,
            title="Updated Title"
        )

        assert updated_task is not None
        assert updated_task.title == "Updated Title"
        assert updated_task.description == "Original Description"  # Should remain unchanged
        assert updated_task.completed is False  # Should remain unchanged

        # Update only the description
        updated_task2 = self.service.update_task(
            original_task.id,
            description="New Description"
        )

        assert updated_task2 is not None
        assert updated_task2.title == "Updated Title"  # Should remain unchanged
        assert updated_task2.description == "New Description"
        assert updated_task2.completed is False  # Should remain unchanged

        # Update only the completion status
        updated_task3 = self.service.update_task(
            original_task.id,
            completed=True
        )

        assert updated_task3 is not None
        assert updated_task3.title == "Updated Title"  # Should remain unchanged
        assert updated_task3.description == "New Description"  # Should remain unchanged
        assert updated_task3.completed is True

    def test_update_task_not_found(self):
        """Test updating a non-existent task."""
        result = self.service.update_task(999, title="New Title")

        assert result is None

    def test_update_task_invalid_id(self):
        """Test updating a task with invalid ID."""
        with pytest.raises(ValueError, match="Task ID must be a positive integer"):
            self.service.update_task(-1, title="New Title")

    def test_update_task_empty_title_error(self):
        """Test updating a task with an empty title."""
        task = self.service.add_task("Original Title")

        with pytest.raises(ValueError, match="Title cannot be empty or contain only whitespace"):
            self.service.update_task(task.id, title="")

    def test_update_task_whitespace_only_title_error(self):
        """Test updating a task with a whitespace-only title."""
        task = self.service.add_task("Original Title")

        with pytest.raises(ValueError, match="Title cannot be empty or contain only whitespace"):
            self.service.update_task(task.id, title="   ")

    def test_update_task_title_too_long_error(self):
        """Test updating a task with a title longer than 200 characters."""
        task = self.service.add_task("Original Title")
        long_title = "x" * 201

        with pytest.raises(ValueError, match="Title must be 200 characters or less"):
            self.service.update_task(task.id, title=long_title)

    def test_update_task_description_too_long_error(self):
        """Test updating a task with a description longer than 1000 characters."""
        task = self.service.add_task("Original Title")
        long_description = "x" * 1001

        with pytest.raises(ValueError, match="Description must be 1000 characters or less"):
            self.service.update_task(task.id, description=long_description)

    def test_delete_task_success(self):
        """Test deleting a task successfully."""
        task = self.service.add_task("Task to Delete")

        result = self.service.delete_task(task.id)

        assert result is True
        # Verify the task no longer exists
        remaining_tasks = self.service.get_all_tasks()
        assert len(remaining_tasks) == 0

    def test_delete_task_not_found(self):
        """Test deleting a non-existent task."""
        result = self.service.delete_task(999)

        assert result is False

    def test_delete_task_invalid_id(self):
        """Test deleting a task with invalid ID."""
        with pytest.raises(ValueError, match="Task ID must be a positive integer"):
            self.service.delete_task(-1)

    def test_delete_task_then_verify_nonexistent(self):
        """Test that a deleted task cannot be retrieved."""
        task = self.service.add_task("Task to Delete")

        # Delete the task
        result = self.service.delete_task(task.id)
        assert result is True

        # Verify it cannot be retrieved
        retrieved_task = self.service.get_task_by_id(task.id)
        assert retrieved_task is None

        # Verify it doesn't appear in the task list
        all_tasks = self.service.get_all_tasks()
        assert task not in all_tasks