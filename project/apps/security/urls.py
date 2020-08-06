from django.conf.urls import url
from rest_framework import routers
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
)

router = routers.DefaultRouter()

urlpatterns = [
    # url(r'^login', views.AuthView.as_view()),
    url(r'^users/$', views.UsersView.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UsersView.as_view()),
    url(r'^recover-password/$', views.RecoverPasswordView.as_view()),
    url(r'^reset-password/$', views.ResetPasswordView.as_view()),
    url(r'^register/$', views.RegisterView.as_view()),
    # url(r'^token/$', TokenObtainPairView.as_view()),
    url(r'^token-refresh/$', TokenRefreshView.as_view()),
    url(r'^token/$', views.MyTokenObtainPairView.as_view()),
    url(r'^$', views.error_404_view),
]

urlpatterns += router.urls
