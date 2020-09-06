from django.urls import path, include
from . import views
app_name = "App_Login"

urlpatterns = [
    path('signup/',views.sign_up,name="signup"),
    path('login/',views.login_page,name="login"),
    path('profile/',views.profile,name="profile"),
    path('logout/',views.logout_user,name="logout"),
    path("change_profile/",views.user_change,name="user_change"),
    path("add_picture/",views.add_pro_pic,name="add_pro_pic"),
    path('change_picture',views.change_pro_pic,name="change_pro_pic")
    
]
