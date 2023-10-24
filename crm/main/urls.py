from django.urls import path
from .views import index, attendance_detail


urlpatterns = [
    path('', index, name='index'),
    path('<int:team_id>/attendance/', attendance_detail, name='attendance_detail'),
]
