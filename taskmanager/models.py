from django.db import models

class Status(models.TextChoices):
    NEW = 'new', 'New'
    IN_PROGRESS = 'in progress', 'In progress'
    PENDING = 'pending', 'Pending'
    BLOCKED = 'blocked', 'Blocked'
    DONE = 'done', 'Done'

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'task_manager_category'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    categories = models.ManyToManyField(Category, related_name='tasks', blank=True)
    status = models.CharField(max_length=100, choices=Status.choices, default=Status.NEW)
    deadline = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'task_manager_task'
        ordering = ['-created_at']
        verbose_name = 'Task'
        constraints = [models.UniqueConstraint(fields=['title', 'deadline'], name='unique_title_deadline')]



class SubTask(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')
    status = models.CharField(max_length=100, choices=Status.choices, default=Status.NEW)
    deadline = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'task_manager_subtask'
        verbose_name = 'SubTask'
        ordering = ['-created_at']

