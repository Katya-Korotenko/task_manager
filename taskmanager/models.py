from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Status(models.TextChoices):
    NEW = 'new', 'New'
    IN_PROGRESS = 'in progress', 'In progress'
    PENDING = 'pending', 'Pending'
    BLOCKED = 'blocked', 'Blocked'
    DONE = 'done', 'Done'

class CategoryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

class Category(models.Model):

    objects = CategoryManager()
    name = models.CharField(max_length=100, unique=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'task_manager_category'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

class Task(models.Model):

    owner = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='tasks_owned')
    title = models.CharField(max_length=100)
    description = models.TextField()
    categories = models.ManyToManyField(Category, related_name='tasks', blank=True)
    status = models.CharField(max_length=100, choices=Status.choices, default=Status.NEW)
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'task_manager_task'
        ordering = ['-created_at']
        verbose_name = 'Task'
        constraints = [models.UniqueConstraint(fields=['title', 'deadline'], name='unique_title_deadline')]



class SubTask(models.Model):

    owner = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='subtasks_owned')
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')
    status = models.CharField(max_length=100, choices=Status.choices, default=Status.NEW)
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'task_manager_subtask'
        verbose_name = 'SubTask'
        ordering = ['-created_at']

