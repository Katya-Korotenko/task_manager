from django.contrib.auth.models import User
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Count
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError



from .models import Task, SubTask, Category
from .permissions import IsOwnerOrReadOnly
from .serializers import TaskSerializer, SubTaskSerializer, CategoryCreateSerializer, RegisterSerializer


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

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

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
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
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

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SubTaskDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubTask.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
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

class MyTasksView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]



class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user is None:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        response = Response({"detail": "Login successful"})
        response.set_cookie(key='access_token', value=access_token, httponly=True, path='/')
        response.set_cookie(key='refresh_token', value=refresh_token, httponly=True, path='/')
        return response




class RefreshTokenView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token is None:
            return Response({"detail": "Refresh token not found"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
        except TokenError:
            return Response({"detail": "Invalid or expired refresh token"}, status=status.HTTP_401_UNAUTHORIZED)

        response = Response({"detail": "Token refreshed"})
        response.set_cookie(key='access_token', value=access_token, httponly=True, path='/')
        return response



class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token is None:
            return Response({"detail": "Refresh token not found"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except TokenError:
            return Response({"detail": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

        response = Response({"detail": "Logout successful"})
        response.delete_cookie('access_token', path='/')
        response.delete_cookie('refresh_token', path='/')
        return response