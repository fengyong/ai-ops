from django.urls import path
from .views import get_permissions, get_menus
from .auth_views import user_login, user_logout, user_info

urlpatterns = [
    path('permissions/', get_permissions, name='get_permissions'),
    path('menus/', get_menus, name='get_menus'),
    path('login/', user_login, name='user_login'),
    path('logout/', user_logout, name='user_logout'),
    path('user-info/', user_info, name='user_info'),
]
