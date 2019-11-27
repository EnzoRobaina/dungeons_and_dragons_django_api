"""trabalho URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include
from rest_framework import routers
from api import views

router = routers.DefaultRouter()

router.register(r'characters', views.CharacterViewSet)
router.register(r'skills', views.SkillViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('v1/', include(router.urls)),
    path(
        'v1/characters/<int:character_pk>/skills/',
        views.SkillsManagerView.as_view(),
        name='skills_manager'
    ),
    path(
        'v1/characters/<int:character_pk>/skills/<int:skill_pk>/',
        views.SkillsNestedInCharacterViewSet.as_view(),
        name='skills_nested_in_character'
    )
]
