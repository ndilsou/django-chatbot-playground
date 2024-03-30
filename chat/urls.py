"""
URL configuration for chat project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include

# from rest_framework import routers
from rest_framework_nested import routers

from chat.api import views
# from . import admin

router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet)
router.register(r"groups", views.GroupViewSet)
router.register(r"system-prompts", views.SystemPromptViewSet)
router.register(r"conversations", views.ConversationViewSet)
router.register(r"messages", views.MessageViewSet)
router.register(r"tags", views.TagViewSet)
router.register(r"notes", views.NoteViewSet)

conversations_router = routers.NestedSimpleRouter(
    router, r"conversations", lookup="conversation"
)
conversations_router.register(
    r"messages", views.MessageViewSet, basename="conversation-messages"
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/", include(conversations_router.urls)),
    path("api/auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("api/dj-rest-auth/", include("dj_rest_auth.urls")),
    path("api/dj-rest-auth/registration/", include("dj_rest_auth.registration.urls")),
    path("api/dj-rest-auth/google/", views.GoogleLogin.as_view(), name="google_login"),
    path("api/dj-rest-auth/github/", views.GitHubLogin.as_view(), name="github_login"),
    path("api/accounts/", include("allauth.urls")),
]
