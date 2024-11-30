from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.response import Response
from .models import *
from account.models import *
from .serializers import *
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.shortcuts import get_object_or_404


# -----------------------------------------------------------------listing the posts for apply
class List_of_posts(APIView):
    def get(self, request):
        try:
            post = Posts.objects.all()
            serializer = ListPostSerializer(post, many=True).data
            return Response(serializer, status=status.HTTP_200_OK)
        except Posts.DoesNotExist:
            return Response({"message": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
        
        
#-------------------------------------------------------------------detail view of post 

class Detail_view_post(APIView):
    def get(self, request, post_id):
        try:
            post = Posts.objects.get(id=post_id)
            serializer = Detail_Post_Serializer(post).data
            return Response(serializer, status=status.HTTP_200_OK)
        except Posts.DoesNotExist:
            return Response({"message": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

# ---------------------------------------------------------------------Apply job
class Apply_Job(APIView):
    def post(self, request):
        serializer = ApplicationSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                post = Posts.objects.get(id=serializer.validated_data['post'].id)
            except Posts.DoesNotExist:
                return Response({"error": "Job posting does not exist"}, status=status.HTTP_400_BAD_REQUEST)

            # Save the application
            application = serializer.save()

            # Generate a verification token
            verification_token = get_random_string(6)

            # Send a verification email
            verification_url = f"{settings.FRONTEND_URL}/{settings.TEMPLATE_NAME}?"
            send_mail(
                'Verify your email address',
                f'Varification Code = {verification_token}',
                settings.DEFAULT_FROM_EMAIL,
                [application.email],
                fail_silently=False,
            )

            # Save the verification token (this would be in a separate model typically)
            application.verification_token = verification_token
            application.save()

            return Response({"message": "Application submitted, Kindly verify your email in order to accept your CV submission.","verification_code":verification_token}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class AdvancedSearchAPIView(APIView):
    def post(self, request, *args, **kwargs):  # Method name should be lowercase
        title = request.data.get('title', None)
        role_name = request.data.get('role', None)
        department_name = request.data.get('department', None)

        # Create a dictionary for the filter arguments
        filters = {}

        if title:
            filters['title__icontains'] = title
        if role_name:
            filters['role_name__icontains'] = role_name
        if department_name:
            filters['department__department_name__icontains'] = department_name

        # Apply the filters in a single query
        queryset = Posts.objects.filter(**filters)

        serializer = ListPostSerializer(queryset, many=True)
        
        # Correctly access nested fields if necessary
        formatted_data = [
            {
                "job_posting_id": item['id'],
                "job_title": item['title'],
                "department": item['department']['department_name'],  # Ensure this is correctly serialized
                "role": item['role_name'],  # Ensure this is correctly serialized
                "posted_on": item['posted_on'],
                "close_date": item['close_date'],
                "location": item['location'],
               
            }
            for item in serializer.data
        ]
        return Response(formatted_data, status=status.HTTP_200_OK)
