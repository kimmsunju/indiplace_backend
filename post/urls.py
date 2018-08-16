from django.urls import path
from . import views

urlpatterns = [
    path('', views.MemberList.as_view()),
    path('<int:pk>/', views.MemberDetail.as_view())
]
