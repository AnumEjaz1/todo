"""Main entry point for the todo application."""
from .cli import TodoCLI
from .service import TodoService
from .repository import InMemoryTodoRepository


def main():
    """Main entry point for the application.

    This function initializes all the required components (repository, service, and CLI)
    and starts the interactive command-line interface for the todo application.
    """
    # Initialize the application components
    repository = InMemoryTodoRepository()
    service = TodoService(repository)
    cli = TodoCLI(service)

    # Run the CLI
    cli.run()


if __name__ == "__main__":
    main()