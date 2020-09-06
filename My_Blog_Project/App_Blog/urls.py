from django.urls import path
from . import views
app_name = "App_Blog"

urlpatterns = [
    path("",views.BlogList.as_view(),name="blog_list"),
    path("write/",views.CreateBlog,name="create_blog"),
    path("details/<slug:slug>",views.blog_details,name="blog_details"),
    path('edit/<int:pk>/', views.UpdateBlog.as_view(), name='edit_blog'),
    path("myblogs/",views.myblog,name='my_blogs'),
    path("liked/<int:pk>",views.liked,name="liked_post"),
    path("unliked/<int:pk>",views.unliked,name="unliked_post")
]
