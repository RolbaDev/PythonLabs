import os
import json
import sys
from termcolor import colored
import argparse
from datetime import datetime
from Task import Task


class Manager:

    STATUS_OPTIONS = {"1": "Started", "2": "Paused", "3": "Completed"}
    TTL = 7

    def __init__(self):
        self.current_list = "default.json"
        self.tasks = self.load_tasks()

    def create_new_list(self, name):
        self.current_list = f"{name}.json"
        self.tasks = []
        self.save_tasks()
        print(colored(f"✅ Created new list: {name}", "green"))

    def set_current_list(self, list_name):
        filename = f"{list_name}.json"
        if os.path.exists(filename):
            self.current_list = filename
            self.tasks = self.load_tasks()
            print(colored(f"List: {list_name}", "green"))
        else:
            print(colored(f"List '{list_name}' does not exist.", "red"))

    def list_available_lists(self):
        files = [f[:-5] for f in os.listdir() if f.endswith(".json")]
        if not files:
            print(colored("❌ No available task lists.", "red"))
        else:
            print(colored("📋 Available task lists:", "cyan"))
            for file in files:
                print(f"- {file}")

    def load_tasks(self):
        if os.path.exists(self.current_list):
            with open(self.current_list, "r") as file:
                return [Task.from_dict(task) for task in json.load(file)]
        return []

    def save_tasks(self):
        with open(self.current_list, "w") as file:
            json.dump([task.to_dict() for task in self.tasks], file, indent=4)

    def add_task(self, name, description, list_name=None):
        if list_name:
            if not os.path.exists(f"{list_name}.json"):
                print(
                    colored(
                        f"❌ List '{list_name}' does not exist. Task was not added.",
                        "red",
                    )
                )
                return
            self.set_current_list(list_name)

        if not name or not description:
            print(colored("❌ Task name and description are required!", "orange"))
            return

        self.tasks.append(Task(name, description))
        self.save_tasks()
        print(colored("✅ Task added.", "green"))

    def list_tasks(self, status_filter=None, list_name=None):
        if list_name:
            filename = f"{list_name}.json"
            if not os.path.exists(filename):
                print(colored(f"❌ List '{list_name}' does not exist.", "red"))
                return
            self.set_current_list(list_name)

        if not self.tasks:
            print(colored("❌ No available tasks.", "red"))
            return

        today = datetime.today()
        recent_tasks = [
            (index, task)
            for index, task in enumerate(self.tasks, start=1)
            if task.created_at is None or (today - task.created_at).days <= self.TTL
        ]

        print(colored(f"📋 List: ({self.current_list}):\n", "cyan"))

        if recent_tasks:
            print(colored("✅ Active tasks:", "green"))
            for i, (index, task) in enumerate(recent_tasks, 1):
                task_str = colored(
                    f"[{index}] - {task.name} - {task.description} - Status: ({task.status})",
                    self.get_status_color(task.status),
                )
                print(task_str)
        else:
            print(colored("❌ No active tasks.", "red"))

    def get_status_color(self, status):
        return {"Started": "yellow", "Paused": "red", "Completed": "green"}.get(
            status, "white"
        )

    def update_task(self, task_id, status_id, list_name=None):
        try:
            task = self.tasks[task_id - 1]
            status = self.STATUS_OPTIONS.get(str(status_id))

            if status:
                task.status = status
                self.save_tasks()
                print(colored(f"'{task.name}' Status: {task.status}", "yellow"))
            else:
                print(
                    colored(
                        "❌ Invalid status! Available statuses: 1 - Started, 2 - Paused, 3 - Completed",
                        "red",
                    )
                )
        except IndexError:
            print(colored("❌ Task with the given ID not found!", "red"))

    def remove_task(self, task_id, list_name=None):
        if not self.tasks:
            print(colored("❌ No tasks available to remove.", "red"))
            return
        try:
            task_id = int(task_id) - 1
            if 0 <= task_id < len(self.tasks):
                deleted_task = self.tasks.pop(task_id)
                self.save_tasks()
                print(
                    colored(f"✅ Task '{deleted_task.name}' has been removed.", "green")
                )
            else:
                print(colored("❌ Invalid task number.", "red"))
        except ValueError:
            print(colored("❌ Task ID must be a number!", "red"))

    def delete_list(self, name):
        filename = f"{name}.json"
        if os.path.exists(filename):
            os.remove(filename)
            print(colored(f"✅ List '{name}' has been deleted.", "green"))
            if self.current_list == filename:
                self.current_list = "default.json"
                self.tasks = self.load_tasks()
                print(colored("📋 Switched to the default task list.", "yellow"))
        else:
            print(colored(f"❌ List '{name}' does not exist.", "red"))

    # Handles commands from argparse
    def handle_command(self, args):
        parser = argparse.ArgumentParser(
            description="Task Manager", formatter_class=argparse.RawTextHelpFormatter
        )
        subparsers = parser.add_subparsers(dest="command")

        # Add task
        add_parser = subparsers.add_parser("add_task", help="Add a task")
        add_parser.add_argument("name", type=str, help="Task name")
        add_parser.add_argument("description", type=str, help="Task description")
        add_parser.add_argument("--list", type=str, help="List name")
        add_parser.epilog = 'Example: python Manager.py add_task "Task 1" "Task description" --list "mylist"'

        # List tasks
        list_parser = subparsers.add_parser("list_tasks", help="List tasks")
        list_parser.add_argument(
            "--status",
            type=int,
            choices=[1, 2, 3],
            help="Filter tasks by status (1-Started, 2-Paused, 3-Completed)",
        )
        list_parser.add_argument("--list", type=str, help="List name")
        list_parser.epilog = (
            'Example: python Manager.py list_tasks --status 1 --list "mylist"'
        )

        # Update task status
        update_parser = subparsers.add_parser(
            "update_status", help="Update task status"
        )
        update_parser.add_argument("task_id", type=int, help="Task ID")
        update_parser.add_argument(
            "status",
            type=int,
            choices=[1, 2, 3],
            help="New status (1-Started, 2-Paused, 3-Completed)",
        )
        update_parser.add_argument("--list", type=str, help="List name")
        update_parser.epilog = (
            'Example: python Manager.py update_status 2 1 --list "mylist"'
        )

        # Remove task
        remove_parser = subparsers.add_parser("remove_task", help="Remove a task")
        remove_parser.add_argument("task_id", type=int, help="Task ID to remove")
        remove_parser.add_argument("--list", type=str, help="List name")
        remove_parser.epilog = (
            'Example: python Manager.py remove_task 3 --list "mylist"'
        )

        # Delete list
        delete_list_parser = subparsers.add_parser(
            "delete_list", help="Delete a task list"
        )
        delete_list_parser.add_argument("name", type=str, help="List name")
        delete_list_parser.epilog = 'Example: python Manager.py delete_list "mylist"'

        # Create new list
        new_list_parser = subparsers.add_parser("add_list", help="Create a new list")
        new_list_parser.add_argument("name", type=str, help="New list name")
        new_list_parser.epilog = 'Example: python Manager.py add_list "newlist"'

        # List available lists
        list_lists_parser = subparsers.add_parser(
            "lists", help="List all available task lists"
        )
        list_lists_parser.epilog = "Example: python Manager.py lists"

        parsed_args = parser.parse_args(args)

        # Commands
        if parsed_args.command == "add_task":
            self.add_task(parsed_args.name, parsed_args.description, parsed_args.list)
        elif parsed_args.command == "list_tasks":
            self.list_tasks(parsed_args.status, parsed_args.list)
        elif parsed_args.command == "update_status":
            self.update_task(parsed_args.task_id, parsed_args.status, parsed_args.list)
        elif parsed_args.command == "remove_task":
            self.remove_task(parsed_args.task_id, parsed_args.list)
        elif parsed_args.command == "delete_list":
            self.delete_list(parsed_args.name)
        elif parsed_args.command == "add_list":
            self.create_new_list(parsed_args.name)
        elif parsed_args.command == "lists":
            self.list_available_lists()


def main():
    manager = Manager()

    manager.handle_command(sys.argv[1:])


if __name__ == "__main__":
    main()
