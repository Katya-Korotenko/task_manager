from django.urls import path, include
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import TaskListCreateView, TaskDetailView, TaskStatsView, SubTaskListCreateView, SubTaskDetailUpdateDeleteView, CategoryViewSet


router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='category')


urlpatterns = [
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/detail/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('tasks/stats/', TaskStatsView.as_view(), name='task-stats'),
    path('subtask/list/', SubTaskListCreateView.as_view(), name='subtask-list'),

    path('subtask/<int:pk>/', SubTaskDetailUpdateDeleteView.as_view(), name='subtask-detail-update-delete'),
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]