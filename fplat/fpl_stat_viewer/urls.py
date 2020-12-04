from django.urls import path
from fpl_stat_viewer import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:player_id>', views.player, name='player'),
]
