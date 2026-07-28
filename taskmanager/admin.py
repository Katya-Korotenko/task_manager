from django.contrib import admin
from .models import Task, SubTask, Category, Status

class SubTaskInline(admin.TabularInline):
    model = SubTask
    extra = 1

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('short_title', 'status', 'deadline')
    search_fields = ('title',)
    list_filter = ('status',)
    inlines = [SubTaskInline]

    def short_title(self, obj):
        if len(obj.title) > 10:
            return obj.title[:10] + "..."
        return obj.title
    short_title.short_description = "Title"


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'task' , 'status', 'deadline')
    search_fields = ('title',)
    list_filter = ('status',)
    actions = ['mark_as_done']

    def mark_as_done(self, request, queryset):
        queryset.update(status=Status.DONE)

    mark_as_done.short_description = "Mark selected subtasks as Done"

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)