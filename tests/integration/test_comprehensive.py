"""Comprehensive end-to-end integration tests for the todo application."""
import io
import sys
from contextlib import redirect_stdout
from unittest.mock import patch
from todo_app.repository import InMemoryTodoRepository
from todo_app.service import TodoService
from todo_app.cli import TodoCLI


class TestComprehensiveEndToEnd:
    """Comprehensive end-to-end integration tests for all features working together."""

    def setup_method(self):
        """Set up a fresh application instance for each test."""
        self.repository = InMemoryTodoRepository()
        self.service = TodoService(self.repository)
        self.cli = TodoCLI(self.service)

    def test_full_workflow_all_features(self):
        """Test a complete workflow using all features together."""
        # Test adding multiple tasks
        with patch('builtins.input', side_effect=[
            'add Task1 Description1',
            'add Task2 Description2',
            'add Task3 Description3',
            'view',
            'complete 1',
            'update 2 NewTitle NewDescription',
            'view',
            'delete 3',
            'view',
            'quit'
        ]):
            f = io.StringIO()
            with redirect_stdout(f):
                self.cli.run()

            output = f.getvalue()

        # Verify all operations worked as expected
        # Check that tasks were added
        assert "Added task #1: Task1" in output
        assert "Added task #2: Task2" in output
        assert "Added task #3: Task3" in output

        # Check that tasks were displayed
        assert "Task1" in output
        assert "Description1" in output
        assert "Task2" in output
        assert "Description2" in output
        assert "Task3" in output

        # Check that task 1 was marked complete
        assert "Task #1 marked as complete: Task1" in output

        # Check that task 2 was updated
        assert "Updated task #2: NewTitle" in output

        # Check that task 3 was deleted
        assert "Task #3 deleted." in output

        # Final view should show only tasks 1 (completed) and 2 (updated title/desc)
        assert "NewTitle" in output
        assert "NewDescription" in output
        assert "[✓]" in output  # Task 1 should be marked complete
        assert "Task3" not in output  # Task 3 should be gone

    def test_error_handling_workflow(self):
        """Test error handling across different operations."""
        with patch('builtins.input', side_effect=[
            'add',  # Invalid add command
            'add ValidTask ValidDescription',
            'complete 999',  # Non-existent task
            'update 999 NewTitle',  # Non-existent task
            'delete 999',  # Non-existent task
            'view',
            'quit'
        ]):
            f = io.StringIO()
            with redirect_stdout(f):
                self.cli.run()

            output = f.getvalue()

        # Verify error messages were shown
        assert "Usage: add <title> [description]" in output
        assert "Task #999 not found." in output  # Multiple times for different operations
        assert "ValidTask" in output  # The valid task should still be there

    def test_task_lifecycle_complete(self):
        """Test the complete lifecycle of a task through all operations."""
        # Add a task
        task = self.service.add_task("Lifecycle Task", "Test description for lifecycle")

        # Verify it's added correctly
        tasks = self.service.get_all_tasks()
        assert len(tasks) == 1
        assert tasks[0].title == "Lifecycle Task"
        assert tasks[0].description == "Test description for lifecycle"
        assert tasks[0].completed is False

        # Mark it as complete
        completed_task = self.service.mark_task_complete(task.id)
        assert completed_task.completed is True

        # Update its details
        updated_task = self.service.update_task(task.id, title="Updated Lifecycle Task", description="Updated description")
        assert updated_task.title == "Updated Lifecycle Task"
        assert updated_task.description == "Updated description"
        assert updated_task.completed is True  # Should still be complete

        # Delete the task
        result = self.service.delete_task(task.id)
        assert result is True

        # Verify it's gone
        final_tasks = self.service.get_all_tasks()
        assert len(final_tasks) == 0