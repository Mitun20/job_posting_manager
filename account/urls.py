from django.urls import path
from .views import *
from django.conf.urls.static import static


urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('', Login.as_view(), name='login'),
    path('forget_password/', ForgetPassword.as_view(), name='forget_password'),
    path('change_password/', ChangePassword.as_view(), name='change_password'),
    path('create_department/', CreateDepartment.as_view(), name='create_department'),
    path('retrieve_departments/', RetrieveDepartments.as_view(), name='retrieve_departments'),
    path('update_department/<int:department_id>/', UpdateDepartment.as_view(), name='update_department'),
    path('inactive_department/<int:department_id>/', InactiveDepartment.as_view(), name='inactive_department'),
    path('create_role/', CreateRole.as_view(), name='create_role'),
    path('retrieve_roles/', RetrieveRoles.as_view(), name='retrieve_roles'),
    path('update_role/<int:role_id>/', UpdateRole.as_view(), name='update_role'),
    path('inactive_role/<int:role_id>/', InactiveRole.as_view(), name='inactive_role'),
    path('get_department/', get_department.as_view(), name='get_department'),
    path('get_role/', get_role.as_view(), name='get_role'),
    path('create_post/', CreatePosts.as_view(), name='create_post'),
    path('update_post/<int:post_id>/', UpdatePosts.as_view(), name='update_post'),
    path('inactive_post/<int:post_id>/', InactivePosts.as_view(), name='inactive_post'),
    path('job_postings/', JobPostingsListView.as_view(), name='job_postings_list'),
    path('list_application/<int:post_id>/', ListApplication.as_view(), name='list_application'),
    path('applicant_profile/<int:applicant_id>/', Applicant_Profile.as_view(), name='applicant_profile'),
    path('download_resume/<int:applicant_id>/', Download_Resume.as_view(), name='download_resume'),
    path('advanced_search/', AdvancedSearchAPIView.as_view(), name='advanced_search'),
    path('filter_posts/', PostFilterView.as_view(), name='filter-posts'),
    

    
] 
