import os


class Renderer:
    @classmethod
    def title(cls, title: str) -> str:
        return f"=== {title} ==="

    @classmethod
    def box(cls, content: str) -> str:
        """
        Create a box around the content with a dashed line.
        The box will adjust its width based on the longest line of content.

        Args:
            content (str): The content to be boxed.

        Returns:
            str: The content wrapped in a box.
        """

        lines = content.split("\n")
        max_length = max(len(line) for line in lines)
        box_width = max_length + 4
        dashed_line = "+" + "-" * (box_width - 2) + "+"

        box_content = [dashed_line]
        for line in lines:
            box_content.append(f"| {line.ljust(max_length)} |")
        box_content.append(dashed_line)

        return "\n".join(box_content)

    @classmethod
    def todo(cls, title: str, completed: bool) -> str:
        """
        Create a string representation of a todo item.

        Args:
            title (str): The title of the todo item.
            completed (bool): The completion status of the todo item.

        Returns:
            str: The string representation of the todo item.
        """

        status = "[x]" if completed else "[ ]"
        return f"{status} {title}"

    @classmethod
    def commands(cls, commands: dict) -> str:
        """
        Create a string representation of available commands.

        Args:
            commands (dict): A dictionary of command names and their descriptions.
            Example: {"t": "toggle", "a": "add", "r": "rename", "d": "delete", "b": "back", "e": "exit"}
        Returns:
            str: The string representation of the commands.
        """

        command_strings = []
        for command, description in commands.items():
            command_strings.append(f"{command}: {description}")

        commands_text = ", ".join(command_strings)
        return cls.box(f"Commands -> {commands_text}")

    @classmethod
    def clear_screen(cls):
        """
        Clear the console screen.
        This method checks the operating system and uses the appropriate command to clear the screen.
        """

        if os.name == "posix":
            os.system("clear")
        else:
            os.system("cls")
