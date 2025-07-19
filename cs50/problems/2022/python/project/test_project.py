import os
import pytest
from src.renderer import Renderer
from src.repository_manager import RepositoryManager
from src.todo_manager import TodoManager
from src.repository import Repository
from src.todos import Todos
from src.todo import Todo


# === Renderer ===
def test_renderer_title():
    assert Renderer.title("Test") == "=== Test ==="
    assert Renderer.title("") == "===  ==="


def test_renderer_box():
    assert Renderer.box("Test") == "+------+\n| Test |\n+------+"
    assert (
        Renderer.box("Test\nLong line 2")
        == "+-------------+\n| Test        |\n| Long line 2 |\n+-------------+"
    )
    assert Renderer.box("") == "+--+\n|  |\n+--+"


# === RepositoryManager ===
def test_repository_manager_add_list(tmp_path):
    repo_dir = tmp_path / "test_repo"
    repo_manager = RepositoryManager(str(repo_dir))
    assert repo_manager.add_list("Test List") is True


def test_repository_manager_add_list_already_exists(tmp_path):
    repo_dir = tmp_path / "test_repo"
    repo_manager = RepositoryManager(str(repo_dir))
    repo_manager.add_list("Test List")
    assert repo_manager.add_list("Test List") is False


def test_repository_manager_rename_list(tmp_path):
    repo_dir = tmp_path / "test_repo"
    repo_manager = RepositoryManager(str(repo_dir))
    repo_manager.add_list("Test List")
    assert repo_manager.rename_list("1", "Renamed List") is True


def test_repository_manager_rename_list_invalid_index(tmp_path):
    repo_dir = tmp_path / "test_repo"
    repo_manager = RepositoryManager(str(repo_dir))
    repo_manager.add_list("Test List")
    assert repo_manager.rename_list("0", "Renamed List") is False
    assert repo_manager.rename_list("2", "Renamed List") is False


def test_repository_manager_delete_list(tmp_path):
    repo_dir = tmp_path / "test_repo"
    repo_manager = RepositoryManager(str(repo_dir))
    repo_manager.add_list("Test List")
    repo_manager.add_list("Test asdist")
    assert repo_manager.delete_list("1") is True


def test_repository_manager_delete_list_invalid_index(tmp_path):
    repo_dir = tmp_path / "test_repo"
    repo_manager = RepositoryManager(str(repo_dir))
    repo_manager.add_list("Test List")
    assert repo_manager.delete_list("0") is False
    assert repo_manager.delete_list("2") is False


def test_repository_manager_delete_list_empty_repository(tmp_path):
    repo_dir = tmp_path / "test_repo"
    repo_manager = RepositoryManager(str(repo_dir))
    assert repo_manager.delete_list("0") is False


def test_repository_manager_get_list(tmp_path):
    repo_dir = tmp_path / "test_repo"
    repo_manager = RepositoryManager(str(repo_dir))
    repo_manager.add_list("Test List")
    assert isinstance(repo_manager.get_list("1"), TodoManager)


def test_repository_manager_get_list_invalid_index(tmp_path):
    repo_dir = tmp_path / "test_repo"
    repo_manager = RepositoryManager(str(repo_dir))
    repo_manager.add_list("Test List")
    assert repo_manager.get_list("0") is None
    assert repo_manager.get_list("2") is None


# === Repository ===
def test_repository_repository_init(tmp_path):
    repo_dir = tmp_path / "test_repo"
    repo = Repository(repository=str(repo_dir), repository_name="test_repo")

    assert os.path.isdir(repo_dir) is False
    assert repo.repository == str(repo_dir)
    assert repo.files == []
    assert repo.todos == []


def test_repository_create_list(tmp_path):
    repo_dir = tmp_path / "test_repo"
    repo = Repository(repository=str(repo_dir), repository_name="test_repo")

    result = repo.create_list("shopping")

    assert result is True
    assert os.path.isdir(repo_dir) is True
    assert "shopping.csv" in repo.files
    assert repo.todos == ["shopping"]


def test_repository_files_property_with_existing_content(tmp_path):
    repo_dir = tmp_path / "test_repo"
    os.makedirs(repo_dir, exist_ok=True)

    repo = Repository(repository=str(repo_dir), repository_name="test_repo")

    repo.create_list("test1")
    repo.create_list("test2")

    assert sorted(repo.files) == ["test1.csv", "test2.csv"]
    assert sorted(repo.todos) == ["test1", "test2"]


def test_repository_create_list_with_existing_file(tmp_path):
    repo_dir = tmp_path / "test_repo"
    os.makedirs(repo_dir, exist_ok=True)

    repo = Repository(repository=str(repo_dir), repository_name="test_repo")
    repo.create_list("existing_list")

    with pytest.raises(FileExistsError):
        repo.create_list("existing_list")

    assert len(repo.files) == 1
    assert "existing_list.csv" in repo.files


def test_repository_delete_list(tmp_path):
    repo_dir = tmp_path / "test_repo"
    os.makedirs(repo_dir, exist_ok=True)

    repo = Repository(repository=str(repo_dir), repository_name="test_repo")
    repo.create_list("list1")
    repo.create_list("list2")
    result = repo.delete_list(0)

    assert result is True
    assert len(repo.files) == 1
    assert "list2.csv" in repo.files


def test_repository_delete_list_invalid_index(tmp_path):
    repo_dir = tmp_path / "test_repo"
    os.makedirs(repo_dir, exist_ok=True)

    repo = Repository(repository=str(repo_dir), repository_name="test_repo")
    repo.create_list("list1")
    repo.create_list("list2")
    result = repo.delete_list(5)

    assert result is False
    assert len(repo.files) == 2
    assert "list1.csv" in repo.files
    assert "list2.csv" in repo.files


def test_repository_delete_list_empty_repository(tmp_path):
    repo_dir = tmp_path / "test_repo"
    os.makedirs(repo_dir, exist_ok=True)

    repo = Repository(repository=str(repo_dir), repository_name="test_repo")
    result = repo.delete_list(0)

    assert result is False
    assert len(repo.files) == 0


def test_repository_rename_list(tmp_path):
    repo_dir = tmp_path / "test_repo"
    os.makedirs(repo_dir, exist_ok=True)

    repo = Repository(repository=str(repo_dir), repository_name="test_repo")
    repo.create_list("old_name")
    result = repo.rename_list(0, "new_name")

    assert result is True
    assert "new_name.csv" in repo.files
    assert "old_name.csv" not in repo.files


def test_repository_rename_list_invalid_index(tmp_path):
    repo_dir = tmp_path / "test_repo"
    os.makedirs(repo_dir, exist_ok=True)

    repo = Repository(repository=str(repo_dir), repository_name="test_repo")
    repo.create_list("list1")
    result = repo.rename_list(5, "new_name")

    assert result is False
    assert len(repo.files) == 1
    assert "list1.csv" in repo.files


def test_repository_rename_list_empty_repository(tmp_path):
    repo_dir = tmp_path / "test_repo"
    os.makedirs(repo_dir, exist_ok=True)

    repo = Repository(repository=str(repo_dir), repository_name="test_repo")
    result = repo.rename_list(0, "new_name")

    assert result is False
    assert len(repo.files) == 0


def test_repository_str_method(tmp_path):
    repo_dir = tmp_path / "test_repo"
    os.makedirs(repo_dir, exist_ok=True)

    repo = Repository(repository=str(repo_dir), repository_name="test_repo")
    repo.create_list("list1")
    repo.create_list("list2")

    expected_str = (
        "=== test_repo ===\n+----------+\n| 1. list1 |\n| 2. list2 |\n+----------+"
    )
    assert str(repo) == expected_str


# === TodoManager ===
def test_todo_manager_create_todo_manager(tmp_path):
    repo_dir = tmp_path / "test_repo"
    todo_manager = TodoManager(repository_path=str(repo_dir))
    assert todo_manager is not None
    assert todo_manager._todos is not None


def test_todo_manager_add_todo(tmp_path):
    repo_dir = tmp_path / "test_repo"
    todo_manager = TodoManager(repository_path=str(repo_dir))
    result = todo_manager.add_todo("Test Todo")
    assert result is True
    assert len(todo_manager._todos) == 1
    assert todo_manager._todos[0].title == "Test Todo"
    assert not todo_manager._todos[0].completed
    with pytest.raises(ValueError):
        todo_manager.add_todo("")


def test_todo_manager_delete_todo(tmp_path):
    repo_dir = tmp_path / "test_repo"
    todo_manager = TodoManager(repository_path=str(repo_dir))
    todo_manager.add_todo("Test Todo")
    result = todo_manager.delete_todo(0)
    assert result is True
    assert len(todo_manager._todos) == 0
    with pytest.raises(IndexError):
        todo_manager.delete_todo(0)


def test_todo_manager_rename_todo(tmp_path):
    repo_dir = tmp_path / "test_repo"
    todo_manager = TodoManager(repository_path=str(repo_dir))
    todo_manager.add_todo("Test Todo")
    result = todo_manager.rename_todo(0, "Renamed Todo")
    assert result is True
    assert todo_manager._todos[0].title == "Renamed Todo"
    # Renaming out of bounds todo
    assert todo_manager.rename_todo(1, "Another Todo") is False


def test_todo_manager_toggle_todo(tmp_path):
    repo_dir = tmp_path / "test_repo"
    todo_manager = TodoManager(repository_path=str(repo_dir))
    todo_manager.add_todo("Test Todo")
    result = todo_manager.toggle_todo(0)
    assert result is True
    assert todo_manager._todos[0].completed is True
    # Toggling out of bounds todo
    assert todo_manager.toggle_todo(1) is False


# === Todos ===
def test_todos_todos_init_with_default_list_name(tmp_path):
    repo_dir = tmp_path / "test_repo"
    todos = Todos(repository_path=str(repo_dir))
    assert todos.filepath == str(repo_dir / "todos.csv")
    assert todos._filename == "todos.csv"
    assert todos.list_name == "todos"
    assert os.path.exists(todos.filepath) is False
    assert os.path.exists(str(repo_dir / "todos.csv")) is False


def test_todos_todos_init_with_custom_list_name(tmp_path):
    repo_dir = tmp_path / "test_repo"
    todos = Todos(list_name="custom_todos", repository_path=str(repo_dir))
    assert todos._filename == "custom_todos.csv"
    assert todos.list_name == "custom_todos"
    assert todos.filepath == str(repo_dir / "custom_todos.csv")
    assert os.path.exists(todos.filepath) is False
    assert os.path.exists(str(repo_dir / "todos.csv")) is False


def test_todos_add_todo(tmp_path):
    repo_dir = tmp_path / "test_repo"
    todos = Todos(repository_path=str(repo_dir))
    todos.add(Todo("Test Todo"))
    assert len(todos._tasks) == 1
    assert todos._tasks[0].title == "Test Todo"
    assert todos._tasks[0].completed is False
    assert os.path.exists(todos.filepath) is True
    with open(todos.filepath, "r") as f:
        lines = f.readlines()
        assert len(lines) == 1
        assert lines[0].strip() == "Test Todo,False"


def test_todos_toggle_todo(tmp_path):
    repo_dir = tmp_path / "test_repo"
    todos = Todos(repository_path=str(repo_dir))
    todos.add(Todo("Test Todo"))
    todos.toggle(0)
    assert todos._tasks[0].completed is True
    with open(todos.filepath, "r") as f:
        lines = f.readlines()
        assert len(lines) == 1
        assert lines[0].strip() == "Test Todo,True"
    todos.toggle(0)
    assert todos._tasks[0].completed is False
    with open(todos.filepath, "r") as f:
        lines = f.readlines()
        assert len(lines) == 1
        assert lines[0].strip() == "Test Todo,False"
    with pytest.raises(IndexError):
        todos.toggle(1)


def test_todos_delete_todo(tmp_path):
    repo_dir = tmp_path / "test_repo"
    todos = Todos(repository_path=str(repo_dir))
    todos.add(Todo("Test Todo"))
    todos.delete(0)
    assert len(todos._tasks) == 0
    assert os.path.exists(todos.filepath) is True
    with open(todos.filepath, "r") as f:
        lines = f.readlines()
        assert len(lines) == 0
    with pytest.raises(IndexError):
        todos.delete(0)


def test_todos_rename_todo(tmp_path):
    repo_dir = tmp_path / "test_repo"
    todos = Todos(repository_path=str(repo_dir))
    todos.add(Todo("Test Todo"))
    todos.rename(0, "Renamed Todo")
    assert todos._tasks[0].title == "Renamed Todo"
    assert os.path.exists(todos.filepath) is True
    with open(todos.filepath, "r") as f:
        lines = f.readlines()
        assert len(lines) == 1
        assert lines[0].strip() == "Renamed Todo,False"
    with pytest.raises(IndexError):
        todos.rename(1, "Another Todo")


def test_todos_save_todos(tmp_path):
    repo_dir = tmp_path / "test_repo"
    todos = Todos(repository_path=str(repo_dir))
    todos.save()
    assert os.path.exists(todos.filepath) is True
    with open(todos.filepath, "r") as f:
        lines = f.readlines()
        assert len(lines) == 0


# === Todo ===
def test_todo_create_todo():
    todo = Todo("Test Todo")
    assert todo.title == "Test Todo"
    assert not todo.completed


def test_todo_toggle_todo():
    todo = Todo("Test Todo")
    assert not todo.completed
    todo.toggle()
    assert todo.completed
    todo.toggle()
    assert not todo.completed


def test_todo_todo_length():
    todo = Todo("Test Todo")
    assert len(todo) == len("Test Todo")
    todo.toggle()
    assert len(todo) == len("Test Todo")


def test_todo_todo_str():
    todo = Todo("Test Todo")
    assert str(todo) == "[ ] Test Todo"
    todo.toggle()
    assert str(todo) == "[x] Test Todo"
