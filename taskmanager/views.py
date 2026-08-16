from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from rest_framework import status
from django.db.models import Count
from django.shortcuts import get_object_or_404


from .models import Task, SubTask
from .serializers import TaskSerializer, SubTaskSerializer
from .pagination import SubTaskPagination

class TaskCreateView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskListView(generics.ListAPIView):
    serializer_class = TaskSerializer

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

class TaskDetailView(generics.RetrieveAPIView):
    queryset = Task.objects.all()
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


class SubTaskListCreateView(APIView):

    def get(self, request):
        subtasks = SubTask.objects.all()

        task_title = request.query_params.get('task')
        if task_title:
            subtasks = subtasks.filter(task__title=task_title)

        status_filter = request.query_params.get('status')
        if status_filter:
            subtasks = subtasks.filter(status=status_filter)

        paginator = SubTaskPagination()
        page = paginator.paginate_queryset(subtasks, request)
        serializer = SubTaskSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


    def post(self, request):
        serializer = SubTaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SubTaskDetailUpdateDeleteView(APIView):

    def delete(self, request, subtask_id):
        subtask = get_object_or_404(SubTask, pk=subtask_id)
        subtask.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self,request, subtask_id):
        subtask = get_object_or_404(SubTask, pk=subtask_id)
        serializer = SubTaskSerializer(instance=subtask, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self,request, subtask_id):
        subtask = get_object_or_404(SubTask, pk=subtask_id)
        serializer = SubTaskSerializer(subtask)
        return Response(serializer.data)

