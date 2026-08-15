from django.urls import path
from .views import TaskCreateView, TaskListView, TaskDetailView, TaskStatsView, SubTaskListCreateView, SubTaskDetailUpdateDeleteView

urlpatterns = [
    path('tasks/create/', TaskCreateView.as_view(), name='task-create'),
    path('tasks/list/', TaskListView.as_view(), name='task-list'),
    path('tasks/detail/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('tasks/stats/', TaskStatsView.as_view(), name='task-stats'),
    path('subtask/list/', SubTaskListCreateView.as_view(), name='subtask-list'),

    path('subtask/<int:subtask_id>/', SubTaskDetailUpdateDeleteView.as_view(), name='subtask-detail-update-delete'),
]