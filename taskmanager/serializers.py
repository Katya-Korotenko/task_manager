from rest_framework import serializers
from django.utils import timezone
from .models import Task, SubTask, Category


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'owner', 'status', 'deadline']
        read_only_fields = ['owner']

class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'deadline']

    def validate_deadline(self, value):

        if value < timezone.now():
            raise serializers.ValidationError("Deadline cannot be less than now")
        return value


class SubTaskSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = SubTask
        fields = ['id', 'title', 'description', 'owner', 'task', 'status', 'deadline', 'created_at']
        read_only_fields = ['owner']

class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

    def create(self, validated_data):
        if Category.objects.filter(name=validated_data['name']).exists():
            raise serializers.ValidationError("Category already exists")
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        name = validated_data.get('name', instance.name)
        if Category.objects.filter(name=name).exclude(id=instance.id).exists():
            raise serializers.ValidationError("Category already exists")
        instance.name = name
        instance.save()
        return instance


class TaskDetailSerializer(serializers.ModelSerializer):
    subtasks = SubTaskSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'owner', 'description', 'status', 'deadline', 'created_at', 'subtasks']
        read_only_fields = ['owner']