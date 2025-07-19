import os
from src.renderer import Renderer


class Repository:
    def __init__(self, repository, repository_name):
        self.repository = repository
        self.repository_name = repository_name

    @property
    def files(self):
        try:
            if not os.path.isdir(self.repository):
                return []
            files = os.listdir(self.repository)
            return files
        except Exception as e:
            print(f"Error listing files: {e}")
            return []

    @property
    def todos(self):
        formatted_files = []
        for file in self.files:
            if file.endswith(".csv"):
                formatted_name = file[:-4]
                formatted_files.append(formatted_name)
        return formatted_files

    @property
    def list_names(self):
        formatted_names = []
        for file in self.files:
            if file.endswith(".csv"):
                formatted_name = file[:-4]  # Remove the .csv extension
                formatted_names.append(formatted_name)
            else:
                formatted_names.append(file)
        return formatted_names

    @property
    def longest_list_name_length(self):
        if self.list_names:
            return max(len(name) for name in self.list_names)
        return 0

    def create_list(self, name):
        if not os.path.isdir(self.repository):
            os.makedirs(self.repository)
        file_path = os.path.join(self.repository, f"{name}.csv")
        if os.path.exists(file_path):
            raise FileExistsError(f"List '{name}' already exists")
        with open(file_path, "w") as _:
            pass
        return True

    def delete_list(self, index: int):
        try:
            if 0 <= index < len(self.files):
                file_path = os.path.join(self.repository, self.files[index])
                os.remove(file_path)
                return True
            else:
                print("Index out of range")
                return False
        except Exception as e:
            print(f"Error deleting list: {e}")
            return False

    def rename_list(self, index: int, new_name: str):
        try:
            if 0 <= index < len(self.files):
                old_file_path = os.path.join(self.repository, self.files[index])
                new_file_path = os.path.join(self.repository, f"{new_name}.csv")
                os.rename(old_file_path, new_file_path)
                return True
            else:
                print("Index out of range")
                return False
        except Exception as e:
            print(f"Error renaming list: {e}")
            return False

    def __len__(self):
        return len(self.list_names)

    def __str__(self):
        list = ""

        for i, file in enumerate(self.list_names, 1):
            list += f"{i}. {file}"
            if i < len(self.list_names):
                list += "\n"

        app_title = Renderer.title(self.repository_name)

        if self.list_names:
            return f"{app_title}\n{Renderer.box(list)}"
        else:
            return f"{app_title}\n{Renderer.box('No lists found. Create one.')}"
