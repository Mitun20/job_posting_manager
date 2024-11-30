from django.conf import settings
from rest_framework import serializers
from applications.models import *
from .models import *  # Import your model if not already imported

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['department_name']  

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = ['role_name']  

class PostSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(required=False)
    class Meta:
        model = Posts
        fields = ['title', 'department', 'role', 'description', 'experience_from', 'experience_to', 'salary', 'close_date', 'posted_by', 'image', 'location']
        
    def get_image(self, obj):
        return f"{settings.SITE_URL}{obj.image.url}" if obj.image else None
    
class PostApplicationSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer()
    number_of_applicants = serializers.IntegerField()

    class Meta:
        model = Posts
        fields = ['id', 'title','department', 'role', 'description', 'number_of_applicants', 'is_active','posted_on']
        
class ApplicationSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    resume = serializers.SerializerMethodField()

    class Meta:
        model = Application
        fields = ['id', 'email', 'resume', 'name']

    def get_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    def get_resume(self, obj):
        return f"{settings.SITE_URL}{obj.cv_file.url}" if obj.cv_file else None
    
class Applicant_Profile_Serializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    resume = serializers.SerializerMethodField()
    status_choices = serializers.SerializerMethodField()
    class Meta:
        model = Application
        fields = ('name', 'email', 'phone', 'additional_info', 'resume', 'status','status_choices', 'post')

    def get_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    def get_resume(self, obj):
        return f"{settings.SITE_URL}{obj.cv_file.url}" if obj.cv_file else None
    
    def get_status_choices(self, obj):
        return [{'id': index + 1, 'value': choice[1]} for index, choice in enumerate(Application.STATUS_CHOICES)]
    
class SearchSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer()
    number_of_applicants = serializers.SerializerMethodField()

    class Meta:
        model = Posts
        fields = ['id', 'title','department', 'role', 'description', 'number_of_applicants','is_active','posted_on']

    def get_number_of_applicants(self, obj):
        return Application.objects.filter(post=obj).count()
