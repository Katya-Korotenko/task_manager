
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Count


from .models import Task
from .serializers import TaskSerializer

class TaskCreateView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskListView(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class TaskDetailView(generics.RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class TaskStatsView(APIView):
    def get(self, request):
        total_tasks = Task.objects.count()
        overdue_tasks = Task.objects.filter(deadline__lt = timezone.now()).count()
        status_counts = Task.objects.values('status').annotate(count=Count('id'))
        return Response({
            "total_tasks": total_tasks,
            "overdue_tasks": overdue_tasks,
            "status_counts": status_counts,
        })