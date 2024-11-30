from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Count
from django.utils.crypto import get_random_string
from .models import *
from .serializers import *
from applications.models import *
from django.shortcuts import get_object_or_404
from django.http import  HttpResponse
from django.db.models import Q
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import generics

class Login(APIView):
    def post(self, request):
        print("top--",request.data)
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        print("bottom",username, password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            
            return Response({
                'refresh': refresh_token,
                'access': access_token,
                'username': username,
                "id":user.id
            }, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class ForgetPassword(APIView):
    def post(self, request):
        username = request.data.get('username')
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        new_password = get_random_string(length=8)
        user.set_password(new_password)
        user.save()

        send_mail(
            'Your Password has reset',
            f'Your new password is: {new_password}. Make your password with more secure',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

        return Response({'message': 'Password reset token has been sent to your email'})


class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        old_password = request.data.get('oldPassword')
        new_password = request.data.get('newPassword')

        if not user.check_password(old_password):
            return Response({'error': 'Old password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        return Response({
            'message': 'Password has been successfully changed',
            'refresh': refresh_token,
            'access': access_token,
        })
        
    
#---------------------------------------------------------------------- Manage Department

class CreateDepartment(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        department = Department(
            department_name=request.data['department_name'],
            description=request.data['description'],
            is_active= True
        )
        department.save()

        return Response({"message": "Department created successfully"}, status=status.HTTP_201_CREATED)

class RetrieveDepartments(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        departments = Department.objects.all()
        data = [
            {
                "departmentId": department.id,
                "departmentName": department.department_name,
                "description": department.description,
                "is_active": department.is_active,
            }
            for department in departments
        ]
        return Response(data, status=status.HTTP_200_OK)
    
class UpdateDepartment(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, department_id):
        try:
            department = Department.objects.get(id=department_id)
            data = {
                "departmentName": department.department_name,
                "description": department.description,
            }
            return Response(data, status=status.HTTP_200_OK)
        except Department.DoesNotExist:
            return Response({"message": "Department not found"}, status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request, department_id):
        try:
            department = Department.objects.filter(id=department_id)
        except Department.DoesNotExist:
            return Response({"message": "Department not found"}, status=status.HTTP_404_NOT_FOUND)
        department.update(
        department_name = request.data["department_name"],
        description = request.data["description"],
        )

        return Response({"message": "Department updated successfully"}, status=status.HTTP_200_OK)
    
    
class InactiveDepartment(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, department_id):
        
        if department_id is None:
            return Response({"message": "Department ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            department = Department.objects.get(id=department_id)
            department.is_active = request.data.get('is_active')

            department.save()
            return Response({"message": "Department status has been updated successfully"}, status=status.HTTP_200_OK)
        except Department.DoesNotExist:
            return Response({"message": "Department not found"}, status=status.HTTP_404_NOT_FOUND)
        
#---------------------------------------------------------------------- Manage roles

class CreateRole(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        roles = Roles(
            role_name=request.data['role_name'],
            is_active=True,
        )
        roles.save()

        return Response({"message": "Roles created successfully"}, status=status.HTTP_201_CREATED)

class RetrieveRoles(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        roles = Roles.objects.all()
        data = [
            {
                "roleId": role.id,
                "role_name": role.role_name,
                "is_active": role.is_active,
            }
            for role in roles
        ]
        return Response(data, status=status.HTTP_200_OK)
    
class UpdateRole(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, role_id):
        try:
            role = Roles.objects.get(id=role_id)
            data = {
                "role_name": role.role_name,
            }
            return Response(data, status=status.HTTP_200_OK)
        except Roles.DoesNotExist:
            return Response({"message": "Role not found"}, status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request, role_id):
        try:
            role = Roles.objects.filter(id=role_id)
        except Roles.DoesNotExist:
            return Response({"message": "Rolet not found"}, status=status.HTTP_404_NOT_FOUND)
        role.update(
        role_name = request.data["role_name"],
        )

        return Response({"message": "Role updated successfully"}, status=status.HTTP_200_OK)
    
class InactiveRole(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, role_id):
        
        if role_id is None:
            return Response({"message": "Role ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            role = Roles.objects.get(id=role_id)
            role.is_active = request.data.get('is_active')
            role.save()
            return Response({"message": "Role status has been updated successfully"}, status=status.HTTP_200_OK)
        except Roles.DoesNotExist:
            return Response({"message": "Role not found"}, status=status.HTTP_404_NOT_FOUND)


#--------------------------------------------------------------------- Manage Posts


class JobPostingsListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
            posts = Posts.objects.all().annotate(
                number_of_applicants=Count('application')
            )
            serializer = PostApplicationSerializer(posts, many=True)
            return Response(serializer.data)

class get_department(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        departments = Department.objects.filter(is_active=True)
        
        data = [
            {
                "departmentId": department.id,
                "departmentName": department.department_name,
                "description": department.description,
                "is_active": department.is_active,
            }
            for department in departments
        ]
        
        return Response(data, status=status.HTTP_200_OK)
    
class get_role(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        roles = Roles.objects.filter(is_active=True)
        data = [
            {
                "roleId": role.id,
                "role_name": role.role_name,
                "is_active": role.is_active,
            }
            for role in roles
        ]
        return Response(data, status=status.HTTP_200_OK)
    

class CreatePosts(APIView):
    permission_classes = [IsAuthenticated]
    # parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        image = request.FILES.get('image')
        
        post = Posts(
            title=request.data.get('title'),
            department_id=request.data.get('department'),
            role=request.data.get('role'),
            description=request.data.get('description'),
            experience_from=request.data.get('experience_from'),
            experience_to=request.data.get('experience_to'),
            salary=request.data.get('salary'),
            close_date=request.data.get('close_date',None),
            posted_by=request.user,
            location=request.data.get('location'),
            image=image if image else None
        )
        post.save()
        return Response({"message": "Job posted successfully"}, status=status.HTTP_201_CREATED)

class UpdatePosts(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, post_id):
        try:
            post = Posts.objects.get(id=post_id)
            serializer = PostSerializer(post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Posts.DoesNotExist:
            return Response({"message": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, post_id):
        try:
            post = Posts.objects.get(id=post_id)
        except Posts.DoesNotExist:
            return Response({"message": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

        # Extract the image and other fields from the request
        image = request.FILES.get('image')
        
        # Update the post fields
        post.title = request.data.get('title', post.title)
        post.department_id = request.data.get('department', post.department_id)
        post.role = request.data.get('role', post.role)
        post.description = request.data.get('description', post.description)
        post.experience_from = request.data.get('experience_from', post.experience_from)
        post.experience_to = request.data.get('experience_to', post.experience_to)
        post.salary = request.data.get('salary', post.salary)
        post.close_date = request.data.get('close_date', post.close_date)
        post.location = request.data.get('location', post.location)
        
        if image:
            post.image = image

        post.save()
        return Response({"message": "Post updated successfully"}, status=status.HTTP_200_OK)




class InactivePosts(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, post_id):
        
        if post_id is None:
            return Response({"message": "Post ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            post = Posts.objects.get(id=post_id)
            post.is_active = request.data.get('is_active')
            post.save()
            return Response({"message": "Post status has been updated successfully"}, status=status.HTTP_200_OK)
        except Roles.DoesNotExist:
            return Response({"message": "Post not found"}, status=status.HTTP_404_NOT_FOUND)



#-------------------------------------------------------------- listing the Application for specific post
        
class ListApplication(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, post_id):
        try:
            applications = Application.objects.filter(post_id=post_id)
        except Application.DoesNotExist:
            return Response({"error": "No applicants found for the given job posting"}, status=404)
        
        serializer = ApplicationSerializer(applications, many=True)
        return Response(serializer.data)
    
    
# ---------------------------------------------------------------detail profile of applicants

class Applicant_Profile(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, applicant_id):
        try:
            applicant = Application.objects.get(id=applicant_id)
            serializer = Applicant_Profile_Serializer(applicant).data
            return Response(serializer, status=status.HTTP_200_OK)
        except Application.DoesNotExist:
            return Response({"message": "Application not found"}, status=status.HTTP_404_NOT_FOUND)
        
    def post(self, request,applicant_id):
        subject = request.data.get('subject')
        message = request.data.get('message')
        try:
            applicant = Application.objects.get(id=applicant_id)
        except User.DoesNotExist:
            return Response({'error': 'Applicant does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [applicant.email],
            fail_silently=False,
        )
        return Response({'message': 'Email sent successfully'})
    
    def patch(self, request, applicant_id):
        try:
            applicant = Application.objects.get(id=applicant_id)
        except Application.DoesNotExist:
            return Response({"message": "Application not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Check for valid status value
        new_status = request.data.get('status')
        if new_status not in dict(Application.STATUS_CHOICES).keys():
            return Response({"message": "Invalid status value"}, status=status.HTTP_400_BAD_REQUEST)

        # Update status and save
        applicant.status = new_status
        applicant.save()
        
        serializer = Applicant_Profile_Serializer(applicant)
        return Response({"message": "status value Updated"}, status=status.HTTP_200_OK)


class Download_Resume(APIView):
    def get(self, request, applicant_id):
        application = get_object_or_404(Application, id=applicant_id)
        response = HttpResponse(application.cv_file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{application.cv_file.name}"'
        
        return response


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

        serializer = SearchSerializer(queryset, many=True)
        
        # Correctly access nested fields if necessary
        formatted_data = [
            {
                "id": item['id'],
                "title": item['title'],
                "department": item['department']['department_name'],  # Ensure this is correctly serialized
                "role": item['role_name'],  # Ensure this is correctly serialized
                "number_of_applicants": item['number_of_applicants'],
                "is_active": item['is_active'],
            }
            for item in serializer.data
        ]
        return Response(formatted_data, status=status.HTTP_200_OK)
    
    
# -----------------------------------------------------filter by date, title, department and role
class PostFilterView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        # Extract data from the JSON body
        title = request.data.get('title', None)
        department_name = request.data.get('department', None)
        role = request.data.get('role', None)
        date = request.data.get('date', None)

        # Create a dictionary for the filter arguments
        filters = Q()
        if title:
            filters &= Q(title__icontains=title)
        if department_name:
            filters &= Q(department__department_name__icontains=department_name)
        if role:
            filters &= Q(role__icontains=role)
        if date:
            try:
                filters &= Q(posted_on=date)  # Assuming date is provided in 'YYYY-MM-DD' format
            except ValueError:
                return Response({"error": "Invalid date format. Use 'YYYY-MM-DD'."}, status=status.HTTP_400_BAD_REQUEST)

        # Apply the filters in a single query
        queryset = Posts.objects.filter(filters)

        serializer = SearchSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)