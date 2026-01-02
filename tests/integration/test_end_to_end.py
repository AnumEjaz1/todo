"""Integration tests for the todo application."""
import io
import sys
from contextlib import redirect_stdout
from unittest.mock import patch
from todo_app.repository import InMemoryTodoRepository
from todo_app.service import TodoService
from todo_app.cli import TodoCLI


class TestEndToEnd:
    """End-to-end integration tests for the todo application."""

    def setup_method(self):
        """Set up a fresh application instance for each test."""
        self.repository = InMemoryTodoRepository()
        self.service = TodoService(self.repository)
        self.cli = TodoCLI(self.service)

    def test_add_task_through_cli(self):
        """Test adding a task through the CLI interface."""
        # Mock user input for the add command
        with patch('builtins.input', side_effect=['add Test Task Test Description', 'quit']):
            # Capture the output
            f = io.StringIO()
            with redirect_stdout(f):
                self.cli.run()

            output = f.getvalue()

        # Verify the task was added
        tasks = self.service.get_all_tasks()
        assert len(tasks) == 1
        assert tasks[0].title == "Test Task"
        assert tasks[0].description == "Test Description"
        assert tasks[0].completed is False

    def test_view_tasks_through_cli(self):
        """Test viewing tasks through the CLI interface."""
        # Add a task first
        self.service.add_task("Test Task", "Test Description")

        # Mock user input for the view command
        with patch('builtins.input', side_effect=['view', 'quit']):
            # Capture the output
            f = io.StringIO()
            with redirect_stdout(f):
                self.cli.run()

            output = f.getvalue()

        # Verify the output contains the task
        assert "Test Task" in output
        assert "Test Description" in output

    def test_complete_task_through_cli(self):
        """Test marking a task as complete through the CLI interface."""
        # Add a task first
        task = self.service.add_task("Test Task")

        # Mock user input for the complete command
        with patch('builtins.input', side_effect=[f'complete {task.id}', 'view', 'quit']):
            # Capture the output
            f = io.StringIO()
            with redirect_stdout(f):
                self.cli.run()

            output = f.getvalue()

        # Verify the task is marked as complete
        updated_task = self.service.get_task_by_id(task.id)
        assert updated_task.completed is True

    def test_update_task_through_cli(self):
        """Test updating a task through the CLI interface."""
        # Add a task first
        task = self.service.add_task("Original Title", "Original Description")

        # Mock user input for the update command
        with patch('builtins.input', side_effect=[f'update {task.id} New Title New Description', 'view', 'quit']):
            # Capture the output
            f = io.StringIO()
            with redirect_stdout(f):
                self.cli.run()

            output = f.getvalue()

        # Verify the task was updated
        updated_task = self.service.get_task_by_id(task.id)
        assert updated_task.title == "New Title"
        assert updated_task.description == "New Description"

    def test_delete_task_through_cli(self):
        """Test deleting a task through the CLI interface."""
        # Add a task first
        task = self.service.add_task("Test Task")

        # Mock user input for the delete command
        with patch('builtins.input', side_effect=[f'delete {task.id}', 'view', 'quit']):
            # Capture the output
            f = io.StringIO()
            with redirect_stdout(f):
                self.cli.run()

            output = f.getvalue()

        # Verify the task was deleted
        tasks = self.service.get_all_tasks()
        assert len(tasks) == 0

    def test_view_tasks_through_cli_integration(self):
        """Integration test for viewing tasks through the CLI interface."""
        # Add some tasks first
        task1 = self.service.add_task("Task 1", "Description for task 1")
        task2 = self.service.add_task("Task 2", "Description for task 2")
        # Mark one task as complete
        self.service.mark_task_complete(task2.id)

        # Mock user input for the view command
        with patch('builtins.input', side_effect=['view', 'quit']):
            # Capture the output
            f = io.StringIO()
            with redirect_stdout(f):
                self.cli.run()

            output = f.getvalue()

        # Verify the output contains the tasks
        assert "Task 1" in output
        assert "Description for task 1" in output
        assert "Task 2" in output
        assert "Description for task 2" in output
        # Verify that the completed task is marked as complete
        assert "[✓]" in output
        # Verify that the pending task is marked as pending
        assert "[○]" in output

    def test_mark_task_complete_through_cli_integration(self):
        """Integration test for marking tasks complete through the CLI interface."""
        # Add a task first
        task = self.service.add_task("Task to Complete", "Description for task to complete")

        # Mock user input for the complete command
        with patch('builtins.input', side_effect=[f'complete {task.id}', 'view', 'quit']):
            # Capture the output
            f = io.StringIO()
            with redirect_stdout(f):
                self.cli.run()

            output = f.getvalue()

        # Verify the task is now marked as complete
        assert f"Task #{task.id} marked as complete: Task to Complete" in output
        # Verify that the task appears as complete when viewing
        assert "[✓]" in output
        assert "Task to Complete" in output

    def test_mark_task_incomplete_through_cli_integration(self):
        """Integration test for marking tasks incomplete through the CLI interface."""
        # Add a task and mark it as complete
        task = self.service.add_task("Task to Uncomplete", "Description for task to uncomplete")
        self.service.mark_task_complete(task.id)

        # Mock user input for the uncomplete command
        with patch('builtins.input', side_effect=[f'uncomplete {task.id}', 'view', 'quit']):
            # Capture the output
            f = io.StringIO()
            with redirect_stdout(f):
                self.cli.run()

            output = f.getvalue()

        # Verify the task is now marked as incomplete
        assert f"Task #{task.id} marked as incomplete: Task to Uncomplete" in output
        # Verify that the task appears as incomplete when viewing
        assert "[○]" in output
        assert "Task to Uncomplete" in output

    def test_update_task_through_cli_integration(self):
        """Integration test for updating tasks through the CLI interface."""
        # Add a task first
        task = self.service.add_task("Original Title", "Original Description")

        # Mock user input for the update command
        with patch('builtins.input', side_effect=[f'update {task.id} New Title New Description', 'view', 'quit']):
            # Capture the output
            f = io.StringIO()
            with redirect_stdout(f):
                self.cli.run()

            output = f.getvalue()

        # Verify the task was updated
        assert f"Updated task #{task.id}: New Title" in output
        # Verify that the updated task appears when viewing
        assert "New Title" in output
        assert "New Description" in output

    def test_delete_task_through_cli_integration(self):
        """Integration test for deleting tasks through the CLI interface."""
        # Add a task first
        task = self.service.add_task("Task to Delete", "Description for task to delete")

        # Mock user input for the delete command with confirmation
        with patch('builtins.input', side_effect=[f'delete {task.id}', 'y', 'view', 'quit']):
            # Capture the output
            f = io.StringIO()
            with redirect_stdout(f):
                self.cli.run()

            output = f.getvalue()

        # Verify the task was deleted
        assert f"Are you sure you want to delete task 'Task to Delete'?" in output
        assert f"Task #{task.id} deleted." in output
        # Verify that the task no longer appears when viewing
        assert "Task to Delete" not in output

    def test_delete_task_cancelled_through_cli_integration(self):
        """Integration test for cancelling task deletion through the CLI interface."""
        # Add a task first
        task = self.service.add_task("Task to Delete", "Description for task to delete")

        # Mock user input for the delete command with cancellation
        with patch('builtins.input', side_effect=[f'delete {task.id}', 'n', 'view', 'quit']):
            # Capture the output
            f = io.StringIO()
            with redirect_stdout(f):
                self.cli.run()

            output = f.getvalue()

        # Verify the task deletion was cancelled
        assert f"Are you sure you want to delete task 'Task to Delete'?" in output
        assert "Task deletion cancelled." in output
        # Verify that the task still appears when viewing
        assert "Task to Delete" in output