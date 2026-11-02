
import json
from pathlib import Path


TASKS_FILE = Path(__file__).with_name("tasks.json")


def load_tasks():
	try:
		with TASKS_FILE.open("r", encoding="utf-8") as file:
			tasks = json.load(file)
		if not isinstance(tasks, list):
			raise ValueError
		return tasks
	except FileNotFoundError:
		return []
	except (json.JSONDecodeError, OSError, ValueError):
		print("Unable to read the tasks file. Starting with an empty task list.")
		return []


def save_tasks(tasks):
	try:
		with TASKS_FILE.open("w", encoding="utf-8") as file:
			json.dump(tasks, file, indent=2)
	except OSError:
		print("Unable to save tasks.")


def list_tasks(tasks):
	if not tasks:
		print("No tasks found.")
		return

	for number, task in enumerate(tasks, 1):
		status = "Done" if task["complete"] else "Pending"
		print(f"{number}. [{status}] {task['title']}")


def add_task(tasks):
	title = input("Enter a task: ").strip()
	if not title:
		print("Task cannot be empty.")
		return

	tasks.append({"title": title, "complete": False})
	save_tasks(tasks)
	print("Task added.")


def complete_task(tasks):
	if not tasks:
		print("No tasks found.")
		return

	list_tasks(tasks)
	value = input("Enter the task number to mark complete: ").strip()
	if not value.isdigit():
		print("Please enter a valid task number.")
		return

	index = int(value) - 1
	if index < 0 or index >= len(tasks):
		print("That task number does not exist.")
		return

	tasks[index]["complete"] = True
	save_tasks(tasks)
	print("Task marked complete.")


def main():
	tasks = load_tasks()

	while True:
		print("\nTask Tracker")
		print("1. Add task")
		print("2. List tasks")
		print("3. Mark task complete")
		print("4. Exit")

		choice = input("Choose an option: ").strip()
		if choice == "1":
			add_task(tasks)
		elif choice == "2":
			list_tasks(tasks)
		elif choice == "3":
			complete_task(tasks)
		elif choice == "4":
			save_tasks(tasks)
			print("Goodbye!")
			break
		else:
			print("Please choose a number from 1 to 4.")


if __name__ == "__main__":
	main()
