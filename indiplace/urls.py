from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views

urlpatterns = [
    path('member', views.MemberList.as_view()),
    path('member/<int:pk>', views.MemberDetail.as_view()),
    path('artist', views.ArtistList.as_view()),
    path('artist/<int:pk>', views.ArtistDetail.as_view()),
    path('performance', views.PerformanceList.as_view()),
    path('performance/<int:pk>', views.PerformanceDetail.as_view()),
    path('genre', views.GenreList.as_view()),
]
