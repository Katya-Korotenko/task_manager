from django.contrib import admin
from .models import Task, SubTask, Category
# Register your models here.

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'deadline')

@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'task' , 'status', 'deadline')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = ('name',)