from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Count
from rest_framework.permissions import IsAuthenticatedOrReadOnly


from .models import Task, SubTask, Category
from .serializers import TaskSerializer, SubTaskSerializer, CategoryCreateSerializer


class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']

    DAYS_MAPPING = {
        'monday': 2,
        'tuesday': 3,
        'wednesday': 4,
        'thursday': 5,
        'friday': 6,
        'saturday': 7,
        'sunday': 1,
    }

    def get_queryset(self):
        queryset = Task.objects.all()
        day = self.request.query_params.get('day')
        if day:
            day_number = self.DAYS_MAPPING.get(day.lower())
            if day_number:
                queryset = queryset.filter(deadline__week_day=day_number)
        return queryset

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = TaskSerializer

class TaskStatsView(APIView):

    def get(self,request):
        total_tasks = Task.objects.count()
        overdue_tasks = Task.objects.filter(deadline__lt = timezone.now()).count()
        status_counts = Task.objects.values('status').annotate(count=Count('id'))
        return Response({
            "total_tasks": total_tasks,
            "overdue_tasks": overdue_tasks,
            "status_counts": status_counts,
        })


class SubTaskListCreateView(generics.ListCreateAPIView):
    queryset = SubTask.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = SubTaskSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']


class SubTaskDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubTask.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = SubTaskSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CategoryCreateSerializer

    @action(detail=True, methods=['get'])
    def count_tasks(self, request, pk=None):
        category = self.get_object()
        count = category.tasks.count()
        return Response({'task_count': count})