from src.renderer import Renderer


class Todo:
    def __init__(self, title: str):
        self.title = title
        self.completed = False

    def toggle(self):
        self.completed = not self.completed

    def __len__(self):
        return len(self.title)

    def __str__(self):
        return Renderer.todo(self.title, self.completed)
