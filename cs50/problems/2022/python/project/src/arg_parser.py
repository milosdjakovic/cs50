import os
import sys
import argparse
import shutil
from src.renderer import Renderer


class ArgParser:
    def __init__(self, base_dir="repositories"):
        self.base_dir = base_dir
        self.parser = argparse.ArgumentParser(description="Todo List Application")
        self.parser.add_argument(
            "repository",
            nargs="?",
            default=None,
            help='"name of the repo" or repo-name - Repository to use',
        )
        self.parser.add_argument(
            "-l", "--list", action="store_true", help="List available repositories"
        )
        self.parser.add_argument(
            "-c", "--create", action="store_true", help="Create a new repository"
        )
        self.parser.add_argument(
            "-d", "--delete", action="store_true", help="Delete an existing repository"
        )

    def parse_args(self, args=None):
        """
        Parse command-line arguments and return a valid repository name or exit

        Args:
            args: List of command line arguments (for testing purposes)

        Returns:
            str: Repository name if valid
        """
        parsed_args = self.parser.parse_args(args)

        if parsed_args.list:
            self.list_repositories()
            sys.exit(0)

        if not parsed_args.repository:
            self.parser.print_help()
            sys.exit(0)

        if parsed_args.delete:
            self.delete_repository(parsed_args.repository)
            sys.exit(0)

        if parsed_args.create:
            return self.create_repository(parsed_args.repository)

        repo_path = os.path.join(self.base_dir, parsed_args.repository)
        if not os.path.exists(repo_path):
            print(
                Renderer.box(
                    f"Error: Repository '{parsed_args.repository}' doesn't exist."
                )
            )
            self.list_repositories()
            sys.exit(1)

        return parsed_args.repository

    def list_repositories(self):
        """
        List all available repositories in the base directory
        """
        if not os.path.exists(self.base_dir):
            print(
                Renderer.box(
                    "No repositories found.\nUse --create or -c flag to create a new repository."
                )
            )
            return

        repos = []
        for item in os.listdir(self.base_dir):
            item_path = os.path.join(self.base_dir, item)
            if os.path.isdir(item_path):
                repos.append(item)

        if not repos:
            print(
                Renderer.box(
                    "No repositories found.\nUse --create or -c flag to create a new repository."
                )
            )
        else:
            print(Renderer.title("Available repositories:"))
            repos_string = ""
            for repo in repos:
                repos_string += f"- {repo}"
                if repo != repos[-1]:
                    repos_string += "\n"
            print(Renderer.box(repos_string))

    def create_repository(self, repo_name):
        """
        Create a repository with the given name

        Args:
            repo_name: Name of the repository

        Returns:
            str: Repository name
        """
        repo_path = os.path.join(self.base_dir, repo_name)

        if os.path.exists(repo_path):
            print(Renderer.box(f"Repository '{repo_name}' already exists."))
            return repo_name

        try:
            os.makedirs(repo_path)
            print(Renderer.box(f"Created new repository: {repo_name}"))
            return repo_name
        except OSError as e:
            print(Renderer.box(f"Error creating repository '{repo_name}': {e}"))
            sys.exit(1)

    def delete_repository(self, repo_name):
        """
        Delete a repository with the given name

        Args:
            repo_name: Name of the repository to delete
        """
        repo_path = os.path.join(self.base_dir, repo_name)

        if not os.path.exists(repo_path):
            print(Renderer.box(f"Error: Repository '{repo_name}' doesn't exist."))
            self.list_repositories()
            return

        try:
            shutil.rmtree(repo_path)
            print(Renderer.box(f"Repository '{repo_name}' has been deleted."))
            self.list_repositories()
        except OSError as e:
            print(Renderer.box(f"Error deleting repository '{repo_name}': {e}"))
            sys.exit(1)
