from django.urls import path
from .views import *

urlpatterns = [
   
    path('list_of_posts/', List_of_posts.as_view(), name='list_of_posts'),
    path('detail_view_post/<int:post_id>/', Detail_view_post.as_view(), name='detail_view_post'),
    path('apply_Job/', Apply_Job.as_view(), name='apply_Job'),
    path('search/', AdvancedSearchAPIView.as_view(), name='search'),
    # path('verify_email/', VerifyEmail.as_view(), name='verify_email'),
] 