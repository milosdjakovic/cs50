import csv
import os
from typing import List
from src.todo import Todo
from src.renderer import Renderer


class Todos:
    def __init__(self, list_name="todos", repository_path="repository"):
        self.list_name = list_name
        self._filename = f"{list_name}.csv"
        self._repository_path = repository_path
        self._tasks: List[Todo] = []
        self.load()

    @property
    def filepath(self):
        return os.path.join(self._repository_path, self._filename)

    def load(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, "r", newline="") as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    title, completed = row
                    task = Todo(title)
                    task.completed = completed == "True"
                    self._tasks.append(task)

    def add(self, task: Todo):
        self._tasks.append(task)
        self.save()

    def toggle(self, index: int):
        if 0 <= index < len(self._tasks):
            self._tasks[index].toggle()
            self.save()
        else:
            raise IndexError("Index out of range")

    def delete(self, index: int):
        if 0 <= index < len(self._tasks):
            del self._tasks[index]
            self.save()
        else:
            raise IndexError("Index out of range")

    def rename(self, index: int, new_title: str):
        if 0 <= index < len(self._tasks):
            self._tasks[index].title = new_title
            self.save()
        else:
            raise IndexError("Index out of range")

    def save(self):
        os.makedirs(self._repository_path, exist_ok=True)

        with open(self.filepath, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            for task in self._tasks:
                writer.writerow([task.title, task.completed])

    def __getitem__(self, index):
        return self._tasks[index]

    def __len__(self):
        return len(self._tasks)

    def __str__(self):
        list = ""

        for i, task in enumerate(self._tasks, 1):
            list += f"{i}. {task}"
            if i < len(self._tasks):
                list += "\n"

        app_title = Renderer.title(self.list_name)

        if self._tasks:
            return f"{app_title}\n{Renderer.box(list)}"
        else:
            return f"{app_title}\n{Renderer.box('No todos found. Create one.')}"
