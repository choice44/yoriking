from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views
from django.urls import path

urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('mypage/', views.MypageView.as_view(), name='mypage'),
    path('login/', views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('<int:user_id>/', views.UserView.as_view(), name='user_view'),
    path('<int:user_id>/follow/', views.FollowView.as_view(), name='follow_view'),
]

