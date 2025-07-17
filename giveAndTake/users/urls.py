from django.urls import path
from .views import create_user, user_detail


urlpatterns = [
    path('create/', create_user, name='create_user'),
    path('<str:email>/', user_detail, name='user_detail'),
    # path('<str:email>/', update_user, name='update_user'),
    # path('<str:email>/', delete_user, name='delete_user'),
]
