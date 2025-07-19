from src.renderer import Renderer
from src.repository_manager import RepositoryManager
from src.arg_parser import ArgParser

BASE_DIR = "repositories"


def main():
    greet()

    repository = get_repository_name()

    initialize_repository(repository)


def get_repository_name():
    arg_parser = ArgParser(base_dir=BASE_DIR)
    repo_name = arg_parser.parse_args()

    return repo_name


def initialize_repository(repository):
    rm = RepositoryManager(base_dir=BASE_DIR, repository=repository)
    rm.load()


def greet():
    print(Renderer.box("WELCOME TO CLI TODO"))


if __name__ == "__main__":
    main()
