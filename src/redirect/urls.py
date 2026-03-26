from django.urls import path
from . import views

REDIRECT_PATTERN_PREFIX = 'r/'

urlpatterns = [
    
    path(REDIRECT_PATTERN_PREFIX + '<str:code>/+', views.inspect_view),
    path(REDIRECT_PATTERN_PREFIX + '<str:code>+/', views.inspect_view),
    path(REDIRECT_PATTERN_PREFIX + '<str:code>+', views.inspect_view),
    
    path(REDIRECT_PATTERN_PREFIX + '<str:code>/', views.redirect_view),
    path(REDIRECT_PATTERN_PREFIX + '<str:code>', views.redirect_view),
    
    path('dashboard/', views.dashboard_view, name='dashboard'),
]



    