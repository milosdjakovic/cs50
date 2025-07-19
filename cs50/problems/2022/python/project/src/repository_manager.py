import sys
import os
from src.renderer import Renderer
from src.repository import Repository
from src.todo_manager import TodoManager


class RepositoryManager:
    def __init__(self, base_dir, repository=None):
        repository_dir = "default" if repository is None else repository
        repository_path = os.path.join(base_dir, repository_dir)
        self._repository = Repository(
            repository=repository_path,
            repository_name=repository_dir,
        )

    def load(self):
        """
        Load the repository and display the lists.
        """
        self.render_repository()

    def render_repository(self):
        try:
            while True:
                Renderer.clear_screen()
                print(self._repository)
                print(
                    Renderer.commands(
                        {
                            "s": "select",
                            "a": "add",
                            "r": "rename",
                            "d": "delete",
                            "e": "exit",
                        }
                    )
                )
                cmd = input("Enter a command: ").strip().lower()
                if cmd == "a":
                    self.add_list()
                elif cmd == "r":
                    self.rename_list()
                elif cmd == "d":
                    self.delete_list()
                elif cmd == "s":
                    self.select_list()
                elif cmd == "e":
                    self.quit()
                else:
                    pass
        except (KeyboardInterrupt, EOFError):
            self.quit()

    def add_list(self, name=None):
        """
        Add a new list with the given name.
        If name is None, prompt the user for a name.
        """
        if name is None:
            name = input("Enter the name of the list: ")

        if name:
            try:
                self._repository.create_list(name)
                return True
            except FileExistsError:
                return False
        else:
            return False

    def rename_list(self, list_number: str = None, new_name: str = None):
        """
        Rename an existing list.
        If list_number is None, prompt the user for an index.
        If new_name is None, prompt the user for a new name.
        """
        try:
            if list_number is None:
                list_number = int(input("Enter the index of the list to rename: "))
            list_number = int(list_number)
        except ValueError:
            return False

        index = list_number - 1
        if not 0 <= index < len(self._repository):
            return False

        if list_number < 1 or list_number > len(self._repository):
            return False

        if new_name is None:
            new_name = input("Enter the new name: ")

        if not new_name:
            return False

        return self._repository.rename_list(index, new_name)

    def delete_list(self, list_number: str = None):
        """
        Delete a list at the given list_number.
        If list_number is None, prompt the user for an list_number.
        """
        try:
            if list_number is None:
                list_number = int(input("Enter the index of the list to delete: "))
            list_number = int(list_number)
        except ValueError:
            return False

        index = list_number - 1
        if not 0 <= index < len(self._repository):
            return False

        return self._repository.delete_list(index)

    def select_list(self):
        """
        Select and render a list by its number
        """
        todo_manager = self.get_list()

        if todo_manager:
            todo_manager.render_todos()

    def get_list(self, list_number: str = None):
        """
        Get a TodoManager for the list at a valid given number.

        Args:
            list_number: The number of the list to select (1-indexed)

        Returns:
            TodoManager instance if successful, None otherwise
        """
        try:
            if list_number is None:
                list_number = int(input("Enter the number of the list to select: "))
            list_number = int(list_number)
        except ValueError:
            return None

        list_index = list_number - 1
        if not 0 <= list_index < len(self._repository):
            return None

        try:
            list_name = self._repository.todos[list_index]
            return TodoManager(list=list_name)
        except Exception:
            return None

    def quit(self):
        Renderer.clear_screen()
        print(Renderer.box("Bye"))
        sys.exit()
