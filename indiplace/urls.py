from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login', views.Authorization.as_view()),
    path('member', views.MemberList.as_view()),
    path('member/<int:pk>', views.MemberDetail.as_view()),
    path('artist', views.ArtistList.as_view()),
    path('artist/<int:pk>', views.ArtistDetail.as_view()),
    path('performance', views.PerformanceList.as_view()),
    path('performance/<int:pk>', views.PerformanceDetail.as_view()),
    path('performance/main', views.PerformanceView.as_view()),
    path('performance/recently', views.PerformanceRecent.as_view()),
    path('favorite', views.FavoriteArtistList.as_view()),
] 

# 어떤 URL을 정적으로 추가할래? > MEDIA_URL을 static 파일 경로로 추가
# 실제 파일은 어디에 있는데? > MEDIA_ROOT 경로내의 파일을 static 파일로 설정
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),