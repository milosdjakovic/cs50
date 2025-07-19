import sys
from src.todo import Todo
from src.todos import Todos
from src.renderer import Renderer


class TodoManager:
    def __init__(self, list=None, repository_path="repository"):
        self._todos = Todos(list_name=list, repository_path=repository_path)

    def render_todos(self):
        while True:
            Renderer.clear_screen()
            print(self._todos)

            commands = {
                "a": "add",
                "r": "rename",
                "d": "delete",
                "b": "back",
                "e": "exit",
            }
            if len(self._todos) > 0:
                commands = {"t": "toggle", **commands}
            print(Renderer.commands(commands))
            cmd = input("Enter a command: ").strip().lower()
            if cmd == "a":
                self.add_todo()
            elif cmd == "r":
                self.rename_todo()
            elif cmd == "d":
                self.delete_todo()
            elif cmd == "t":
                self.toggle_todo()
            elif cmd == "b":
                return
            elif cmd == "e":
                self.quit()
            else:
                pass

    def add_todo(self, title=None):
        """
        Add a new todo with the given title.

        Args:
            title: Optional title for the todo. If None, prompt the user.

        Returns:
            bool: True if todo was added, False otherwise
        """
        if title is None:
            title = input("Enter the title of the todo: ")

        return self._create_todo(title)

    def _create_todo(self, title):
        """
        Create a todo with the given title.

        Returns:
            bool: True if successful, False otherwise
        """
        if not title:
            raise ValueError("Title cannot be empty.")

        todo = Todo(title)
        self._todos.add(todo)
        return True

    def delete_todo(self, index=None):
        """
        Delete a todo at the given index.
        If index is None, prompt the user.
        """
        if index is None:
            try:
                index = int(input("Enter the number of the todo to delete: ")) - 1
            except ValueError:
                print("Invalid input. Please enter a number.")
                return False

        self._todos.delete(index)
        return True

    def rename_todo(self, index: str = None, new_title: str = None):
        """
        Rename a todo at the given index.
        If index is None, prompt the user.
        """
        try:
            if index is None:
                index = int(input("Enter the number of the todo to rename: ")) - 1
                index = int(index)
        except ValueError:
            return False

        if index < 0 or index >= len(self._todos):
            return False

        try:
            if new_title is None:
                new_title = input("Enter the new title: ")
            if not new_title:
                raise ValueError("Title cannot be empty.")
        except ValueError:
            return False

        self._todos.rename(index, new_title)
        return True

    def toggle_todo(self, index: str = None):
        """
        Toggle the completion status of a todo at the given index.
        If index is None, prompt the user.
        """
        try:
            if index is None:
                index = int(input("Enter the number of the todo to toggle: ")) - 1
                index = int(index)
        except ValueError:
            return False

        try:
            self._todos.toggle(index)
            return True
        except (ValueError, IndexError):
            return False

    def quit(self):
        Renderer.clear_screen()
        print(Renderer.box("Bye"))
        sys.exit()
