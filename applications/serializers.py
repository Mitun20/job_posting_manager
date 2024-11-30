from django.conf import settings
from rest_framework import serializers
from account.models import *
from .models import Application

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['department_name']  

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = ['role_name']  


class ListPostSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer()
    # role = RoleSerializer()
    class Meta:
        model = Posts
        fields = ['id', 'title','department', 'role', 'posted_on', 'close_date', 'location']




class Detail_Post_Serializer(serializers.ModelSerializer):
    department = DepartmentSerializer()
    # role = RoleSerializer()
    image = serializers.SerializerMethodField()
    class Meta:
        model = Posts
        fields = ['title', 'department', 'role', 'description', 'experience_from', 'experience_to', 'salary','posted_on', 'close_date', 'image', 'location']

    def get_image(self, obj):
        return f"{settings.SITE_URL}{obj.image.url}" if obj.image else None


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ('first_name', 'last_name', 'email', 'phone', 'additional_info', 'cv_file', 'status', 'post')
        
    # Override to set the status to 'Applied' on creation
    def create(self, validated_data):
        validated_data['status'] = 'Applied'
        return super().create(validated_data) 