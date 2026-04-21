from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('post/', views.post_question, name='post_question'),
    path('question/<int:question_id>/', views.question_detail, name='question_detail'),
    path('answer/<int:answer_id>/like/', views.toggle_like, name='toggle_like'),
    # Communities & Groups
    path('communities/', views.group_list, name='group_list'),
    path('communities/create/', views.create_group, name='create_group'),
    path('communities/<int:group_id>/', views.group_detail, name='group_detail'),
    path('communities/<int:group_id>/join/', views.join_group, name='join_group'),
    path('communities/<int:group_id>/leave/', views.leave_group, name='leave_group'),
    path('communities/<int:group_id>/post/', views.post_question, name='post_question_group'),
    
    # Polls System
    path('communities/<int:group_id>/poll/', views.create_poll, name='create_poll'),
    path('poll/<int:poll_id>/vote/', views.vote_poll, name='vote_poll'),

    # Authentication
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='discussion/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
