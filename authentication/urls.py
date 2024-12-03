from django.urls import path, include
from rest_framework.routers import DefaultRouter

from authentication import views

router = DefaultRouter()

router.register('profile', views.ProfileView, basename='profile')
router.register('leaderboard', views.LeaderboardView, basename='leaderboard')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', views.LoginView.as_view(), name='login'),
    path('refresh_token/', views.RefreshTokenView.as_view(), name='token_refresh'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('verify_email/<token>/', views.VerifyEmailView.as_view(), name='verify_email'),
    path('password_reset_request', views.PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password_reset_confirm/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

]
