from django.contrib import admin
from .models import Task, SubTask, Category
# Register your models here.

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'deadline')
    search_fields = ('title',)
    list_filter = ('status',)

@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'task' , 'status', 'deadline')
    search_fields = ('title',)
    list_filter = ('status',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)