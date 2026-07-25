from datetime import date, timedelta
from django.core.management.base import BaseCommand
from taskmanager.models import Task, SubTask


class Command(BaseCommand):
    help = "CRUD-операции для Task и SubTask"

    def handle(self, *args, **options):
        task, subtask1, subtask2 = self.create_records()
        self.read_records()
        self.update_records(task, subtask1, subtask2)
        self.delete_records(task)

    def create_records(self):
        today = date.today()
        task = Task.objects.create(
            title="Prepare presentation",
            description="Prepare materials and slides for the presentation",
            status="New",
            deadline=today + timedelta(days=3),
        )
        subtask1 = SubTask.objects.create(
            task=task,
            title="Gather information",
            description="Find necessary information for the presentation",
            status="New",
            deadline=today + timedelta(days=2),
        )
        subtask2 = SubTask.objects.create(
            task=task,
            title="Create slides",
            description="Create presentation slides",
            status="New",
            deadline=today + timedelta(days=1),
        )
        self.stdout.write(self.style.SUCCESS("Records created"))
        return task, subtask1, subtask2

    def read_records(self):
        new_tasks = Task.objects.filter(status="New")
        self.stdout.write(f"New tasks: {list(new_tasks)}")

        overdue_done = SubTask.objects.filter(status="Done", deadline__lt=date.today())
        self.stdout.write(f"Overdue done subtasks: {list(overdue_done)}")

    def update_records(self, task, subtask1, subtask2):
        task.status = "In progress"
        task.save()

        subtask1.deadline = date.today() - timedelta(days=2)
        subtask1.save()

        subtask2.description = "Create and format presentation slides"
        subtask2.save()

        self.stdout.write(self.style.SUCCESS("Records updated"))

    def delete_records(self, task):
        task.delete()
        self.stdout.write(self.style.SUCCESS("Task and subtasks deleted"))